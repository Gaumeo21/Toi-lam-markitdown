# SPDX-FileCopyrightText: 2024-present Adam Fourney <adamfo@microsoft.com>
#
# SPDX-License-Identifier: MIT
"""Supported and blocked formats for the local portable Streamlit app."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

AUDIO_EXTENSIONS: frozenset[str] = frozenset(
    {
        ".mp3",
        ".wav",
        ".m4a",
        ".flac",
        ".ogg",
        ".aac",
        ".wma",
    }
)

SUPPORTED_FORMAT_GROUPS: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("PDF", (".pdf",)),
    ("Word", (".docx",)),
    ("PowerPoint", (".pptx",)),
    ("Excel", (".xlsx", ".xls")),
    ("Text/Markdown", (".txt", ".md")),
    ("Web/text data files", (".html", ".htm", ".csv", ".json", ".xml")),
    ("Images", (".png", ".jpg", ".jpeg")),
    ("ZIP archives", (".zip",)),
)

SUPPORTED_EXTENSIONS: frozenset[str] = frozenset(
    extension for _, extensions in SUPPORTED_FORMAT_GROUPS for extension in extensions
)

UNSUPPORTED_NOTE = (
    "YouTube URLs, web URLs, and audio files are not supported in this portable app."
)
AUDIO_REJECTION_ERROR = "Audio files are not supported in this portable app."


@dataclass(frozen=True)
class ValidationResult:
    """Describes whether an uploaded file extension can be converted."""

    ok: bool
    extension: str
    message: str = ""
    is_audio: bool = False


def normalized_extension(filename: str | None) -> str:
    """Return a lower-case suffix for an uploaded file name."""

    if not filename:
        return ""
    return Path(filename).suffix.lower()


def validate_upload_filename(filename: str | None) -> ValidationResult:
    """Validate a local upload file name before writing it to disk."""

    extension = normalized_extension(filename)
    if extension in AUDIO_EXTENSIONS:
        return ValidationResult(
            ok=False,
            extension=extension,
            message=AUDIO_REJECTION_ERROR,
            is_audio=True,
        )

    if extension not in SUPPORTED_EXTENSIONS:
        supported = ", ".join(sorted(SUPPORTED_EXTENSIONS))
        return ValidationResult(
            ok=False,
            extension=extension,
            message=f"Unsupported file type '{extension or '(none)'}'. Supported extensions: {supported}.",
        )

    return ValidationResult(ok=True, extension=extension)


def markdown_download_filename(filename: str | None) -> str:
    """Return a safe Markdown download filename for an upload name."""

    stem = Path(filename or "").stem.strip()
    if not stem or stem.startswith("."):
        stem = "document"
    return f"{stem}.md"


def streamlit_uploader_types() -> list[str]:
    """Return extension names formatted for st.file_uploader(type=...)."""

    return sorted(extension.removeprefix(".") for extension in SUPPORTED_EXTENSIONS | AUDIO_EXTENSIONS)


def supported_formats_summary() -> str:
    """Return a Markdown bullet list of supported file format groups."""

    return "\n".join(
        f"- **{label}:** {', '.join(extensions)}"
        for label, extensions in SUPPORTED_FORMAT_GROUPS
    )
