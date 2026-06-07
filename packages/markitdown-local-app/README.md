# MarkItDown Local Portable App

MarkItDown Local Portable is a local-only Streamlit UI for converting one local file at a time to Markdown. It is designed for the portable ZIP flow described in `docs/local-portable-app-spec.md`:

```text
Download zip -> Extract -> Run launcher script -> Browser opens local app -> Drop file -> Convert -> Download .md
```

## MVP behavior

- Runs as a local web app.
- Accepts exactly one local file per conversion.
- Does not provide URL, YouTube, remote URL, stdin, or pipe input.
- Rejects audio files before conversion.
- Writes uploads only to a temporary file and deletes the temporary file after conversion.
- Shows both raw Markdown and rendered preview tabs.
- Provides a `Download Markdown` button.

## Supported formats

The portable MVP is configured for these local formats:

- PDF: `.pdf`
- Word: `.docx`
- PowerPoint: `.pptx`
- Excel: `.xlsx`, `.xls`
- Text/Markdown: `.txt`, `.md`
- Web/text data files: `.html`, `.htm`, `.csv`, `.json`, `.xml`
- Images: `.png`, `.jpg`, `.jpeg`
- ZIP archives: `.zip`

## Explicitly unsupported

The portable app does not support:

- YouTube URLs.
- Web URLs.
- Remote URLs.
- Audio files.
- Streaming input/stdin.

Audio extensions blocked by the UI include `.mp3`, `.wav`, `.m4a`, `.flac`, `.ogg`, `.aac`, and `.wma`.

## Development

From this package directory, install the package in a development environment and run:

```bash
python -m markitdown_local_app
```

or:

```bash
streamlit run src/markitdown_local_app/app.py
```

## Portable Windows build

From the repository root, run the Windows portable build script on a Windows x64 machine with Python installed:

```powershell
python scripts/build_portable_windows.py
```

The script stages `dist/markitdown-local/`, vendors app dependencies without the MarkItDown audio or YouTube extras, copies the launcher and README, and writes `dist/markitdown-local-portable-windows-x64.zip`.
