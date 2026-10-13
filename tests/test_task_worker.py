import json
import tempfile
import unittest
from pathlib import Path

from scripts.dae_task_worker import TaskError, execute, safe_relative_path


class TaskWorkerTests(unittest.TestCase):
    def test_rejects_parent_path(self):
        with self.assertRaises(TaskError):
            safe_relative_path("../outside.txt")

    def test_creates_bundle_and_report(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            manifest = root / "task.json"
            manifest.write_text(json.dumps({
                "task_id": "sample-task",
                "title": "Sample deliverable",
                "deliverables": [{"path": "deliverables/answer.md", "content": "# Complete\n"}],
            }), encoding="utf-8")
            report = execute(manifest, root / "output")
            self.assertEqual(report["status"], "READY_FOR_HUMAN_REVIEW")
            self.assertTrue((root / "output" / "sample-task-submission-bundle.zip").is_file())
            self.assertEqual(report["submission_status"], "NOT_SUBMITTED")
            self.assertEqual(report["payment_status"], "NOT_RECEIVED")

    def test_refuses_to_overwrite_workspace(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            manifest = root / "task.json"
            manifest.write_text(json.dumps({
                "task_id": "repeat",
                "title": "Repeat",
                "deliverables": [{"path": "answer.md", "content": "Draft"}],
            }), encoding="utf-8")
            execute(manifest, root / "output")
            with self.assertRaises(TaskError):
                execute(manifest, root / "output")


if __name__ == "__main__":
    unittest.main()
