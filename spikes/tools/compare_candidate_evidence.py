#!/usr/bin/env python3
"""Validate Windows/Linux candidate artifacts and emit one factual comparison snapshot."""
from __future__ import annotations

import argparse
import json
import os
import re
from pathlib import Path
from typing import Any

CANDIDATES = ("electron", "tauri")
PLATFORMS = ("windows", "linux")
LOGICAL_HASH_FIELDS = (
    "canonical_json_sha256",
    "clipboard_sha256",
    "pdf_sha256",
)
HEX_SHA256 = re.compile(r"^[0-9a-f]{64}$")


def load_one(root: Path, name: str) -> tuple[Path, dict[str, Any]]:
    matches = sorted(root.rglob(name))
    if len(matches) != 1:
        raise RuntimeError(f"expected exactly one {name} below {root}, found {len(matches)}")
    return matches[0], json.loads(matches[0].read_text(encoding="utf-8"))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def require_sha256(value: Any, label: str) -> str:
    require(isinstance(value, str) and HEX_SHA256.fullmatch(value) is not None,
            f"{label}: valid lowercase SHA-256 is required")
    return value


def validate_scenario(data: dict[str, Any], candidate: str, platform_name: str) -> dict[str, Any]:
    prefix = f"{platform_name}/{candidate}"
    require(data.get("candidate") == candidate, f"{prefix}: scenario candidate mismatch")
    require(data.get("status") == "ok", f"{prefix}: scenario status is not ok")
    checks = data.get("checks")
    require(isinstance(checks, dict) and checks, f"{prefix}: scenario checks missing")
    failed = [name for name, value in checks.items() if value is not True]
    require(not failed, f"{prefix}: failed checks: {', '.join(failed)}")
    package = data.get("harness", {}).get("package_evidence", {})
    require(package.get("artifact_layout_round_trip_verified") is True,
            f"{prefix}: scenario did not verify archive round trip")
    require(package.get("launched_from_verified_package_root") is True,
            f"{prefix}: scenario did not launch from restored package root")

    hashes = data.get("hashes")
    require(isinstance(hashes, dict), f"{prefix}: logical output hashes missing")
    logical = {
        field: require_sha256(hashes.get(field), f"{prefix}/{field}")
        for field in LOGICAL_HASH_FIELDS
    }

    tools = data.get("tool_results")
    require(isinstance(tools, dict), f"{prefix}: Visio tool results missing")
    for operation in ("vsdx", "vssx", "generated", "generatedInspection"):
        result = tools.get(operation)
        require(isinstance(result, dict), f"{prefix}: {operation} tool result missing")
        require(result.get("status") == "ok", f"{prefix}: {operation} status is not ok")
    controlled_vsdx = require_sha256(tools["vsdx"].get("sha256"), f"{prefix}/controlled VSDX")
    controlled_vssx = require_sha256(tools["vssx"].get("sha256"), f"{prefix}/controlled VSSX")
    generated = require_sha256(tools["generated"].get("sha256"), f"{prefix}/generated VSDX")
    generated_inspection = require_sha256(
        tools["generatedInspection"].get("sha256"),
        f"{prefix}/generated VSDX inspection",
    )
    require(generated == generated_inspection,
            f"{prefix}: generated VSDX changed between generation and package inspection")

    return {
        "logical_output_sha256": logical,
        "controlled_vsdx_sha256": controlled_vsdx,
        "controlled_vssx_sha256": controlled_vssx,
        "generated_vsdx_sha256": generated,
    }


def validate_runtime(data: dict[str, Any], candidate: str, platform_name: str) -> None:
    prefix = f"{platform_name}/{candidate}"
    require(data.get("candidate") == candidate, f"{prefix}: runtime candidate mismatch")
    require(float(data.get("startup_to_renderer_ready_ms", 0)) > 0,
            f"{prefix}: startup measurement missing")
    require(int(data.get("idle_process_tree_rss_bytes", 0)) > 0,
            f"{prefix}: RSS measurement missing")
    require(int(data.get("measurement_root_pid", 0)) > 0,
            f"{prefix}: candidate root PID missing")
    package = data.get("package_evidence", {})
    require(package.get("artifact_layout_round_trip_verified") is True,
            f"{prefix}: runtime did not verify archive round trip")
    require(package.get("launched_from_verified_package_root") is True,
            f"{prefix}: runtime did not launch from restored package root")


