#!/usr/bin/env python3
"""Capture visual review pages with an installed headless Edge/Chrome browser."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
from pathlib import Path
from typing import Any


def candidate_browsers() -> list[Path]:
    names = ["msedge", "msedge.exe", "chrome", "chrome.exe", "chromium", "chromium.exe"]
    found: list[Path] = []
    for name in names:
        resolved = shutil.which(name)
        if resolved:
            found.append(Path(resolved))

    env_candidates = [
        os.environ.get("ProgramFiles", "") + r"\Microsoft\Edge\Application\msedge.exe",
        os.environ.get("ProgramFiles(x86)", "") + r"\Microsoft\Edge\Application\msedge.exe",
        os.environ.get("LocalAppData", "") + r"\Microsoft\Edge\Application\msedge.exe",
        os.environ.get("ProgramFiles", "") + r"\Google\Chrome\Application\chrome.exe",
        os.environ.get("ProgramFiles(x86)", "") + r"\Google\Chrome\Application\chrome.exe",
        os.environ.get("LocalAppData", "") + r"\Google\Chrome\Application\chrome.exe",
    ]
    for value in env_candidates:
        path = Path(value)
        if value and path.exists():
            found.append(path)

    unique: list[Path] = []
    seen = set()
    for path in found:
        key = str(path).lower()
        if key not in seen and path.exists():
            unique.append(path)
            seen.add(key)
    return unique


def run_capture(browser: Path, url: str, out_path: Path, window_size: str) -> dict[str, Any]:
    out_path.parent.mkdir(parents=True, exist_ok=True)

    attempts = [
        ["--headless=new", "--disable-gpu", "--hide-scrollbars", f"--window-size={window_size}", f"--screenshot={out_path}", url],
        ["--headless", "--disable-gpu", "--hide-scrollbars", f"--window-size={window_size}", f"--screenshot={out_path}", url],
    ]

    last: dict[str, Any] | None = None
    for args in attempts:
        proc = subprocess.run([str(browser), *args], capture_output=True, text=True)
        last = {
            "browser": str(browser),
            "url": url,
            "out": str(out_path),
            "args": args,
            "returncode": proc.returncode,
            "stdout": proc.stdout.strip(),
            "stderr": proc.stderr.strip(),
            "exists": out_path.exists(),
            "size_bytes": out_path.stat().st_size if out_path.exists() else 0,
        }
        if proc.returncode == 0 and out_path.exists() and out_path.stat().st_size > 0:
            return last
    assert last is not None
    return last


def main() -> int:
    parser = argparse.ArgumentParser(description="Capture visual review HTML pages.")
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument("--visual-dir", type=Path, default=Path("visual_checks/parametric_busbar"))
    parser.add_argument("--out", type=Path, default=Path("_reports/visual_review_browser_captures"))
    parser.add_argument("--window-size", default="1400,1000")
    args = parser.parse_args()

    repo_root = args.repo_root.resolve()
    visual_dir = args.visual_dir if args.visual_dir.is_absolute() else repo_root / args.visual_dir
    out_dir = args.out if args.out.is_absolute() else repo_root / args.out

    browsers = candidate_browsers()
    if not browsers:
        result = {
            "status": "browser_not_found",
            "captures": [],
            "message": "No Edge/Chrome/Chromium executable found.",
        }
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "capture_manifest.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 2

    browser = browsers[0]
    pages = [
        ("index", visual_dir / "index.html"),
        ("interactive", visual_dir / "interactive.html"),
    ]

    captures: list[dict[str, Any]] = []
    for stem, page in pages:
        if not page.exists():
            captures.append({"page": str(page), "status": "missing"})
            continue
        captures.append(run_capture(browser, page.resolve().as_uri(), out_dir / f"{stem}.png", args.window_size))

    result = {
        "status": "ok" if all(item.get("exists") for item in captures if item.get("status") != "missing") else "partial",
        "browser": str(browser),
        "out_dir": str(out_dir),
        "captures": captures,
    }
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "capture_manifest.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] == "ok" else 1


if __name__ == "__main__":
    raise SystemExit(main())