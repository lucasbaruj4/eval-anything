import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "skills/eval-anything/scripts/prepare_review.py"


class PrepareReviewTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.source = self.root / "results.json"
        self.destination = self.root / "copies"
        self.data = {
            "criteria": ["Keep the delivery date."],
            "pairs": [
                {
                    "id": "private-task-identifier",
                    "prompt": "Rewrite the source: café delivery takes five days.",
                    "outputs": [
                        {"condition": "private-new-skill", "model": "private-model-name",
                         "text": "Delivery takes five days.\n\nCafé orders too."},
                        {"condition": "private-old-skill", "model": "private-model-name",
                         "text": "Café orders arrive in five days.\n"},
                    ],
                }
            ],
        }

    def run_cli(self, data=None):
        self.source.write_text(json.dumps(self.data if data is None else data), encoding="utf-8")
        return subprocess.run([sys.executable, str(SCRIPT), str(self.source), str(self.destination)],
                              capture_output=True, text=True)

    def test_review_copies_preserve_content_without_identity_metadata(self):
        self.data["pairs"][0]["outputs"][0]["trace"] = "/private/session/path"
        result = self.run_cli()
        self.assertEqual(result.returncode, 0, result.stderr)
        public_text = (self.destination / "review/pack.json").read_text()
        public = json.loads(public_text)
        self.assertEqual(public["criteria"], self.data["criteria"])
        self.assertEqual(public["items"][0]["prompt"], self.data["pairs"][0]["prompt"])
        self.assertCountEqual([public["items"][0][side] for side in ("A", "B")],
                              [output["text"] for output in self.data["pairs"][0]["outputs"]])
        for secret in ("private-task-identifier", "private-model-name", "private-new-skill",
                       "private-old-skill", "/private/session/path"):
            self.assertNotIn(secret, public_text)

    def test_private_key_resolves_every_shuffled_output(self):
        second = copy.deepcopy(self.data["pairs"][0])
        second["id"] = "second-private-task"
        second["prompt"] = "Write a short notice."
        second["outputs"][0]["text"] = "The office opens Monday."
        second["outputs"][1]["text"] = "Office hours start on Monday."
        self.data["pairs"].append(second)
        result = self.run_cli()
        self.assertEqual(result.returncode, 0, result.stderr)
        public = json.loads((self.destination / "review/pack.json").read_text())
        key = json.loads((self.destination / "private/key.json").read_text())
        self.assertEqual(len(public["items"]), 2)
        seen = []
        for item in public["items"]:
            identity = key[item["label"]]
            source = next(pair for pair in self.data["pairs"] if pair["id"] == identity["pair_id"])
            seen.append(source["id"])
            self.assertEqual(item["prompt"], source["prompt"])
            for side in ("A", "B"):
                original = next(output for output in source["outputs"]
                                if output["condition"] == identity[side]["condition"])
                self.assertEqual(item[side], original["text"])
                self.assertEqual(identity[side]["model"], original["model"])
        self.assertCountEqual(seen, [pair["id"] for pair in self.data["pairs"]])

    def test_empty_criteria_support_initial_human_preferences(self):
        self.data["criteria"] = []
        self.assertEqual(self.run_cli().returncode, 0)

    def test_invalid_pairs_leave_no_review_folder(self):
        invalid = []
        for field in ("prompt", "id"):
            data = copy.deepcopy(self.data)
            data["pairs"][0][field] = ""
            invalid.append(data)
        for field in ("text", "condition", "model"):
            data = copy.deepcopy(self.data)
            del data["pairs"][0]["outputs"][0][field]
            invalid.append(data)
        data = copy.deepcopy(self.data)
        data["pairs"][0]["outputs"].pop()
        invalid.extend([data, {"criteria": [], "pairs": []}, []])
        for data in invalid:
            with self.subTest(data=data):
                result = self.run_cli(data)
                self.assertNotEqual(result.returncode, 0)
                self.assertFalse(self.destination.exists())

    def test_duplicate_pair_ids_are_rejected(self):
        self.data["pairs"].append(copy.deepcopy(self.data["pairs"][0]))
        self.assertNotEqual(self.run_cli().returncode, 0)
        self.assertFalse(self.destination.exists())

    def test_same_condition_is_rejected(self):
        self.data["pairs"][0]["outputs"][1]["condition"] = "private-new-skill"
        self.assertNotEqual(self.run_cli().returncode, 0)
        self.assertFalse(self.destination.exists())

    def test_different_models_are_rejected(self):
        self.data["pairs"][0]["outputs"][1]["model"] = "different-model"
        self.assertNotEqual(self.run_cli().returncode, 0)
        self.assertFalse(self.destination.exists())

    def test_existing_results_are_never_overwritten(self):
        self.assertEqual(self.run_cli().returncode, 0)
        pack = self.destination / "review/pack.json"
        before = pack.read_bytes()
        result = self.run_cli()
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(pack.read_bytes(), before)

    def test_invalid_json_leaves_no_review_folder(self):
        self.source.write_text("not json")
        result = subprocess.run([sys.executable, str(SCRIPT), str(self.source), str(self.destination)],
                                capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(self.destination.exists())


if __name__ == "__main__":
    unittest.main()
