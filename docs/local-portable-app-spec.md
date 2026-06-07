# MarkItDown Local Portable App Spec

## 1. Mục tiêu

Tạo một ứng dụng local dạng portable cho MarkItDown để người dùng phổ thông có thể chuyển đổi tài liệu sang Markdown bằng giao diện kéo-thả, không cần thao tác với Python, `pip install`, virtual environment, hoặc command line phức tạp sau khi đã tải gói portable.

Luồng người dùng mục tiêu:

```text
Download zip → Extract → Run launcher script → Browser mở app local → Kéo-thả file → Convert → Download .md
```

Ứng dụng phải chạy cục bộ trên máy người dùng theo mặc định. Không upload tài liệu lên dịch vụ ngoài trừ khi người dùng chủ động bật tùy chọn cloud trong phần nâng cao.

## 2. Ràng buộc sản phẩm

### 2.1. Không hỗ trợ YouTube URL hoặc web URL

Ứng dụng portable này chỉ nhận file local. Không cung cấp ô nhập URL và không hỗ trợ chuyển đổi:

- YouTube URL.
- Web page URL.
- Remote URL bất kỳ.
- Nội dung từ stdin hoặc pipe.

Ứng dụng không được gọi trực tiếp các API chuyển đổi URL như `convert_url()` hoặc `convert_uri()` cho input từ người dùng.

### 2.2. Không hỗ trợ audio

Ứng dụng portable này không hỗ trợ audio transcription hoặc audio metadata conversion. UI phải từ chối sớm các file audio và hiển thị thông báo rõ ràng.

Các extension audio bị chặn tối thiểu:

- `.mp3`
- `.wav`
- `.m4a`
- `.flac`
- `.ogg`
- `.aac`
- `.wma`

### 2.3. Portable, không yêu cầu install

Artifact phát hành chính là file `.zip`. Người dùng chỉ cần tải về, giải nén và chạy launcher script.

Không yêu cầu người dùng:

- Cài Python thủ công.
- Chạy `pip install`.
- Tạo virtual environment.
- Chạy file application `.exe` trực tiếp.
- Dùng terminal command phức tạp.

Trên Windows, bundle có thể chứa Python runtime portable nội bộ. Người dùng không chạy `python.exe` trực tiếp; launcher script gọi runtime này ở bên trong.

### 2.4. Không đóng gói thành app `.exe`

Không dùng các hướng đóng gói tạo executable app cho MVP:

- PyInstaller one-file `.exe`.
- Nuitka `.exe`.
- cx_Freeze `.exe`.
- Electron desktop `.exe`.
- Tauri desktop `.exe`.
- Windows installer `.msi`.

Launcher được chấp nhận:

- Windows: `.cmd` hoặc `.bat`.
- macOS/Linux trong giai đoạn sau: `.command` hoặc `.sh`.

## 3. Phạm vi MVP

### 3.1. Bắt buộc

MVP phải có:

- Giao diện web local, ưu tiên Streamlit để triển khai nhanh.
- Drag-and-drop hoặc file picker cho một file local mỗi lần.
- Validate extension trước khi convert.
- Từ chối audio file bằng lỗi dễ hiểu.
- Không có input URL.
- Convert file local sang Markdown bằng API Python của MarkItDown.
- Preview Markdown dạng raw text và rendered preview.
- Nút tải file `.md`.
- Temporary file an toàn và được xóa sau convert.
- Portable Windows zip có launcher script.
- README trong artifact hướng dẫn chạy.

### 3.2. Ngoài phạm vi MVP

MVP không bao gồm:

- Batch convert nhiều file.
- Lưu lịch sử chuyển đổi.
- User account hoặc auth.
- Remote hosting.
- Desktop executable app.
- YouTube/web URL conversion.
- Audio transcription.
- Audio metadata extraction.
- Advanced Markdown editor.

## 4. Định dạng file hỗ trợ

### 4.1. Supported formats cho MVP

