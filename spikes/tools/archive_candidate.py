#!/usr/bin/env python3
"""Create and verify a deterministic portable evidence archive for a candidate package."""
from __future__ import annotations

import argparse
import gzip
import hashlib
import io
import json
import os
from pathlib import Path
import shutil
import stat
import tarfile


def iter_entries(root: Path) -> list[Path]:
    return sorted(root.rglob("*"), key=lambda item: item.relative_to(root).as_posix())


def tree_digest(root: Path) -> tuple[str, int, int]:
    digest = hashlib.sha256()
    file_count = 0
    total_bytes = 0
    for item in iter_entries(root):
        relative = item.relative_to(root).as_posix()
        metadata = item.lstat()
        mode = stat.S_IMODE(metadata.st_mode)
        if item.is_symlink():
            kind = "symlink"
            payload = os.readlink(item).encode("utf-8")
        elif item.is_dir():
            kind = "directory"
            payload = b""
        elif item.is_file():
            kind = "file"
            payload = item.read_bytes()
            file_count += 1
            total_bytes += len(payload)
        else:
            raise RuntimeError(f"unsupported package entry: {item}")
        digest.update(f"{kind}\0{mode:o}\0{relative}\0{len(payload)}\0".encode("utf-8"))
        digest.update(payload)
    return digest.hexdigest(), file_count, total_bytes


def tar_bytes(root: Path) -> bytes:
    output = io.BytesIO()
    with tarfile.open(fileobj=output, mode="w", format=tarfile.PAX_FORMAT) as archive:
        root_info = tarfile.TarInfo(root.name)
        root_info.type = tarfile.DIRTYPE
        root_info.mode = stat.S_IMODE(root.stat().st_mode)
        root_info.mtime = 0
        root_info.uid = 0
        root_info.gid = 0
        root_info.uname = ""
        root_info.gname = ""
        archive.addfile(root_info)
        for item in iter_entries(root):
            relative = Path(root.name) / item.relative_to(root)
            metadata = item.lstat()
            info = tarfile.TarInfo(relative.as_posix())
            info.mode = stat.S_IMODE(metadata.st_mode)
            info.mtime = 0
            info.uid = 0
            info.gid = 0
            info.uname = ""
            info.gname = ""
            if item.is_symlink():
                info.type = tarfile.SYMTYPE
                info.linkname = os.readlink(item)
                archive.addfile(info)
            elif item.is_dir():
                info.type = tarfile.DIRTYPE
                archive.addfile(info)
            elif item.is_file():
                data = item.read_bytes()
                info.type = tarfile.REGTYPE
                info.size = len(data)
                archive.addfile(info, io.BytesIO(data))
            else:
                raise RuntimeError(f"unsupported package entry: {item}")
    return output.getvalue()


def safe_extract(archive_path: Path, destination: Path) -> None:
    with tarfile.open(archive_path, mode="r:gz") as archive:
        destination_resolved = destination.resolve()
        for member in archive.getmembers():
            target = (destination / member.name).resolve()
            if target != destination_resolved and destination_resolved not in target.parents:
                raise RuntimeError(f"unsafe archive member: {member.name}")
        archive.extractall(destination, filter="data")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("candidate")
    parser.add_argument("package_root", type=Path)
    parser.add_argument("archive_path", type=Path)
    parser.add_argument("manifest_path", type=Path)
    parser.add_argument("--base-root", type=Path, default=Path.cwd())
    args = parser.parse_args()

    package_root = args.package_root.resolve()
    archive_path = args.archive_path.resolve()
    manifest_path = args.manifest_path.resolve()
    base_root = args.base_root.resolve()
    if not package_root.is_dir():
        raise RuntimeError(f"candidate package root does not exist: {package_root}")

    before_digest, file_count, unpacked_bytes = tree_digest(package_root)
    archive_path.parent.mkdir(parents=True, exist_ok=True)
    tar_payload = tar_bytes(package_root)
    archive_path.write_bytes(gzip.compress(tar_payload, compresslevel=9, mtime=0))
    archive_sha256 = hashlib.sha256(archive_path.read_bytes()).hexdigest()

    parent = package_root.parent
    shutil.rmtree(package_root)
    safe_extract(archive_path, parent)
    after_digest, after_file_count, after_unpacked_bytes = tree_digest(package_root)
    if (before_digest, file_count, unpacked_bytes) != (after_digest, after_file_count, after_unpacked_bytes):
        raise RuntimeError("candidate package changed after deterministic archive extraction")

    manifest = {
        "protocol": "electroscheme-candidate-package/1",
        "candidate": args.candidate,
        "package_root": package_root.relative_to(base_root).as_posix(),
        "archive_path": archive_path.relative_to(base_root).as_posix(),
        "archive_format": "deterministic-tar-gzip",
        "archive_sha256": archive_sha256,
        "archive_size_bytes": archive_path.stat().st_size,
        "unpacked_tree_sha256": after_digest,
        "unpacked_size_bytes": after_unpacked_bytes,
        "unpacked_file_count": after_file_count,
        "artifact_layout_round_trip_verified": True,
        "archive_metadata": "sorted paths; uid/gid/mtime normalized; original entry modes and symlinks preserved",
    }
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
