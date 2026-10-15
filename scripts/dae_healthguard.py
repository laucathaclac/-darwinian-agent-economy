#!/usr/bin/env python3
"""Run DAE HealthGuard on a normalized position JSON file (offline, read-only)."""
from __future__ import annotations
import argparse, json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from dae.healthguard import assess_json  # noqa: E402

def main() -> int:
    parser = argparse.ArgumentParser(description="Assess a normalized lending position without signing or submitting transactions.")
    parser.add_argument("input", help="Path to a JSON file containing position data")
    parser.add_argument("--output", help="Optional path for the JSON assessment report")
    args = parser.parse_args()
    try:
        payload = json.loads(Path(args.input).read_text(encoding="utf-8"))
        result = assess_json(payload)
    except (OSError, json.JSONDecodeError, TypeError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    rendered = json.dumps(result, indent=2, ensure_ascii=False, allow_nan=False) + "\n"
    if args.output:
        Path(args.output).write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
