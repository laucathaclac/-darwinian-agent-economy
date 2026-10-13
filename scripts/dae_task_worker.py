"""Execute a reviewed DAE task manifest into a deliverable bundle.

This worker performs bounded local work: materialize declared files, run built-in
quality checks, and package the result. It never accepts a task, contacts a client,
runs task-supplied commands, handles wallet secrets, or submits/publishes anything.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

MAX_FILES = 100
MAX_FILE_BYTES = 1_000_000
SECRET_PATTERNS = (
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(r"\b(?:api[_-]?key|secret|token|password)\s*[:=]\s*['\"][^'\"]{12,}['\"]", re.I),
    re.compile(r"\b0x[a-fA-F0-9]{64}\b"),
)


class TaskError(ValueError):
    """The task manifest or resulting deliverables failed validation."""


def safe_relative_path(value: str) -> Path:
    if not isinstance(value, str) or not value.strip():
        raise TaskError("Every deliverable needs a non-empty path.")
    posix = PurePosixPath(value.replace("\\", "/"))
    if posix.is_absolute() or any(part in ("", ".", "..") for part in posix.parts):
        raise TaskError(f"Unsafe deliverable path: {value!r}")
    if posix.parts and ":" in posix.parts[0]:
        raise TaskError(f"Drive-qualified path is not allowed: {value!r}")
    return Path(*posix.parts)


def load_manifest(path: Path) -> dict:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise TaskError(f"Cannot read valid JSON manifest: {exc}") from exc
    if not isinstance(payload, dict):
        raise TaskError("Manifest root must be a JSON object.")
    for field in ("task_id", "title", "deliverables"):
        if field not in payload:
            raise TaskError(f"Missing required manifest field: {field}")
    if not isinstance(payload["deliverables"], list) or not payload["deliverables"]:
        raise TaskError("deliverables must be a non-empty list.")
    if len(payload["deliverables"]) > MAX_FILES:
        raise TaskError(f"At most {MAX_FILES} deliverables are allowed.")
    for item in payload["deliverables"]:
        if not isinstance(item, dict) or "path" not in item or "content" not in item:
            raise TaskError("Each deliverable must include path and content.")
        safe_relative_path(item["path"])
        if not isinstance(item["content"], str):
            raise TaskError("Deliverable content must be UTF-8 text.")
        if len(item["content"].encode("utf-8")) > MAX_FILE_BYTES:
            raise TaskError(f"Deliverable exceeds {MAX_FILE_BYTES} bytes: {item['path']}")
    return payload


def inspect_content(path: str, content: str) -> list[str]:
    findings = []
    if not content.strip():
        findings.append(f"{path}: empty file")
    for pattern in SECRET_PATTERNS:
        if pattern.search(content):
            findings.append(f"{path}: possible credential/private-key material detected")
            break
    return findings


def execute(manifest_path: Path, output_root: Path) -> dict:
    task = load_manifest(manifest_path)
    task_id = re.sub(r"[^A-Za-z0-9._-]+", "-", str(task["task_id"])).strip(".-")
    if not task_id:
        raise TaskError("task_id must contain at least one safe character.")
    workspace = output_root.resolve() / task_id
    workspace.mkdir(parents=True, exist_ok=True)

    # Refuse to overwrite previous work; this avoids silently destroying a draft.
    if any(workspace.iterdir()):
        raise TaskError(f"Workspace already contains files: {workspace}. Choose a new output root or task_id.")

    records = []
    findings = []
    for item in task["deliverables"]:
        relative = safe_relative_path(item["path"])
        content = item["content"]
        findings.extend(inspect_content(item["path"], content))
        destination = (workspace / relative).resolve()
        if workspace.resolve() not in destination.parents:
            raise TaskError(f"Deliverable escapes workspace: {item['path']}")
        destination.parent.mkdir(parents=True, exist_ok=True)
        data = content.encode("utf-8")
        destination.write_bytes(data)
        records.append({
            "path": relative.as_posix(),
            "bytes": len(data),
            "sha256": hashlib.sha256(data).hexdigest(),
        })

    checks = {
        "all_files_nonempty": not any("empty file" in item for item in findings),
        "no_obvious_secrets": not any("credential/private-key" in item for item in findings),
        "declared_files_written": len(records) == len(task["deliverables"]),
    }
    passed = all(checks.values())
    generated_at = datetime.now(timezone.utc).isoformat()
    report = {
        "schema_version": "1.0",
        "task_id": task_id,
        "title": str(task["title"]),
        "source_url": str(task.get("source_url", "")),
        "generated_at": generated_at,
        "status": "READY_FOR_HUMAN_REVIEW" if passed else "BLOCKED",
        "checks": checks,
        "findings": findings,
        "deliverables": records,
        "submission_status": "NOT_SUBMITTED",
        "payment_status": "NOT_RECEIVED",
        "notice": "Local checks are not proof of task acceptance, eligibility, funding, or payment.",
    }
    (workspace / "dae_execution_report.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    bundle_path = output_root.resolve() / f"{task_id}-submission-bundle.zip"
    with zipfile.ZipFile(bundle_path, "w", compression=zipfile.ZIP_DEFLATED) as bundle:
        for file_path in sorted(workspace.rglob("*")):
            if file_path.is_file():
                bundle.write(file_path, file_path.relative_to(workspace).as_posix())
    report["bundle_path"] = str(bundle_path)
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description="DAE bounded local task worker")
    parser.add_argument("--manifest", required=True, type=Path, help="Reviewed JSON task manifest")
    parser.add_argument("--output", type=Path, default=Path("work-output"), help="Output directory")
    args = parser.parse_args()
    try:
        report = execute(args.manifest, args.output)
    except TaskError as exc:
        print(f"DAE task worker blocked: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if report["status"] == "READY_FOR_HUMAN_REVIEW" else 1


if __name__ == "__main__":
    raise SystemExit(main())
