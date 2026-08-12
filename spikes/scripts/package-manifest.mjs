import { createHash } from "node:crypto";
import { readFile, stat } from "node:fs/promises";
import path from "node:path";

function isInside(root, candidate) {
  const relative = path.relative(root, candidate);
  return relative === "" || (!relative.startsWith(`..${path.sep}`) && relative !== ".." && !path.isAbsolute(relative));
}

export async function loadVerifiedPackageManifest(candidate, command, args) {
  const configured = process.env.SPIKE_PACKAGE_MANIFEST;
  const required = process.env.SPIKE_REQUIRE_PACKAGE_MANIFEST === "1";
  if (!configured) {
    if (required) throw new Error(`${candidate} package manifest is required`);
    return null;
  }

  const manifestPath = path.resolve(configured);
  const manifest = JSON.parse(await readFile(manifestPath, "utf8"));
  if (manifest.protocol !== "electroscheme-candidate-package/1") {
    throw new Error(`${candidate} package manifest protocol is ${manifest.protocol ?? "missing"}`);
  }
  if (manifest.candidate !== candidate) {
    throw new Error(`${candidate} package manifest belongs to ${manifest.candidate ?? "unknown"}`);
  }
  if (manifest.artifact_layout_round_trip_verified !== true) {
    throw new Error(`${candidate} package archive round trip is not verified`);
  }
  for (const field of ["package_root", "archive_path", "archive_sha256", "unpacked_tree_sha256"]) {
    if (typeof manifest[field] !== "string" || manifest[field].length === 0) {
      throw new Error(`${candidate} package manifest field ${field} is missing`);
    }
  }
  if (!/^[0-9a-f]{64}$/.test(manifest.archive_sha256) || !/^[0-9a-f]{64}$/.test(manifest.unpacked_tree_sha256)) {
    throw new Error(`${candidate} package manifest contains an invalid SHA-256`);
  }

  const packageRoot = path.resolve(manifest.package_root);
  const archivePath = path.resolve(manifest.archive_path);
  const packageStats = await stat(packageRoot);
  const archiveStats = await stat(archivePath);
  if (!packageStats.isDirectory()) throw new Error(`${candidate} restored package root is not a directory`);
  if (!archiveStats.isFile()) throw new Error(`${candidate} portable package archive is not a file`);
  const actualArchiveSha256 = createHash("sha256").update(await readFile(archivePath)).digest("hex");
  if (actualArchiveSha256 !== manifest.archive_sha256) {
    throw new Error(`${candidate} package archive SHA-256 does not match its manifest`);
  }

  const launchTokens = [command, ...args]
    .filter(token => typeof token === "string" && token.length > 0 && !token.startsWith("-"))
    .map(token => path.resolve(token));
  const launchedFromVerifiedPackageRoot = launchTokens.some(token => isInside(packageRoot, token));
  if (!launchedFromVerifiedPackageRoot) {
    throw new Error(`${candidate} launch command does not reference restored package root ${packageRoot}`);
  }

  return {
    manifest_path: path.relative(process.cwd(), manifestPath) || path.basename(manifestPath),
    package_root: manifest.package_root,
    archive_path: manifest.archive_path,
    archive_sha256: manifest.archive_sha256,
    archive_size_bytes: manifest.archive_size_bytes,
    unpacked_tree_sha256: manifest.unpacked_tree_sha256,
    unpacked_size_bytes: manifest.unpacked_size_bytes,
    unpacked_file_count: manifest.unpacked_file_count,
    artifact_layout_round_trip_verified: true,
    launched_from_verified_package_root: true
  };
}
