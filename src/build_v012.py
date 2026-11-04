#!/usr/bin/env python3
"""Deterministic, conservative AxiomMegaDoc corpus materializer.

Uses the v0.11 builder and v0.9D ledger *inside the committed milestone ZIP*.
Only emits latent_diagnostic records with checker-observed, matching diagnostics.
Does not invent runtime outputs, compiler results, or new corpus records.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import sys
import tempfile
import zipfile

ARCHIVE = Path(__file__).resolve().parent.parent / "axiom_megadoc_v0_11.zip"
LEDGER_END = "/source-corpus/axiom_v09d_ledger.jsonl"
BUILDER_END = "/src/megadoc_builder_batch.py"
SUPPORTED = {
    "axiom_scheme": "build_latent_diagnostic_scheme",
    "axiom_ml": "build_latent_diagnostic_ml",
    "axiom_prolog": "build_latent_diagnostic_prolog",
}
# The v0.11 templates explain LIST SUM and LIST APPEND. They are not
# semantically correct for parity, length, membership, trees, or DCGs.
PAPER_ALIGNED_FAMILIES = {
    "axiom_scheme": {"functional/list/sum"},
    "axiom_ml": {"typed/list/sum"},
    "axiom_prolog": {"logic/list/append-det"},
}
MAX_SOURCE_BYTES = 16_000_000


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def stable_json(value: object) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
            + "\n").encode("utf-8")


def _load_packaged_sources(archive_path: Path, temporary: Path):
    if not zipfile.is_zipfile(archive_path):
        raise ValueError("original v0.11 archive is not a valid ZIP")
    with zipfile.ZipFile(archive_path) as archive:
        names = archive.namelist()
        ledger_names = [n for n in names if n.endswith(LEDGER_END)]
        builder_names = [n for n in names if n.endswith(BUILDER_END)]
        if len(ledger_names) != 1 or len(builder_names) != 1:
            raise ValueError("expected exactly one v0.9D ledger and v0.11 builder in ZIP")
        ledger_info = archive.getinfo(ledger_names[0])
        builder_info = archive.getinfo(builder_names[0])
        if (ledger_info.file_size > MAX_SOURCE_BYTES
                or builder_info.file_size > MAX_SOURCE_BYTES):
            raise ValueError("source archive member too large")
        ledger_data = archive.read(ledger_info)
        builder_data = archive.read(builder_info)
    # Keep the archived module's path contract; it reads ../source-corpus/.
    src = temporary / "src"
    ledger_dir = temporary / "source-corpus"
    src.mkdir()
    ledger_dir.mkdir()
    (src / "megadoc_builder_batch.py").write_bytes(builder_data)
    (ledger_dir / "axiom_v09d_ledger.jsonl").write_bytes(ledger_data)
    module_path = src / "megadoc_builder_batch.py"
    spec = importlib.util.spec_from_file_location("_axiommegadoc_v011_builder", module_path)
    if spec is None or spec.loader is None:
        raise ValueError("cannot import packaged v0.11 builder")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    try:
        spec.loader.exec_module(module)
    finally:
        sys.modules.pop(spec.name, None)
    records = module.load_records()
    if len(records) == 0:
        raise ValueError("empty ledger")
    return module, records, digest(ledger_data), digest(builder_data)


def _checksum_matches(record: dict) -> bool:
    src = record.get("canonical_source")
    if not isinstance(src, str):
        return False
    expected = record.get("canonical_source_hash")
    return (isinstance(expected, str)
            and digest(src.encode("utf-8")) == expected)


def _eligible_pair(valid: dict, invalid: dict) -> tuple[bool, str]:
    if not valid.get("is_valid") or invalid.get("is_valid"):
        return False, "invalid_pair_roles"
    if valid.get("language") != invalid.get("language"):
        return False, "cross_language"
    if (valid.get("contrast_group_id") != invalid.get("contrast_group_id")
            or valid.get("split_group_key") != invalid.get("split_group_key")
            or valid.get("split") != invalid.get("split")):
        return False, "cross_split_or_group"
    if not _checksum_matches(valid) or not _checksum_matches(invalid):
        return False, "canonical_source_hash_mismatch"
    if valid.get("validation", {}).get("static", {}).get("status") != "pass":
        return False, "valid_record_unchecked"
    lane = invalid.get("validation", {}).get("static", {})
    codes = invalid.get("diagnostic_codes", [])
    observed = lane.get("diagnostics", [])
    if (lane.get("status") != "fail" or not codes
            or not isinstance(codes, list) or not isinstance(observed, list)
            or not set(codes).issubset(set(observed))):
        return False, "diagnostic_not_static_checker_observed"
    return True, ""


def _validate_doc(module, md, valid: dict, invalid: dict) -> None:
    flags = md.validation
    if not flags or not all(value is True for value in flags.values()):
        raise ValueError(f"megadoc validation flags failed: {flags}")
    if md.split != valid["split"] or md.record_ids != [
            valid["record_id"], invalid["record_id"]]:
        raise ValueError("wrong split or source record provenance")
    if md.construction != "latent_diagnostic":
        raise ValueError("unexpected construction")
    source_parts = [s.content for s in md.segments if s.segment_type == "source"]
    if len(source_parts) != 2:
        raise ValueError("expected exactly two canonical source segments")
    if not any(sep.join(source_parts) == valid["canonical_source"]
               for sep in ("", "\n")):
        raise ValueError("source segments do not reassemble exactly")
    mutation = [s for s in md.segments if s.segment_type == "invalid_mutation"]
    diagnostic = [s for s in md.segments if s.segment_type == "diagnostic"]
    if len(mutation) != 1 or mutation[0].content != invalid["canonical_source"]:
        raise ValueError("invalid canonical mutation mismatch")
    if (len(diagnostic) != 1 or diagnostic[0].trust_level != "checked"
            or diagnostic[0].content != ", ".join(invalid["diagnostic_codes"])):
        raise ValueError("diagnostic provenance mismatch")
    rendered = module.render_megadoc(md)
    parsed = module.parse_rendered(rendered)
    if (len(parsed) != len(md.segments)
            or any(part["content"] != original.content
                   for part, original in zip(parsed, md.segments))):
        raise ValueError("render/parse segment round-trip failed")
    if md.megadoc_id == "" or md.token_estimate <= 0:
        raise ValueError("empty generated document")


def _view_text(valid: dict, invalid: dict) -> str:
    """Benchmark-only paired source view: no generated rationale or checked label."""
    label_codes = json.dumps(invalid["diagnostic_codes"], ensure_ascii=False, sort_keys=True)
    observed = invalid.get("validation", {}).get("static", {})
    observation = json.dumps(observed, sort_keys=True, ensure_ascii=False)
    language = valid["language"]
    return ("# Axiom corpus record pair — benchmark-only provenance view\n"
            "This is NOT a paper-aligned latent diagnostic or a compiler-verified "
            "training example. Labels are distinguished from checker observations.\n\n"
            f"language: {language}\n"
            f"split: {valid['split']}\n"
            f"family: {valid.get('family', 'unspecified')}\n"
            f"valid_record_id: {valid['record_id']}\n"
            f"invalid_record_id: {invalid['record_id']}\n\n"
            "## Canonical record labelled valid\n\n"
            f"```{language}\n{valid['canonical_source']}\n```\n\n"
            "## Canonical record labelled invalid\n\n"
            f"```{language}\n{invalid['canonical_source']}\n```\n\n"
            "## Label metadata (not inherently checked)\n\n"
            f"recorded_diagnostic_codes: {label_codes}\n\n"
            "## Recorded static checker result\n\n"
            f"validation_static_json: {observation}\n")


def build(archive_path: Path, output: Path, max_docs: int | None = None) -> dict:
    if max_docs is not None and max_docs < 1:
        raise ValueError("--max-docs must be positive")
    if output.exists() and any(output.iterdir()):
        raise ValueError("output must be an empty directory; refusing to overwrite")
    if not archive_path.is_file():
        raise ValueError(f"source archive does not exist: {archive_path}")
    with tempfile.TemporaryDirectory(prefix="axiom-megadoc-v012-") as temp:
        module, records, ledger_sha, builder_sha = _load_packaged_sources(
            archive_path, Path(temp))
        by_group: dict[str, list[dict]] = defaultdict(list)
        for record in records:
            rid = record.get("record_id")
            group = record.get("contrast_group_id")
            if not isinstance(rid, str) or not isinstance(group, str):
                raise ValueError("record missing identity or contrast group")
            by_group[group].append(record)
        if len({r["record_id"] for r in records}) != len(records):
            raise ValueError("duplicate source record IDs")

        skipped = Counter()
        corpus: list[tuple[object, dict, dict]] = []
        views: list[tuple[dict, dict]] = []
        for group, members in sorted(by_group.items()):
            good = [r for r in members if r.get("is_valid") is True]
            bad = [r for r in members if r.get("is_valid") is False]
            if len(good) != 1 or len(bad) != 1:
                skipped["not_a_unique_pair"] += 1
                continue
            valid, invalid = good[0], bad[0]
            if valid.get("language") not in SUPPORTED:
                skipped["unsupported_language"] += 1
                continue
            # Broader record-pair views are usable for filesystem benchmarks;
            # they do not imply the annotated defect has been checker-proved.
            if (valid.get("language") == invalid.get("language")
                    and valid.get("split") == invalid.get("split")
                    and valid.get("split_group_key") == invalid.get("split_group_key")
                    and _checksum_matches(valid) and _checksum_matches(invalid)):
                views.append((valid, invalid))
            else:
                skipped["view_invalid_provenance"] += 1
                continue
            if valid.get("family") not in PAPER_ALIGNED_FAMILIES[valid["language"]]:
                skipped["rationale_not_semantically_applicable"] += 1
                continue
            eligible, reason = _eligible_pair(valid, invalid)
            if not eligible:
                skipped[reason] += 1
                continue
            try:
                md = getattr(module, SUPPORTED[valid["language"]])(valid, invalid)
                _validate_doc(module, md, valid, invalid)
            except (ValueError, KeyError, TypeError) as error:
                # Existing v0.11 templates are intentionally specialized.
                # Report every unsupported structure, never synthesize a repair.
                skipped["unsupported_template_or_validation"] += 1
                continue
            corpus.append((md, valid, invalid))
            if max_docs is not None and len(corpus) == max_docs:
                break

        if not corpus:
            raise ValueError("no checker-grounded megadocs could be constructed")

        output.mkdir(parents=True, exist_ok=True)
        docs = output / "megadocs"
        attributes = output / "attributes"
        records_dir = output / "records"
        streams = output / "streams"
        views_dir = output / "benchmark-views"
        for directory in (docs, attributes, records_dir, streams, views_dir):
            directory.mkdir()

        entries = []
        split_streams: dict[str, list[dict]] = defaultdict(list)
        used_ids = set()
        seen_record_ids = set()
        for md, valid, invalid in corpus:
            if md.megadoc_id in used_ids:
                raise ValueError(f"duplicate megadoc ID {md.megadoc_id}")
            used_ids.add(md.megadoc_id)
            text = md.rendered_text
            text_bytes = text.encode("utf-8")
            doc_rel = f"megadocs/{md.megadoc_id}.md"
            attr_rel = f"attributes/{md.megadoc_id}.json"
            (output / doc_rel).write_bytes(text_bytes)
            attr = {
                "schema": "axiom-megadoc-v012-attributes-v1",
                "megadoc_id": md.megadoc_id,
                "construction": md.construction,
                "language": md.language_set[0],
                "split": md.split,
                "record_ids": md.record_ids,
                "contrast_group_ids": md.contrast_group_ids,
                "trust": "checker-observed-diagnostic",
                "segment_count": len(md.segments),
                "source_sha256": [r["canonical_source_hash"] for r in (valid, invalid)],
                "text_sha256": digest(text_bytes),
                "approximate_word_count": md.token_estimate,
                "validations": md.validation,
            }
            (output / attr_rel).write_bytes(stable_json(attr))
            for record in (valid, invalid):
                rid = record["record_id"]
                if rid not in seen_record_ids:
                    seen_record_ids.add(rid)
                    (records_dir / (digest(rid.encode())[:24] + ".json")).write_bytes(
                        stable_json(record))
            entry = {
                "id": md.megadoc_id,
                "path": doc_rel,
                "attributes_path": attr_rel,
                "text_sha256": attr["text_sha256"],
                "split": md.split,
                "construction": md.construction,
                "language": attr["language"],
                "record_ids": md.record_ids,
                "approximate_word_count": md.token_estimate,
            }
            entries.append(entry)
            split_streams[md.split].append({
                "id": md.megadoc_id,
                "text": text,
                "source": "axiom_megadoc_v012_checker_grounded",
                "metadata": {key: attr[key] for key in (
                    "language", "split", "construction", "record_ids",
                    "text_sha256", "trust")},
            })
        benchmark_views = []
        for valid, invalid in views:
            # Also materialize all source record blobs, not just those that
            # qualify for the stronger latent-rationale trust contract.
            for record in (valid, invalid):
                rid = record["record_id"]
                if rid not in seen_record_ids:
                    seen_record_ids.add(rid)
                    (records_dir / (digest(rid.encode())[:24] + ".json")).write_bytes(
                        stable_json(record))
            identity = digest(valid["contrast_group_id"].encode("utf-8"))[:20]
            rel = f"benchmark-views/{identity}.md"
            view_bytes = _view_text(valid, invalid).encode("utf-8")
            (output / rel).write_bytes(view_bytes)
            benchmark_views.append({
                "path": rel,
                "text_sha256": digest(view_bytes),
                "language": valid["language"],
                "split": valid["split"],
                "family": valid["family"],
                "record_ids": [valid["record_id"], invalid["record_id"]],
                "claimed_diagnostic_codes": invalid["diagnostic_codes"],
                "observed_checker_status": invalid.get("validation", {}).get(
                    "static", {}).get("status"),
                "trust": "benchmark_only_unverified_labels",
            })
        for split, documents in sorted(split_streams.items()):
            with (streams / (split + ".jsonl")).open("wb") as handle:
                for item in documents:
                    handle.write(stable_json(item))
        manifest = {
            "schema": "axiom-megadoc-v012-manifest-v1",
            "source_bundle": "v0.11",
            "source_bundle_sha256": digest(archive_path.read_bytes()),
            "source_ledger_sha256": ledger_sha,
            "source_builder_sha256": builder_sha,
            "records_in_ledger": len(records),
            "generated_docs": len(entries),
            "benchmark_views": len(benchmark_views),
            "selected_source_records": len(seen_record_ids),
            "split_counts": dict(sorted(Counter(e["split"] for e in entries).items())),
            "language_counts": dict(sorted(Counter(e["language"] for e in entries).items())),
            "skipped_groups": dict(sorted(skipped.items())),
            "constructions": ["latent_diagnostic"],
            "paper_aligned_families": {
                language: sorted(families)
                for language, families in sorted(PAPER_ALIGNED_FAMILIES.items())
            },
            "benchmark_view_format": "non-training, source-pair provenance",
            "runtime_traces_executed": False,
            "no_invented_compiler_results": True,
            "approximate_word_count": sum(e["approximate_word_count"] for e in entries),
            "documents": entries,
            "views": benchmark_views,
        }
        (output / "manifest.json").write_bytes(stable_json(manifest))
        return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-zip", type=Path, default=ARCHIVE)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--max-docs", type=int)
    args = parser.parse_args()
    try:
        report = build(args.source_zip, args.output, args.max_docs)
    except (ValueError, OSError, zipfile.BadZipFile) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2
    print(json.dumps({
        k: v for k, v in report.items() if k not in ("documents", "views")
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