def validate_package_sizes(
    package_sizes: dict[str, Any],
    measurements: dict[str, Any],
    platform_name: str,
) -> None:
    prefix = f"{platform_name}/package sizes"
    require(package_sizes.get("protocol") == "electroscheme-package-sizes/1",
            f"{prefix}: unsupported protocol")
    for field in ("workflow_run_id", "exact_head", "npm_lock_sha256", "cargo_lock_sha256"):
        require(str(package_sizes.get(field)) == str(measurements.get(field)),
                f"{prefix}: {field} does not match measurements")
    packages = package_sizes.get("packages")
    require(isinstance(packages, dict), f"{prefix}: packages missing")
    manifests = measurements.get("package_manifests")
    require(isinstance(manifests, dict), f"{platform_name}: package manifests missing")
    for candidate in CANDIDATES:
        package = packages.get(candidate)
        manifest = manifests.get(candidate)
        require(isinstance(package, dict) and isinstance(manifest, dict),
                f"{prefix}/{candidate}: package evidence missing")
        expected = {
            "archive_path": manifest.get("archive_path"),
            "archive_sha256": manifest.get("archive_sha256"),
            "archive_size_bytes": manifest.get("archive_size_bytes"),
            "package_root": manifest.get("package_root"),
            "unpacked_tree_sha256": manifest.get("unpacked_tree_sha256"),
            "unpacked_size_bytes": manifest.get("unpacked_size_bytes"),
            "unpacked_file_count": manifest.get("unpacked_file_count"),
        }
        require(package == expected, f"{prefix}/{candidate}: dedicated JSON differs from package manifest")


def platform_snapshot(root: Path, platform_name: str) -> dict[str, Any]:
    _, measurements = load_one(root, f"measurements-{platform_name}.json")
    _, package_sizes = load_one(root, f"package-sizes-{platform_name}.json")
    validate_package_sizes(package_sizes, measurements, platform_name)
    scenarios: dict[str, Any] = {}
    scenario_evidence: dict[str, Any] = {}
    runtimes: dict[str, Any] = {}
    for candidate in CANDIDATES:
        _, scenario = load_one(root, f"{candidate}-scenario-{platform_name}.json")
        _, runtime = load_one(root, f"{candidate}-runtime-{platform_name}.json")
        scenario_evidence[candidate] = validate_scenario(scenario, candidate, platform_name)
        validate_runtime(runtime, candidate, platform_name)
        scenarios[candidate] = scenario
        runtimes[candidate] = runtime

    manifests = measurements.get("package_manifests")
    require(isinstance(manifests, dict), f"{platform_name}: package manifests missing")
    for candidate in CANDIDATES:
        manifest = manifests.get(candidate, {})
        require(manifest.get("candidate") == candidate, f"{platform_name}/{candidate}: package manifest mismatch")
        require(manifest.get("artifact_layout_round_trip_verified") is True,
                f"{platform_name}/{candidate}: package layout round trip not verified")
        require(int(manifest.get("archive_size_bytes", 0)) > 0,
                f"{platform_name}/{candidate}: archive size missing")
        require(int(manifest.get("unpacked_size_bytes", 0)) > 0,
                f"{platform_name}/{candidate}: unpacked size missing")
        require_sha256(manifest.get("archive_sha256"), f"{platform_name}/{candidate}/archive")
        require_sha256(manifest.get("unpacked_tree_sha256"), f"{platform_name}/{candidate}/unpacked tree")

    return {
        "measurements": measurements,
        "package_sizes": package_sizes,
        "scenarios": scenarios,
        "scenario_evidence": scenario_evidence,
        "runtimes": runtimes,
    }


