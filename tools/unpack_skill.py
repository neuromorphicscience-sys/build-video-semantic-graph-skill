#!/usr/bin/env python3
"""Extract the complete source tree from the installable .skill archive."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import zipfile

EXPECTED_SHA256 = "45defd220e6ebfae001fefffe991137227561ff7bed27bfd996a1174bd3566f8"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def safe_extract(archive: zipfile.ZipFile, destination: Path) -> None:
    destination = destination.resolve()
    for member in archive.infolist():
        target = (destination / member.filename).resolve()
        if destination not in target.parents and target != destination:
            raise RuntimeError(f"Unsafe archive member: {member.filename}")
    archive.extractall(destination)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--package",
        type=Path,
        default=Path(__file__).resolve().parents[1]
        / "dist"
        / "build-video-semantic-graph.skill",
    )
    parser.add_argument("--output", type=Path, default=Path("unpacked"))
    parser.add_argument("--skip-hash-check", action="store_true")
    args = parser.parse_args()

    package = args.package.resolve()
    if not package.is_file():
        parser.error(f"Package not found: {package}")

    actual = sha256(package)
    if not args.skip_hash_check and actual != EXPECTED_SHA256:
        raise SystemExit(
            "Package SHA-256 mismatch:\n"
            f"  expected: {EXPECTED_SHA256}\n"
            f"  actual:   {actual}"
        )

    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(package) as archive:
        safe_extract(archive, output)

    print(f"Extracted {package.name} to {output}")
    print(f"SHA-256: {actual}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
