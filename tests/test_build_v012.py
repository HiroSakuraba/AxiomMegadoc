"""Verification against the authoritative packaged v0.9D ledger."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile

SRC = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC))
from build_v012 import ARCHIVE, build, _eligible_pair, _checksum_matches


class MegaDocV012Tests(unittest.TestCase):
    def setUp(self):
        self.workspace = tempfile.TemporaryDirectory()
        self.addCleanup(self.workspace.cleanup)
        self.base = Path(self.workspace.name)

    def test_build_is_deterministic_and_nonempty(self):
        first = self.base / "first"
        second = self.base / "second"
        m1 = build(ARCHIVE, first)
        m2 = build(ARCHIVE, second)
        self.assertEqual((first / "manifest.json").read_bytes(),
                         (second / "manifest.json").read_bytes())
        self.assertGreater(m1["generated_docs"], 10)
        self.assertTrue(m1["no_invented_compiler_results"])
        self.assertFalse(m1["runtime_traces_executed"])
        self.assertEqual(m1["records_in_ledger"], 520)
        self.assertEqual(len(m1["documents"]), m1["generated_docs"])
        self.assertEqual(
            {p.relative_to(first).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
             for p in first.rglob("*") if p.is_file()},
            {p.relative_to(second).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
             for p in second.rglob("*") if p.is_file()},
        )

    def test_provenance_and_exact_text_hashes(self):
        out = self.base / "corpus"
        manifest = build(ARCHIVE, out)
        seen = set()
        for doc in manifest["documents"]:
            self.assertNotIn(doc["id"], seen)
            seen.add(doc["id"])
            text = (out / doc["path"]).read_bytes()
            attrs = json.loads((out / doc["attributes_path"]).read_text())
            self.assertEqual(hashlib.sha256(text).hexdigest(), doc["text_sha256"])
            self.assertEqual(attrs["text_sha256"], doc["text_sha256"])
            self.assertEqual(attrs["record_ids"], doc["record_ids"])
            self.assertEqual(attrs["split"], doc["split"])
            self.assertTrue(all(attrs["validations"].values()))
            self.assertEqual(attrs["trust"], "checker-observed-diagnostic")
            self.assertIn(b"<AXIOM_MEGADOC ", text)
            self.assertIn(b"</AXIOM_MEGADOC>", text)
        self.assertEqual(sum(manifest["split_counts"].values()), len(seen))

    def test_records_byte_copy(self):
        out = self.base / "corpus"
        manifest = build(ARCHIVE, out, 3)
        self.assertEqual(manifest["selected_source_records"], 6)
        records = list((out / "records").glob("*.json"))
        self.assertEqual(len(records), 6)
        for path in records:
            record = json.loads(path.read_text())
            self.assertTrue(_checksum_matches(record))
            self.assertEqual(
                hashlib.sha256(record["record_id"].encode()).hexdigest()[:24] + ".json",
                path.name,
            )

    def test_safe_output_and_bounds(self):
        with self.assertRaisesRegex(ValueError, "positive"):
            build(ARCHIVE, self.base / "no", 0)
        out = self.base / "nonempty"
        out.mkdir()
        (out / "unrelated").write_text("do not overwrite")
        with self.assertRaisesRegex(ValueError, "empty"):
            build(ARCHIVE, out)
        with self.assertRaisesRegex(ValueError, "not a valid ZIP"):
            (self.base / "bad.zip").write_bytes(b"junk")
            build(self.base / "bad.zip", self.base / "badout")

    def test_unverified_semantic_label_is_excluded(self):
        valid = {
            "is_valid": True,
            "language": "axiom_scheme",
            "contrast_group_id": "same",
            "split_group_key": "same",
            "split": "train",
            "canonical_source": "s",
            "canonical_source_hash": hashlib.sha256(b"s").hexdigest(),
            "validation": {"static": {"status": "pass"}},
        }
        invalid = dict(valid, is_valid=False,
                       diagnostic_codes=["SEMANTIC_EXPECTED_OUTPUT_MISMATCH"],
                       validation={"static": {"status": "pass", "diagnostics": []}})
        self.assertEqual(_eligible_pair(valid, invalid),
                         (False, "diagnostic_not_static_checker_observed"))
        invalid["validation"] = {"static": {
            "status": "fail", "diagnostics": ["SEMANTIC_EXPECTED_OUTPUT_MISMATCH"]}}
        self.assertTrue(_eligible_pair(valid, invalid)[0])
        invalid["split"] = "test"
        self.assertEqual(_eligible_pair(valid, invalid)[1], "cross_split_or_group")

    def test_externally_runnable_cli(self):
        output = self.base / "small"
        proc = subprocess.run([sys.executable, str(SRC / "build_v012.py"),
                               "--output", str(output), "--max-docs", "5"],
                              check=True, capture_output=True, text=True)
        summary = json.loads(proc.stdout)
        self.assertEqual(summary["generated_docs"], 5)
        self.assertEqual(len(list((output / "megadocs").glob("*.md"))), 5)


if __name__ == "__main__":
    unittest.main()