def one_equal_hash(values: list[str], label: str) -> str:
    unique = set(values)
    require(len(unique) == 1, f"{label} differs across platform/candidate scenarios: {sorted(unique)}")
    return unique.pop()


def mb(value: int) -> str:
    return f"{value / 1_000_000:.2f}"


def markdown(snapshot: dict[str, Any]) -> str:
    logical = snapshot["logical_output_sha256"]
    visio = snapshot["visio_sha256"]
    lines = [
        "# Automated desktop candidate comparison evidence",
        "",
        f"- workflow run: `{snapshot['workflow_run_id']}`",
        f"- exact head: `{snapshot['exact_head']}`",
        f"- npm lock SHA-256: `{snapshot['npm_lock_sha256']}`",
        f"- Cargo lock SHA-256: `{snapshot['cargo_lock_sha256']}`",
        f"- canonical JSON SHA-256: `{logical['canonical_json_sha256']}`",
        f"- structured clipboard SHA-256: `{logical['clipboard_sha256']}`",
        f"- deterministic PDF SHA-256: `{logical['pdf_sha256']}`",
        f"- controlled VSDX SHA-256: `{visio['controlled_vsdx_sha256']}`",
        f"- controlled VSSX SHA-256: `{visio['controlled_vssx_sha256']}`",
        f"- generated VSDX SHA-256: `{visio['generated_vsdx_sha256']}`",
        "- logical hashes above are equal across Electron/Tauri and Windows/Linux scenarios",
        "- scope: single GitHub-hosted runner launch per candidate/platform; values are comparative evidence for this run, not universal benchmarks",
        "",
        "| Platform | Candidate | Archive MB | Unpacked MB | Startup ms | Process-tree RSS MB | Scenario | Restored artifact layout |",
        "|---|---:|---:|---:|---:|---:|---|---|",
    ]
    for platform_name in PLATFORMS:
        for candidate in CANDIDATES:
            item = snapshot["platforms"][platform_name]["candidates"][candidate]
            lines.append(
                f"| {platform_name} | {candidate} | {mb(item['archive_size_bytes'])} | "
                f"{mb(item['unpacked_size_bytes'])} | {item['startup_to_renderer_ready_ms']:.2f} | "
                f"{mb(item['idle_process_tree_rss_bytes'])} | PASS | VERIFIED |"
            )
    lines.extend([
        "",
        "This generated table is measurement evidence only. It does not decide the desktop host and does not close native-dialog, drag/drop, print-driver or Microsoft Visio manual gates.",
        "",
    ])
    return "\n".join(lines)


