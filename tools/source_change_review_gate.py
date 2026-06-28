#!/usr/bin/env python3
"""Source change review gate for ElectroScheme Studio.

This tool is non-destructive. It classifies the current dirty tree and writes
reports for review before accepting or reverting coding-agent work.
"""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path
from typing import Any


SOURCE_PREFIXES = (
    "backend/",
    "frontend/",
    "schemas/",
    "examples/",
)

LOCAL_ONLY_PREFIXES = (
    "_logs/",
    "_reports/",
    "_patches/",
)

REVIEW_CANDIDATES = (
    "backend/app/api/symbol_library.py",
    "backend/app/core/symbol_service.py",
    "backend/app/schemas/symbol_library.py",
    "frontend/src/components/SvgSymbol.vue",
    "frontend/src/components/SymbolEditor.vue",
    "frontend/src/lib/editorTypes.ts",
    "frontend/src/lib/routing.ts",
)


def run_git(root: Path, args: list[str]) -> dict[str, Any]:
    completed = subprocess.run(
        ["git", *args],
        cwd=root,
        text=True,
        encoding="utf-8",
        errors="replace",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    return {
        "args": ["git", *args],
        "returncode": completed.returncode,
        "stdout": completed.stdout,
        "stderr": completed.stderr,
    }


def classify_path(path: str) -> str:
    normalized = path.replace("\\", "/")
    if normalized.startswith("backend/app/data/"):
        return "symbol_data_candidate"
    if normalized in REVIEW_CANDIDATES:
        return "symbol_editor_candidate"
    if normalized.startswith("backend/"):
        return "backend_source"
    if normalized.startswith("frontend/"):
        return "frontend_source"
    if normalized.startswith("examples/"):
        return "example_data"
    if normalized.startswith("schemas/"):
        return "schema"
    if normalized.startswith("docs/"):
        return "docs"
    if normalized.startswith("tools/"):
        return "tooling"
    if normalized.startswith(LOCAL_ONLY_PREFIXES):
        return "local_artifact"
    if normalized in {"ГОСТ/", "План.txt"} or normalized.startswith("ГОСТ/"):
        return "local_reference"
    if normalized.endswith(".vsdx") or normalized.endswith(".vss") or normalized.endswith(".vsd"):
        return "local_visio_bank"
    return "other"


def parse_short_status(text: str) -> list[dict[str, str]]:
    items: list[dict[str, str]] = []
    for raw_line in text.splitlines():
        if not raw_line.strip():
            continue
        status = raw_line[:2]
        path = raw_line[3:] if len(raw_line) > 3 else ""
        items.append(
            {
                "status": status,
                "path": path,
                "class": classify_path(path),
                "decision": suggest_decision(status, path),
            }
        )
    return items


def suggest_decision(status: str, path: str) -> str:
    normalized = path.replace("\\", "/")
    cls = classify_path(normalized)

    if cls in {"local_artifact", "local_reference", "local_visio_bank"}:
        return "ignore_or_keep_local"
    if cls in {"symbol_editor_candidate", "symbol_data_candidate"}:
        return "review_for_acceptance_or_rewrite"
    if cls in {"backend_source", "frontend_source", "example_data"}:
        return "diff_review_required"
    if status.startswith("??") and normalized.startswith(SOURCE_PREFIXES):
        return "review_untracked_source"
    return "manual_review"


def summarize(items: list[dict[str, str]]) -> dict[str, int]:
    result: dict[str, int] = {}
    for item in items:
        cls = item.get("class", "other")
        result[cls] = result.get(cls, 0) + 1
    return dict(sorted(result.items()))


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value, encoding="utf-8")


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")


def write_markdown(path: Path, report: dict[str, Any]) -> None:
    items = report["status_items"]
    lines: list[str] = []

    lines.append("# Source change review gate")
    lines.append("")
    lines.append(f"HEAD: `{report['head']['stdout'].strip()}`")
    lines.append("")
    lines.append("## Summary by class")
    lines.append("")
    lines.append("| Class | Count |")
    lines.append("|---|---:|")
    for cls, count in report["summary_by_class"].items():
        lines.append(f"| {cls} | {count} |")
    lines.append("")
    lines.append("## Files requiring review")
    lines.append("")
    lines.append("| Status | Class | Decision | Path |")
    lines.append("|---|---|---|---|")
    for item in items:
        lines.append(f"| `{item['status']}` | {item['class']} | {item['decision']} | `{item['path']}` |")
    lines.append("")
    lines.append("## Symbol editor candidates")
    lines.append("")
    candidates = [item for item in items if item["class"] in {"symbol_editor_candidate", "symbol_data_candidate"}]
    if candidates:
        for item in candidates:
            lines.append(f"- `{item['path']}` — {item['decision']}")
    else:
        lines.append("- No explicit symbol editor candidates found.")
    lines.append("")
    lines.append("## Recommended next action")
    lines.append("")
    lines.append("1. Review backend/frontend diffs.")
    lines.append("2. Decide whether the coding-agent symbol-library implementation is salvageable.")
    lines.append("3. If salvageable, create a controlled acceptance patch.")
    lines.append("4. If not salvageable, create a quarantine/revert patch and keep Visio importer path.")
    lines.append("5. Do not mix cleanup, import conversion and editor features in one patch.")
    lines.append("")
    lines.append("## Diff stat")
    lines.append("")
    lines.append("```text")
    lines.append(report["diff_stat"]["stdout"].strip())
    lines.append("```")
    lines.append("")

    write_text(path, "\n".join(lines) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(description="Review dirty source changes before accepting coding-agent work.")
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--out", type=Path, default=Path("_reports/source_change_review"))
    args = parser.parse_args()

    root = args.root.resolve()
    out = args.out.resolve()
    out.mkdir(parents=True, exist_ok=True)

    status = run_git(root, ["status", "--short"])
    diff_stat = run_git(root, ["diff", "--stat"])
    diff_name_status = run_git(root, ["diff", "--name-status"])
    diff_patch = run_git(root, ["diff", "--", "backend", "frontend", "examples", "schemas"])
    untracked = run_git(root, ["ls-files", "--others", "--exclude-standard"])
    head = run_git(root, ["log", "-1", "--oneline"])

    items = parse_short_status(status["stdout"])
    summary = summarize(items)

    report = {
        "root": str(root),
        "head": head,
        "status": status,
        "status_items": items,
        "summary_by_class": summary,
        "diff_stat": diff_stat,
        "diff_name_status": diff_name_status,
        "untracked_excluding_ignored": untracked,
        "review_policy": {
            "non_destructive": True,
            "do_not_commit_dirty_source_automatically": True,
            "do_not_delete_dirty_source_automatically": True,
            "acceptance_requires_build_gate": True,
            "visio_import_path_remains_preferred_source_of_truth": True,
        },
    }

    write_json(out / "source_change_review.json", report)
    write_markdown(out / "README.md", report)
    write_text(out / "git_status_short.txt", status["stdout"])
    write_text(out / "git_diff_stat.txt", diff_stat["stdout"])
    write_text(out / "git_diff_name_status.txt", diff_name_status["stdout"])
    write_text(out / "git_diff_backend_frontend_examples_schemas.patch", diff_patch["stdout"])
    write_text(out / "git_untracked_excluding_ignored.txt", untracked["stdout"])

    print(json.dumps({"out": str(out), "summary_by_class": summary}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())