Danh sách hiển thị trong UI và tài liệu phải khớp với dependencies thực sự được bundle. MVP ưu tiên các file local phổ biến:

- PDF: `.pdf`
- Word: `.docx`
- PowerPoint: `.pptx`
- Excel: `.xlsx`, `.xls`
- Text/Markdown: `.txt`, `.md`
- Web/text data files: `.html`, `.htm`, `.csv`, `.json`, `.xml`
- Images nếu dependencies đã bundle đủ: `.png`, `.jpg`, `.jpeg`, `.tiff`, `.bmp`
- ZIP nếu muốn giữ converter local archive: `.zip`

### 4.2. Explicitly unsupported

UI và README phải ghi rõ không hỗ trợ:

- YouTube URLs.
- Web URLs.
- Remote URLs.
- Audio files.
- Streaming input/stdin.

## 5. Kiến trúc repo đề xuất

Tạo package/app riêng để không làm rối core package `markitdown`:

```text
packages/
  markitdown-local-app/
    pyproject.toml
    README.md
    portable/
      README.txt
      Start MarkItDown Local.cmd.template
    src/
      markitdown_local_app/
        __init__.py
        __main__.py
        app.py
        supported_formats.py
    tests/
      test_supported_formats.py
scripts/
  build_portable_windows.py
```

Vai trò chính:

- `app.py`: Streamlit UI và conversion flow.
- `supported_formats.py`: danh sách supported/blocked extensions và helper validate input.
- `__main__.py`: entry point chạy Streamlit trong môi trường development.
- `portable/README.txt`: README được copy vào artifact portable.
- `scripts/build_portable_windows.py`: build artifact portable zip.

## 6. UX spec

### 6.1. Layout

```text
+----------------------------------------------------------+
| MarkItDown Local Portable                                |
| Convert local files to Markdown on your machine.         |
+-------------------------+--------------------------------+
| Sidebar                 | Main area                      |
|                         |                                |
| [ ] Keep data URIs      | Drop a local file here         |
| [ ] Enable plugins      |                                |
| Advanced cloud options  | Supported formats summary      |
|                         | Not supported warning          |
|                         |                                |
|                         | [ Convert to Markdown ]        |
|                         |                                |
|                         | Tabs: Raw Markdown | Preview   |
|                         |                                |
|                         | [ Download Markdown ]          |
+-------------------------+--------------------------------+
```

### 6.2. UI text bắt buộc

- Title: `MarkItDown Local Portable`
- Subtitle: `Convert local files to Markdown on your machine.`
- Upload label: `Drop a local file here or browse`
- Convert button: `Convert to Markdown`
- Download button: `Download Markdown`
- Unsupported note: `YouTube URLs, web URLs, and audio files are not supported in this portable app.`
- Audio rejection error: `Audio files are not supported in this portable app.`

### 6.3. Sidebar options

MVP sidebar nên đơn giản:

- `Keep data URIs`, mặc định off.
- `Enable plugins`, mặc định off.
- `Advanced cloud options`, collapsed mặc định hoặc loại khỏi MVP nếu muốn app offline tuyệt đối.

Không được thêm:

- URL input.
- YouTube URL input.
- Audio transcription settings.
- OpenAI audio/transcription settings.

## 7. Conversion flow

Ứng dụng phải convert qua local temporary file:

```text
User uploads file
  ↓
Validate extension
  ↓
Reject audio/unsupported input
  ↓
Write bytes to safe temporary file
  ↓
Call MarkItDown.convert(temp_path)
  ↓
Read result.markdown
  ↓
Delete temporary file in finally
  ↓
Show preview + download button
```

Yêu cầu implementation:

