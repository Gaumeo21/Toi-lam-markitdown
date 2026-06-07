#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2024-present Adam Fourney <adamfo@microsoft.com>
#
# SPDX-License-Identifier: MIT
"""Build the MarkItDown Local Portable Windows ZIP artifact.

This script is intended to be run on Windows x64 for release builds. It can copy a
pre-supplied portable Python runtime via --python-runtime-dir, or on Windows it can
stage the current Python installation as the internal runtime.
"""

from __future__ import annotations

import argparse
import hashlib
import os
import platform
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
LOCAL_APP_ROOT = REPO_ROOT / "packages" / "markitdown-local-app"
LOCAL_APP_SRC = LOCAL_APP_ROOT / "src" / "markitdown_local_app"
PORTABLE_DIR = LOCAL_APP_ROOT / "portable"
DIST_DIR = REPO_ROOT / "dist"
STAGING_DIR = DIST_DIR / "markitdown-local"
ZIP_PATH = DIST_DIR / "markitdown-local-portable-windows-x64.zip"

LOCAL_MARKITDOWN_REQUIREMENT = str(
    REPO_ROOT / "packages" / "markitdown"
) + "[docx,pdf,pptx,xls,xlsx]"
DEPENDENCY_REQUIREMENTS = [
    "streamlit>=1.36",
    LOCAL_MARKITDOWN_REQUIREMENT,
]
FORBIDDEN_PACKAGES = {
    "pydub",
    "speechrecognition",
    "youtube_transcript_api",
    "youtube-transcript-api",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--python-runtime-dir",
        type=Path,
        default=os.environ.get("MARKITDOWN_PORTABLE_PYTHON_DIR"),
        help=(
            "Directory containing a Windows portable Python runtime to copy into "
            "runtime/python. Defaults to MARKITDOWN_PORTABLE_PYTHON_DIR."
        ),
    )
    parser.add_argument(
        "--clean",
        action="store_true",
        default=True,
        help="Clean the staging directory before building (default: true).",
    )
    parser.add_argument(
        "--no-clean",
        dest="clean",
        action="store_false",
        help="Reuse the existing staging directory.",
    )
    parser.add_argument(
        "--skip-dependencies",
        action="store_true",
        help="Skip vendoring dependencies; useful only for smoke-testing staging layout.",
    )
    return parser.parse_args()


def copytree(src: Path, dst: Path) -> None:
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst)


def copy_python_runtime(runtime_source: Path | None, runtime_destination: Path) -> None:
    if runtime_source is not None:
        runtime_source = runtime_source.resolve()
        if not runtime_source.exists():
            raise FileNotFoundError(f"Python runtime directory does not exist: {runtime_source}")
        copytree(runtime_source, runtime_destination)
        return

    if platform.system() != "Windows":
        raise RuntimeError(
            "Windows portable builds need a Windows Python runtime. Run this script on "
            "Windows or pass --python-runtime-dir / set MARKITDOWN_PORTABLE_PYTHON_DIR."
        )

    copytree(Path(sys.base_prefix), runtime_destination)


def vendor_dependencies(site_packages_dir: Path) -> None:
    site_packages_dir.mkdir(parents=True, exist_ok=True)
    command = [
        sys.executable,
        "-m",
        "pip",
        "install",
        "--upgrade",
        "--target",
        str(site_packages_dir),
        *DEPENDENCY_REQUIREMENTS,
    ]
    subprocess.run(command, cwd=REPO_ROOT, check=True)


def validate_forbidden_dependencies(site_packages_dir: Path) -> None:
    found = []
    if not site_packages_dir.exists():
        return

    for child in site_packages_dir.iterdir():
        normalized = child.name.lower().replace("-", "_")
        if any(normalized.startswith(package.replace("-", "_")) for package in FORBIDDEN_PACKAGES):
            found.append(child.name)

    if found:
        raise RuntimeError(
            "Forbidden audio/YouTube dependencies were bundled: " + ", ".join(sorted(found))
        )


def copy_release_docs(staging_dir: Path) -> None:
    shutil.copyfile(PORTABLE_DIR / "README.txt", staging_dir / "README.txt")
    shutil.copyfile(
        PORTABLE_DIR / "Start MarkItDown Local.cmd.template",
        staging_dir / "Start MarkItDown Local.cmd",
    )

    notices = REPO_ROOT / "packages" / "markitdown" / "ThirdPartyNotices.md"
    if notices.exists():
        shutil.copyfile(notices, staging_dir / "THIRD_PARTY_NOTICES.txt")

    license_file = REPO_ROOT / "LICENSE"
    if license_file.exists():
        shutil.copyfile(license_file, staging_dir / "LICENSE.txt")


def stage_files(args: argparse.Namespace) -> None:
    if args.clean and STAGING_DIR.exists():
        shutil.rmtree(STAGING_DIR)
    STAGING_DIR.mkdir(parents=True, exist_ok=True)

    copytree(LOCAL_APP_SRC, STAGING_DIR / "app" / "markitdown_local_app")
    copy_release_docs(STAGING_DIR)
    copy_python_runtime(args.python_runtime_dir, STAGING_DIR / "runtime" / "python")

    if not args.skip_dependencies:
        vendor_dependencies(STAGING_DIR / "site-packages")
    validate_forbidden_dependencies(STAGING_DIR / "site-packages")


def create_zip(staging_dir: Path, zip_path: Path) -> None:
    if zip_path.exists():
        zip_path.unlink()
    zip_path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(staging_dir.rglob("*")):
            archive.write(path, path.relative_to(staging_dir.parent))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    args = parse_args()
    stage_files(args)
    create_zip(STAGING_DIR, ZIP_PATH)
    digest = sha256(ZIP_PATH)
    checksum_path = ZIP_PATH.with_suffix(ZIP_PATH.suffix + ".sha256")
    checksum_path.write_text(f"{digest}  {ZIP_PATH.name}\n", encoding="utf-8")

    print(f"Portable artifact: {ZIP_PATH}")
    print(f"SHA256: {digest}")


if __name__ == "__main__":
    main()
