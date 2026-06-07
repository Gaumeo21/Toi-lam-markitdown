from markitdown_local_app.supported_formats import (
    AUDIO_REJECTION_ERROR,
    SUPPORTED_EXTENSIONS,
    markdown_download_filename,
    supported_formats_summary,
    validate_upload_filename,
)


def test_audio_extension_is_blocked():
    result = validate_upload_filename("meeting.MP3")

    assert not result.ok
    assert result.is_audio
    assert result.extension == ".mp3"
    assert result.message == AUDIO_REJECTION_ERROR


def test_supported_extension_is_accepted():
    result = validate_upload_filename("report.PDF")

    assert result.ok
    assert result.extension == ".pdf"


def test_unsupported_extension_is_rejected():
    result = validate_upload_filename("program.exe")

    assert not result.ok
    assert not result.is_audio
    assert ".exe" in result.message


def test_markdown_download_filename_uses_upload_stem():
    assert markdown_download_filename("Quarterly Report.pdf") == "Quarterly Report.md"


def test_markdown_download_filename_falls_back_for_empty_stem():
    assert markdown_download_filename("") == "document.md"
    assert markdown_download_filename(None) == "document.md"
    assert markdown_download_filename(".bashrc") == "document.md"


def test_supported_formats_summary_has_no_url_flow():
    summary = supported_formats_summary().lower()

    assert "url" not in summary
    assert "youtube" not in summary
    assert "http" not in summary
    assert ".pdf" in summary
    assert ".docx" in summary


def test_supported_extensions_do_not_include_audio_extensions():
    assert ".mp3" not in SUPPORTED_EXTENSIONS
    assert ".wav" not in SUPPORTED_EXTENSIONS