1. Lấy `uploaded_file` từ `st.file_uploader(...)`.
2. Lấy suffix bằng `Path(uploaded_file.name).suffix.lower()`.
3. Nếu suffix nằm trong audio blocklist, hiển thị `st.error(...)` và dừng flow.
4. Tạo temporary file bằng `tempfile.NamedTemporaryFile(delete=False, suffix=suffix)`.
5. Ghi bytes từ `uploaded_file.getbuffer()` vào temporary file.
6. Khởi tạo `MarkItDown(enable_plugins=enable_plugins, **optional_kwargs)`.
7. Gọi `result = md.convert(temp_path, keep_data_uris=keep_data_uris)`.
8. Lấy Markdown từ `result.markdown`.
9. Xóa temporary file trong `finally` bằng `os.unlink(temp_path)` nếu file tồn tại.
10. Tạo download filename bằng `Path(uploaded_file.name).stem + ".md"`; nếu stem rỗng thì fallback `document.md`.

Không dùng CLI subprocess để convert file. Không truyền URL string từ user vào `MarkItDown.convert(...)`.

## 8. Packaging portable Windows

### 8.1. Artifact

Build process tạo artifact:

```text
markitdown-local-portable-windows-x64.zip
```

Sau khi giải nén:

```text
markitdown-local/
  Start MarkItDown Local.cmd
  README.txt
  THIRD_PARTY_NOTICES.txt
  app/
    markitdown_local_app/
      app.py
      __main__.py
      supported_formats.py
      ...
  runtime/
    python/
      ...
  site-packages/
    ...
```

Cấu trúc có thể thay đổi nếu build script cần tối ưu, nhưng phải giữ nguyên trải nghiệm người dùng: giải nén zip và chạy launcher script.

### 8.2. Windows launcher

Launcher chính:

```text
Start MarkItDown Local.cmd
```

Nhiệm vụ launcher:

1. Xác định thư mục artifact bằng `%~dp0`.
2. Set biến môi trường để dùng Python runtime nội bộ.
3. Set `PYTHONPATH` trỏ đến app và site-packages portable.
4. Chạy Streamlit app local.
5. Mở browser hoặc hiển thị URL local để người dùng copy.
6. Giữ cửa sổ mở nếu app lỗi để user đọc troubleshooting.

Concept launcher:

```bat
@echo off
set APP_DIR=%~dp0
set PYTHON=%APP_DIR%runtime\python\python.exe
set PYTHONPATH=%APP_DIR%site-packages;%APP_DIR%app
"%PYTHON%" -m streamlit run "%APP_DIR%app\markitdown_local_app\app.py" --server.headless true
pause
```

Launcher có thể gọi `python.exe` nội bộ, nhưng người dùng không phải chạy `.exe` trực tiếp.

### 8.3. Build script

`scripts/build_portable_windows.py` cần:

1. Tạo staging directory, ví dụ `dist/markitdown-local/`.
2. Copy source local app vào `dist/markitdown-local/app/`.
3. Bundle Python portable runtime vào `dist/markitdown-local/runtime/python/`.
4. Vendor dependencies vào `dist/markitdown-local/site-packages/` hoặc layout tương đương.
5. Include `markitdown`, `streamlit`, và dependencies cho supported formats.
6. Exclude YouTube/audio extras.
7. Copy `README.txt`, launcher script, license/third-party notices.
8. Zip staging directory thành `dist/markitdown-local-portable-windows-x64.zip`.
9. In checksum artifact, ví dụ SHA256, để release dễ kiểm tra.

## 9. Dependency policy

Không dùng mặc định `markitdown[all]` cho portable nếu extra này kéo theo audio/youtube dependencies.

Build script phải chọn extras cụ thể theo supported local formats. Ví dụ concept, cần xác minh tên extras chính xác trong `packages/markitdown/pyproject.toml` khi implement:

```bash
pip install 'packages/markitdown[pdf,docx,pptx,xlsx,xls,outlook]'
```

Không chọn extras:

- `audio-transcription`
- `youtube-transcription`

Nếu image support làm tăng kích thước quá nhiều, có thể tắt image ở MVP hoặc đưa vào variant artifact riêng, nhưng UI/README phải phản ánh đúng khả năng thực tế.

## 10. Security và privacy

Ứng dụng xử lý file với quyền của process hiện tại. Tài liệu phải cảnh báo:

