#!/usr/bin/env python3
"""Repository hygiene audit for ElectroScheme Studio.

This tool is non-destructive:
- it does not delete files;
- it does not checkout/revert files;
- it does not stage or commit anything.

It writes a report describing the dirty working tree so the next patch can
decide what to keep, revert, ignore or quarantine.
"""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path
from typing import Any


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
    if normalized.startswith("backend/"):
        return "backend_source"
    if normalized.startswith("frontend/"):
        return "frontend_source"
    if normalized.startswith("schemas/"):
        return "schema"
    if normalized.startswith("docs/"):
        return "docs"
    if normalized.startswith("examples/"):
        return "example_data"
    if normalized.startswith("tools/"):
        return "tooling"
    if normalized.startswith("_patches/"):
        return "local_patch_artifact"
    if normalized.startswith("_reports/"):
        return "local_report_artifact"
    if normalized.startswith("_logs/"):
        return "local_log_artifact"
    if normalized.endswith(".vsdx") or normalized.endswith(".vss") or normalized.endswith(".vsd"):
        return "local_binary_source_bank"
    if normalized.endswith(".tsbuildinfo"):
        return "frontend_build_artifact"
    if normalized == "План.txt":
        return "local_plan"
    if normalized.startswith("ГОСТ/"):
        return "local_reference_docs"
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
            }
        )
    return items


def summarize(items: list[dict[str, str]]) -> dict[str, int]:
    result: dict[str, int] = {}
    for item in items:
        cls = item.get("class", "other")
        result[cls] = result.get(cls, 0) + 1
    return dict(sorted(result.items()))


def write_markdown(out_path: Path, status_items: list[dict[str, str]], summary: dict[str, int], diff_stat: str, head: str) -> None:
    lines: list[str] = []
    lines.append("# Repository hygiene audit")
    lines.append("")
    lines.append(f"HEAD: `{head.strip()}`")
    lines.append("")
    lines.append("## Summary by class")
    lines.append("")
    lines.append("| Class | Count |")
    lines.append("|---|---:|")
    for cls, count in summary.items():
        lines.append(f"| {cls} | {count} |")
    lines.append("")
    lines.append("## Dirty files")
    lines.append("")
    lines.append("| Status | Class | Path |")
    lines.append("|---|---|---|")
    for item in status_items:
        lines.append(f"| `{item['status']}` | {item['class']} | `{item['path']}` |")
    lines.append("")
    lines.append("## Diff stat")
    lines.append("")
    lines.append("```text")
    lines.append(diff_stat.strip())
    lines.append("```")
    lines.append("")
    lines.append("## Recommended next decisions")
    lines.append("")
    lines.append("1. Do not blindly delete or commit coding-agent work.")
    lines.append("2. Review backend/frontend source changes separately.")
    lines.append("3. Keep local patch artifacts ignored.")
    lines.append("4. Keep local reports/logs ignored.")
    lines.append("5. Decide whether Visio source banks are local-only or Git LFS-managed later.")
    lines.append("6. Before the next functional patch, either accept the coding-agent changes in a controlled commit or revert/quarantine them.")
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a non-destructive repository hygiene audit.")
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--out", type=Path, default=Path("_reports/repository_hygiene"))
    args = parser.parse_args()

    root = args.root.resolve()
    out = args.out.resolve()
    out.mkdir(parents=True, exist_ok=True)

    status = run_git(root, ["status", "--short"])
    diff_stat = run_git(root, ["diff", "--stat"])
    diff_name_status = run_git(root, ["diff", "--name-status"])
    untracked = run_git(root, ["ls-files", "--others", "--exclude-standard"])
    ignored = run_git(root, ["status", "--short", "--ignored"])
    head = run_git(root, ["log", "-1", "--oneline"])

    status_items = parse_short_status(status["stdout"])
    summary = summarize(status_items)

    payload = {
        "root": str(root),
        "head": head,
        "status": status,
        "status_items": status_items,
        "summary_by_class": summary,
        "diff_stat": diff_stat,
        "diff_name_status": diff_name_status,
        "untracked_excluding_ignored": untracked,
        "status_with_ignored": ignored,
    }

    (out / "repository_hygiene_audit.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    write_markdown(
        out / "README.md",
        status_items=status_items,
        summary=summary,
        diff_stat=diff_stat["stdout"],
        head=head["stdout"],
    )

    print(json.dumps({"out": str(out), "summary_by_class": summary}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())