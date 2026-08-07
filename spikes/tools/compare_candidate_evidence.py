#!/usr/bin/env python3
"""Validate Windows/Linux desktop candidate artifacts and emit factual comparison evidence."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

CANDIDATES = ("electron", "tauri")
PLATFORMS = ("windows", "linux")
LOGICAL_HASH_FIELDS = ("canonical_json_sha256", "clipboard_sha256", "pdf_sha256")
HEX_SHA256 = re.compile(r"^[0-9a-f]{64}$")
EXPECTED_ELECTRON_WINDOWS_FAILURE = "native_startup_failure"
EXPECTED_ELECTRON_WINDOWS_EXIT = "0x80000003"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def load_one(root: Path, name: str, *, required: bool = True) -> tuple[Path | None, dict[str, Any] | None]:
    matches = sorted(root.rglob(name))
    if not matches and not required:
        return None, None
    if len(matches) != 1:
        raise RuntimeError(f"expected exactly one {name} below {root}, found {len(matches)}")
    return matches[0], json.loads(matches[0].read_text(encoding="utf-8"))


def require_sha256(value: Any, label: str) -> str:
    require(isinstance(value, str) and HEX_SHA256.fullmatch(value) is not None,
            f"{label}: valid lowercase SHA-256 is required")
    return value


def package_evidence(data: dict[str, Any]) -> dict[str, Any]:
    package = data.get("package_evidence") or data.get("harness", {}).get("package_evidence", {})
    require(package.get("artifact_layout_round_trip_verified") is True,
            "scenario/runtime did not verify archive round trip")
    require(package.get("launched_from_verified_package_root") is True,
            "scenario/runtime did not launch from restored package root")
    return package


def validate_success_scenario(data: dict[str, Any], candidate: str, platform_name: str) -> dict[str, Any]:
    prefix = f"{platform_name}/{candidate}"
    require(data.get("candidate") == candidate, f"{prefix}: scenario candidate mismatch")
    require(data.get("status") == "ok", f"{prefix}: scenario status is not ok")
    checks = data.get("checks")
    require(isinstance(checks, dict) and checks, f"{prefix}: scenario checks missing")
    failed = [name for name, value in checks.items() if value is not True]
    require(not failed, f"{prefix}: failed checks: {', '.join(failed)}")
    package_evidence(data)
    hashes = data.get("hashes")
    require(isinstance(hashes, dict), f"{prefix}: logical output hashes missing")
    logical = {field: require_sha256(hashes.get(field), f"{prefix}/{field}") for field in LOGICAL_HASH_FIELDS}
    tools = data.get("tool_results")
    require(isinstance(tools, dict), f"{prefix}: Visio tool results missing")
    for operation in ("vsdx", "vssx", "generated", "generatedInspection"):
        result = tools.get(operation)
        require(isinstance(result, dict), f"{prefix}: {operation} tool result missing")
        require(result.get("status") == "ok", f"{prefix}: {operation} status is not ok")
    controlled_vsdx = require_sha256(tools["vsdx"].get("sha256"), f"{prefix}/controlled VSDX")
    controlled_vssx = require_sha256(tools["vssx"].get("sha256"), f"{prefix}/controlled VSSX")
    generated = require_sha256(tools["generated"].get("sha256"), f"{prefix}/generated VSDX")
    generated_inspection = require_sha256(tools["generatedInspection"].get("sha256"), f"{prefix}/generated VSDX inspection")
    require(generated == generated_inspection, f"{prefix}: generated VSDX changed between generation and package inspection")
    return {
        "logical_output_sha256": logical,
        "controlled_vsdx_sha256": controlled_vsdx,
        "controlled_vssx_sha256": controlled_vssx,
        "generated_vsdx_sha256": generated,
    }


def validate_expected_failure(data: dict[str, Any], candidate: str, platform_name: str) -> dict[str, Any]:
    prefix = f"{platform_name}/{candidate}"
    require(candidate == "electron" and platform_name == "windows",
            f"{prefix}: candidate failure is not an admitted comparison outcome")
    require(data.get("candidate") == candidate, f"{prefix}: failure candidate mismatch")
    require(data.get("status") == "failed", f"{prefix}: failure evidence must have failed status")
    require(data.get("failure_class") == EXPECTED_ELECTRON_WINDOWS_FAILURE,
            f"{prefix}: unexpected failure class {data.get('failure_class')}")
    require(data.get("exit_code_hex") == EXPECTED_ELECTRON_WINDOWS_EXIT,
            f"{prefix}: expected {EXPECTED_ELECTRON_WINDOWS_EXIT}, got {data.get('exit_code_hex')}")
    require(data.get("secure_runtime_required") is True,
            f"{prefix}: secure-runtime requirement must remain true")
    package_evidence(data)
    return {
        "failure_class": data["failure_class"],
        "exit_code_decimal": data.get("exit_code_decimal"),
        "exit_code_hex": data["exit_code_hex"],
        "error": data.get("error"),
    }


def validate_runtime(data: dict[str, Any], candidate: str, platform_name: str) -> None:
    prefix = f"{platform_name}/{candidate}"
    require(data.get("candidate") == candidate, f"{prefix}: runtime candidate mismatch")
    require(float(data.get("startup_to_renderer_ready_ms", 0)) > 0, f"{prefix}: startup measurement missing")
    require(int(data.get("idle_process_tree_rss_bytes", 0)) > 0, f"{prefix}: RSS measurement missing")
    require(int(data.get("measurement_root_pid", 0)) > 0, f"{prefix}: candidate root PID missing")
    package_evidence(data)


def validate_package_sizes(package_sizes: dict[str, Any], measurements: dict[str, Any], platform_name: str) -> None:
    prefix = f"{platform_name}/package sizes"
    require(package_sizes.get("protocol") == "electroscheme-package-sizes/1", f"{prefix}: unsupported protocol")
    for field in ("workflow_run_id", "exact_head", "npm_lock_sha256", "cargo_lock_sha256"):
        require(str(package_sizes.get(field)) == str(measurements.get(field)), f"{prefix}: {field} does not match measurements")
    packages = package_sizes.get("packages")
    manifests = measurements.get("package_manifests")
    require(isinstance(packages, dict), f"{prefix}: packages missing")
    require(isinstance(manifests, dict), f"{platform_name}: package manifests missing")
    for candidate in CANDIDATES:
        package = packages.get(candidate)
        manifest = manifests.get(candidate)
        require(isinstance(package, dict) and isinstance(manifest, dict), f"{prefix}/{candidate}: package evidence missing")
        expected = {key: manifest.get(key) for key in (
            "archive_path", "archive_sha256", "archive_size_bytes", "package_root",
            "unpacked_tree_sha256", "unpacked_size_bytes", "unpacked_file_count",
        )}
        require(package == expected, f"{prefix}/{candidate}: dedicated JSON differs from package manifest")


def platform_snapshot(root: Path, platform_name: str) -> dict[str, Any]:
    _, measurements = load_one(root, f"measurements-{platform_name}.json")
    _, package_sizes = load_one(root, f"package-sizes-{platform_name}.json")
    assert measurements is not None and package_sizes is not None
    validate_package_sizes(package_sizes, measurements, platform_name)
    manifests = measurements.get("package_manifests")
    require(isinstance(manifests, dict), f"{platform_name}: package manifests missing")
    for candidate in CANDIDATES:
        manifest = manifests.get(candidate, {})
        require(manifest.get("candidate") == candidate, f"{platform_name}/{candidate}: package manifest mismatch")
        require(manifest.get("artifact_layout_round_trip_verified") is True,
                f"{platform_name}/{candidate}: package layout round trip not verified")
        require(int(manifest.get("archive_size_bytes", 0)) > 0, f"{platform_name}/{candidate}: archive size missing")
        require(int(manifest.get("unpacked_size_bytes", 0)) > 0, f"{platform_name}/{candidate}: unpacked size missing")
        require_sha256(manifest.get("archive_sha256"), f"{platform_name}/{candidate}/archive")
        require_sha256(manifest.get("unpacked_tree_sha256"), f"{platform_name}/{candidate}/unpacked tree")

    candidates: dict[str, Any] = {}
    passing_evidence: list[dict[str, Any]] = []
    for candidate in CANDIDATES:
        _, scenario = load_one(root, f"{candidate}-scenario-{platform_name}.json")
        assert scenario is not None
        if scenario.get("status") == "ok":
            evidence = validate_success_scenario(scenario, candidate, platform_name)
            passing_evidence.append(evidence)
            _, runtime = load_one(root, f"{candidate}-runtime-{platform_name}.json")
            assert runtime is not None
            validate_runtime(runtime, candidate, platform_name)
            candidates[candidate] = {"scenario": scenario, "runtime": runtime, "failure": None, "evidence": evidence}
        else:
            failure = validate_expected_failure(scenario, candidate, platform_name)
            _, runtime = load_one(root, f"{candidate}-runtime-{platform_name}.json", required=False)
            require(runtime is None, f"{platform_name}/{candidate}: runtime measurement must not exist after secure startup failure")
            candidates[candidate] = {"scenario": scenario, "runtime": None, "failure": failure, "evidence": None}

    require(candidates["tauri"]["scenario"].get("status") == "ok", f"{platform_name}/tauri: successful secure scenario is mandatory")
    if platform_name == "linux":
        require(candidates["electron"]["scenario"].get("status") == "ok", "linux/electron: successful scenario is mandatory")
    return {
        "measurements": measurements,
        "package_sizes": package_sizes,
        "candidates": candidates,
        "passing_evidence": passing_evidence,
    }


def one_equal_hash(values: list[str], label: str) -> str:
    require(values, f"{label}: no passing scenario evidence")
    unique = set(values)
    require(len(unique) == 1, f"{label} differs across passing candidate/platform scenarios: {sorted(unique)}")
    return unique.pop()


def mb(value: int | None) -> str:
    return "n/a" if value is None else f"{value / 1_000_000:.2f}"


def markdown(snapshot: dict[str, Any]) -> str:
    logical = snapshot["logical_output_sha256"]
    visio = snapshot["visio_sha256"]
    lines = [
        "# Automated desktop candidate comparison evidence", "",
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
        "- logical hashes are equal across every candidate/platform scenario that reached the secure renderer",
        "- Electron Windows secure packaged launch failure, when present, is negative comparison evidence and is never treated as a passing runtime",
        "- scope: single GitHub-hosted runner launch per candidate/platform; values are comparative evidence for this run, not universal benchmarks", "",
        "| Platform | Candidate | Archive MB | Unpacked MB | Startup ms | Process-tree RSS MB | Scenario | Restored artifact layout |",
        "|---|---:|---:|---:|---:|---:|---|---|",
    ]
    for platform_name in PLATFORMS:
        for candidate in CANDIDATES:
            item = snapshot["platforms"][platform_name]["candidates"][candidate]
            startup = item["startup_to_renderer_ready_ms"]
            rss = item["idle_process_tree_rss_bytes"]
            startup_text = "n/a" if startup is None else f"{startup:.2f}"
            lines.append(
                f"| {platform_name} | {candidate} | {mb(item['archive_size_bytes'])} | {mb(item['unpacked_size_bytes'])} | "
                f"{startup_text} | {mb(rss)} | {item['scenario_status']} | VERIFIED |"
            )
    lines += ["", "This generated table is measurement evidence only. It does not close native-dialog, drag/drop, print-driver or Microsoft Visio manual gates.", ""]
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
    exact_head, workflow_run_id = heads.pop(), runs.pop()
    if expected_head:
        require(exact_head == expected_head, f"artifact head {exact_head} does not match expected {expected_head}")
    if expected_run:
        require(workflow_run_id == expected_run, f"artifact run {workflow_run_id} does not match expected {expected_run}")

    evidence = [item for platform in platforms.values() for item in platform["passing_evidence"]]
    logical = {field: one_equal_hash([item["logical_output_sha256"][field] for item in evidence], field) for field in LOGICAL_HASH_FIELDS}
    visio = {field: one_equal_hash([item[field] for item in evidence], field) for field in (
        "controlled_vsdx_sha256", "controlled_vssx_sha256", "generated_vsdx_sha256")}
    result: dict[str, Any] = {
        "protocol": "electroscheme-desktop-comparison/2",
        "workflow_run_id": workflow_run_id,
        "exact_head": exact_head,
        "npm_lock_sha256": npm_locks.pop(),
        "cargo_lock_sha256": cargo_locks.pop(),
        "logical_output_sha256": logical,
        "visio_sha256": visio,
        "passing_scenarios_logical_equality_verified": True,
        "secure_runtime_failure_is_not_pass_evidence": True,
        "measurement_scope": "single GitHub-hosted runner launch per candidate/platform; factual for this exact run and not a universal benchmark",
        "platforms": {},
        "manual_gates": ["OWNER_OR_WINDOWS_VISIO_EVIDENCE_REQUIRED", "OWNER_OR_INTERACTIVE_RUNNER_EVIDENCE_REQUIRED"],
    }
    for platform_name in PLATFORMS:
        platform = platforms[platform_name]
        candidates: dict[str, Any] = {}
        for candidate in CANDIDATES:
            manifest = platform["measurements"]["package_manifests"][candidate]
            candidate_data = platform["candidates"][candidate]
            runtime = candidate_data["runtime"]
            failure = candidate_data["failure"]
            candidates[candidate] = {
                "archive_path": manifest["archive_path"],
                "archive_sha256": manifest["archive_sha256"],
                "archive_size_bytes": manifest["archive_size_bytes"],
                "package_root": manifest["package_root"],
                "unpacked_tree_sha256": manifest["unpacked_tree_sha256"],
                "unpacked_size_bytes": manifest["unpacked_size_bytes"],
                "startup_to_renderer_ready_ms": None if runtime is None else runtime["startup_to_renderer_ready_ms"],
                "idle_process_tree_rss_bytes": None if runtime is None else runtime["idle_process_tree_rss_bytes"],
                "scenario_status": "PASS" if failure is None else "FAIL_SECURE_NATIVE_STARTUP",
                "failure": failure,
                "artifact_layout_round_trip_verified": True,
                "launched_from_verified_package_root": True,
            }
        result["platforms"][platform_name] = {
            "artifact_name": platform["measurements"].get("artifact_name"),
            "runner_os": platform["measurements"].get("runner_os"),
            "runner_architecture": platform["measurements"].get("runner_architecture"),
            "package_size_json": platform["measurements"].get("package_size_json"),
            "toolchains": {key: platform["measurements"].get(key) for key in ("python", "node", "npm", "rustc", "cargo")},
            "candidates": candidates,
        }
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("artifact_root", type=Path)
    parser.add_argument("json_output", type=Path)
    parser.add_argument("markdown_output", type=Path)
    parser.add_argument("--expected-head")
    parser.add_argument("--expected-run")
    args = parser.parse_args()
    snapshot = build_snapshot(args.artifact_root, args.expected_head, args.expected_run)
    args.json_output.parent.mkdir(parents=True, exist_ok=True)
    args.markdown_output.parent.mkdir(parents=True, exist_ok=True)
    args.json_output.write_text(json.dumps(snapshot, indent=2) + "\n", encoding="utf-8")
    args.markdown_output.write_text(markdown(snapshot), encoding="utf-8")
    print(json.dumps(snapshot, indent=2))


if __name__ == "__main__":
    main()