- Chỉ convert file tin cậy hoặc chạy trong môi trường cô lập nếu file đến từ nguồn không tin cậy.
- Không bật plugins nếu không tin tưởng plugin đã được bundle/cài.
- Không bật cloud options nếu không muốn dữ liệu rời khỏi máy.
- Temporary file phải được xóa sau mỗi lần convert.
- Không lưu nội dung file upload vào repo root, working directory, hoặc thư mục artifact lâu dài.

Mặc định MVP nên local-only. Nếu giữ cloud options, phải đặt trong section advanced collapsed và giải thích rõ dữ liệu có thể gửi tới dịch vụ ngoài.

## 11. Test plan

### 11.1. Unit tests

Nếu tách helper vào `supported_formats.py`, cần test:

- Audio extension bị block.
- Supported extension được accept.
- Tên output `.md` được tạo đúng từ tên upload.
- Tên rỗng hoặc không có stem fallback thành `document.md`.
- URL-like strings không xuất hiện trong upload flow.

### 11.2. Manual QA

Trên Windows portable artifact:

1. Tải zip mới.
2. Giải nén vào path có khoảng trắng, ví dụ `C:\Users\User\Downloads\MarkItDown Local\`.
3. Double-click `Start MarkItDown Local.cmd`.
4. Xác nhận browser mở Streamlit local app.
5. Upload `.txt`, convert, preview, download `.md`.
6. Upload `.pdf`, convert, preview, download `.md`.
7. Upload `.mp3`, xác nhận bị từ chối rõ ràng.
8. Xác nhận UI không có input URL.
9. Xác nhận không cần chạy `pip install`.
10. Xác nhận không cần chạy application `.exe` trực tiếp.

### 11.3. Build validation

Build pipeline cần kiểm tra:

- Artifact zip tồn tại.
- Artifact có launcher script.
- Artifact có README.txt.
- Artifact có runtime nội bộ.
- Artifact không bundle extras audio/youtube ngoài ý muốn.
- SHA256 được in hoặc ghi ra file.

## 12. Acceptance criteria

Hoàn thành khi tất cả tiêu chí sau đạt:

- Có package/app local riêng trong repo hoặc spec được dùng để tạo package đó.
- Có portable Windows zip artifact.
- Người dùng chạy được bằng cách giải nén và double-click `Start MarkItDown Local.cmd`.
- Không yêu cầu user chạy `pip install`.
- Không yêu cầu user cài Python thủ công.
- Không yêu cầu user chạy app `.exe` trực tiếp.
- UI chỉ nhận file local.
- UI không có YouTube URL input hoặc web URL input.
- Audio files bị từ chối trước khi convert.
- File local supported convert được sang Markdown.
- Preview Markdown hoạt động.
- Download `.md` hoạt động.
- Temporary file được xóa sau convert.
- README portable ghi rõ supported và unsupported formats.
- Dependencies portable không include audio/youtube extras nếu không cần.

## 13. Implementation task list

### Task 1: Tạo package local app

Tạo `packages/markitdown-local-app/` với Streamlit app, helper validate extension, README và tests cơ bản.

### Task 2: Tạo UI local-only

Triển khai UI không có URL input, hiển thị supported/unsupported formats, upload file local, convert, preview và download.

### Task 3: Chặn audio file

Thêm blocklist audio extension, unit tests, và thông báo lỗi rõ ràng trong UI.

### Task 4: Temporary file safety

Đảm bảo upload bytes chỉ ghi vào temporary file an toàn và luôn xóa trong `finally`.

### Task 5: Tạo portable Windows build

Thêm build script tạo staging directory, vendor runtime/dependencies, launcher `.cmd`, README.txt và zip artifact.

### Task 6: Dependency pruning

Chọn extras cụ thể, không dùng audio/youtube extras, và cập nhật UI/README theo dependencies thực tế.

### Task 7: Manual QA portable artifact

Chạy checklist Windows portable để xác nhận trải nghiệm download → extract → run script → convert → download Markdown.