def build_snapshot(root: Path, expected_head: str | None = None, expected_run: str | None = None) -> dict[str, Any]:
    platforms = {name: platform_snapshot(root, name) for name in PLATFORMS}
    measurements = [platforms[name]["measurements"] for name in PLATFORMS]
    heads = {str(item.get("exact_head")) for item in measurements}
    runs = {str(item.get("workflow_run_id")) for item in measurements}
    npm_locks = {str(item.get("npm_lock_sha256")) for item in measurements}
    cargo_locks = {str(item.get("cargo_lock_sha256")) for item in measurements}
    require(len(heads) == 1 and "None" not in heads, "platform artifacts do not share one exact head")
    require(len(runs) == 1 and "None" not in runs, "platform artifacts do not share one workflow run")
    require(len(npm_locks) == 1 and "None" not in npm_locks, "platform artifacts use different npm locks")
    require(len(cargo_locks) == 1 and "None" not in cargo_locks, "platform artifacts use different Cargo locks")
    exact_head = heads.pop()
    workflow_run_id = runs.pop()
    if expected_head:
        require(exact_head == expected_head, f"artifact head {exact_head} does not match expected {expected_head}")
    if expected_run:
        require(workflow_run_id == expected_run, f"artifact run {workflow_run_id} does not match expected {expected_run}")

    evidence = [
        platforms[platform_name]["scenario_evidence"][candidate]
        for platform_name in PLATFORMS
        for candidate in CANDIDATES
    ]
    logical_output_sha256 = {
        field: one_equal_hash(
            [item["logical_output_sha256"][field] for item in evidence],
            field,
        )
        for field in LOGICAL_HASH_FIELDS
    }
    visio_sha256 = {
        field: one_equal_hash([item[field] for item in evidence], field)
        for field in (
            "controlled_vsdx_sha256",
            "controlled_vssx_sha256",
            "generated_vsdx_sha256",
        )
    }

    result: dict[str, Any] = {
        "protocol": "electroscheme-desktop-comparison/1",
        "workflow_run_id": workflow_run_id,
        "exact_head": exact_head,
        "npm_lock_sha256": npm_locks.pop(),
        "cargo_lock_sha256": cargo_locks.pop(),
        "logical_output_sha256": logical_output_sha256,
        "visio_sha256": visio_sha256,
        "cross_candidate_platform_logical_equality_verified": True,
        "measurement_scope": "single GitHub-hosted runner launch per candidate/platform; factual for this exact run and not a universal benchmark",
        "platforms": {},
        "manual_gates": [
            "OWNER_OR_WINDOWS_VISIO_EVIDENCE_REQUIRED",
            "OWNER_OR_INTERACTIVE_RUNNER_EVIDENCE_REQUIRED",
        ],
    }
    for platform_name in PLATFORMS:
        platform_data = platforms[platform_name]
        candidates: dict[str, Any] = {}
        for candidate in CANDIDATES:
            manifest = platform_data["measurements"]["package_manifests"][candidate]
            runtime = platform_data["runtimes"][candidate]
            candidates[candidate] = {
                "archive_path": manifest["archive_path"],
                "archive_sha256": manifest["archive_sha256"],
                "archive_size_bytes": manifest["archive_size_bytes"],
                "package_root": manifest["package_root"],
                "unpacked_tree_sha256": manifest["unpacked_tree_sha256"],
                "unpacked_size_bytes": manifest["unpacked_size_bytes"],
                "startup_to_renderer_ready_ms": runtime["startup_to_renderer_ready_ms"],
                "idle_process_tree_rss_bytes": runtime["idle_process_tree_rss_bytes"],
                "scenario_status": "ok",
                "artifact_layout_round_trip_verified": True,
                "launched_from_verified_package_root": True,
            }
        result["platforms"][platform_name] = {
            "artifact_name": platform_data["measurements"].get("artifact_name"),
            "runner_os": platform_data["measurements"].get("runner_os"),
            "runner_architecture": platform_data["measurements"].get("runner_architecture"),
            "package_size_json": platform_data["measurements"].get("package_size_json"),
            "toolchains": {
                key: platform_data["measurements"].get(key)
                for key in ("python", "node", "npm", "rustc", "cargo")
            },
            "candidates": candidates,
        }
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("artifact_root", type=Path)
    parser.add_argument("json_output", type=Path)
    parser.add_argument("markdown_output", type=Path)
    parser.add_argument("--expected-head", default=os.environ.get("SPIKE_EXACT_HEAD") or os.environ.get("GITHUB_SHA"))
    parser.add_argument("--expected-run", default=os.environ.get("GITHUB_RUN_ID"))
    args = parser.parse_args()
    snapshot = build_snapshot(args.artifact_root.resolve(), args.expected_head, args.expected_run)
    args.json_output.parent.mkdir(parents=True, exist_ok=True)
    args.markdown_output.parent.mkdir(parents=True, exist_ok=True)
    args.json_output.write_text(json.dumps(snapshot, indent=2) + "\n", encoding="utf-8")
    args.markdown_output.write_text(markdown(snapshot), encoding="utf-8")
    print(json.dumps(snapshot, indent=2))


if __name__ == "__main__":
    main()
