# SPDX-FileCopyrightText: 2024-present Adam Fourney <adamfo@microsoft.com>
#
# SPDX-License-Identifier: MIT
"""Streamlit UI for the MarkItDown local portable app."""

from __future__ import annotations

import os
import tempfile
from pathlib import Path
from typing import BinaryIO

import streamlit as st
from markitdown import MarkItDown

from markitdown_local_app.supported_formats import (
    UNSUPPORTED_NOTE,
    markdown_download_filename,
    streamlit_uploader_types,
    supported_formats_summary,
    validate_upload_filename,
)


def convert_uploaded_file(
    uploaded_file: BinaryIO,
    *,
    filename: str,
    keep_data_uris: bool = False,
    enable_plugins: bool = False,
) -> str:
    """Convert a Streamlit-uploaded local file to Markdown using a temporary file."""

    validation = validate_upload_filename(filename)
    if not validation.ok:
        raise ValueError(validation.message)

    temp_path: str | None = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=validation.extension) as temp_file:
            temp_path = temp_file.name
            getbuffer = getattr(uploaded_file, "getbuffer", None)
            if callable(getbuffer):
                temp_file.write(getbuffer())
            else:
                temp_file.write(uploaded_file.read())

        md = MarkItDown(enable_plugins=enable_plugins)
        result = md.convert(temp_path, keep_data_uris=keep_data_uris)
        return result.markdown
    finally:
        if temp_path and os.path.exists(temp_path):
            os.unlink(temp_path)


def main() -> None:
    """Render the Streamlit app."""

    st.set_page_config(page_title="MarkItDown Local Portable", page_icon="📝")

    st.title("MarkItDown Local Portable")
    st.write("Convert local files to Markdown on your machine.")

    with st.sidebar:
        st.header("Options")
        keep_data_uris = st.checkbox("Keep data URIs", value=False)
        enable_plugins = st.checkbox("Enable plugins", value=False)
        with st.expander("Advanced cloud options", expanded=False):
            st.info(
                "Cloud conversion options are disabled in this MVP. Files stay local "
                "unless you install and enable plugins or future cloud features yourself."
            )
        st.warning("Do not enable plugins unless you trust the bundled or installed plugins.")

    st.subheader("Drop a local file here or browse")
    uploaded_file = st.file_uploader(
        "Drop a local file here or browse",
        type=streamlit_uploader_types(),
        accept_multiple_files=False,
        label_visibility="collapsed",
    )

    with st.expander("Supported formats", expanded=True):
        st.markdown(supported_formats_summary())

    st.warning(UNSUPPORTED_NOTE)
    st.caption("Streaming input/stdin and remote inputs are not available in this local app.")

    if uploaded_file is None:
        return

    validation = validate_upload_filename(uploaded_file.name)
    if not validation.ok:
        st.error(validation.message)
        return

    if st.button("Convert to Markdown", type="primary"):
        try:
            markdown = convert_uploaded_file(
                uploaded_file,
                filename=uploaded_file.name,
                keep_data_uris=keep_data_uris,
                enable_plugins=enable_plugins,
            )
        except Exception as exc:
            st.error(f"Conversion failed: {exc}")
            return

        st.success("Conversion complete.")
        raw_tab, preview_tab = st.tabs(["Raw Markdown", "Preview"])
        with raw_tab:
            st.text_area("Raw Markdown", markdown, height=400)
        with preview_tab:
            st.markdown(markdown or "_(No Markdown content was produced.)_")

        st.download_button(
            "Download Markdown",
            data=markdown,
            file_name=markdown_download_filename(uploaded_file.name),
            mime="text/markdown; charset=utf-8",
        )


if __name__ == "__main__":
    main()
