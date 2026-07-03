"""google-drive-mcp — FastMCP server for reading/downloading files from Google Drive.

Provides read-only access to Google Drive files. Exposes tools to:
  - List and search files in Google Drive.
  - Download files/folders and copy them to the sources/internal_documentation/ directory.
  - Convert Google Docs/Sheets to Markdown/CSV during download.
"""
from __future__ import annotations

import io
import os
import re
import sys
from pathlib import Path
from typing import Annotated

from mcp.server.fastmcp import FastMCP
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from markitdown import MarkItDown

# ── Path bootstrap ────────────────────────────────────────────────────────────

def _find_root() -> Path:
    env = os.environ.get("PROJECT_ROOT")
    if env:
        return Path(env).resolve()
    for parent in Path(__file__).resolve().parents:
        if (parent / "state.json").exists():
            return parent
    raise RuntimeError(
        "Cannot locate project root. Set the PROJECT_ROOT environment variable."
    )

ROOT = _find_root()
INTERNAL_DOC_DIR = ROOT / "sources" / "internal_documentation"

SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]

# ── Authentication Helper ──────────────────────────────────────────────────────

def get_credentials():
    # 1. Try Service Account
    service_account_path = os.environ.get("GDRIVE_SERVICE_ACCOUNT_PATH") or str(
        ROOT / ".agents" / "mcp" / "gdrive" / "service_account.json"
    )
    if os.path.exists(service_account_path):
        from google.oauth2 import service_account
        return service_account.Credentials.from_service_account_file(
            service_account_path, scopes=SCOPES
        )

    # 2. Try OAuth 2.0 (credentials.json + token.json)
    credentials_path = os.environ.get("GDRIVE_CREDENTIALS_PATH") or str(
        ROOT / ".agents" / "mcp" / "gdrive" / "credentials.json"
    )
    token_path = os.environ.get("GDRIVE_TOKEN_PATH") or str(
        ROOT / ".agents" / "mcp" / "gdrive" / "token.json"
    )

    from google.oauth2.credentials import Credentials
    creds = None
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            from google.auth.transport.requests import Request
            creds.refresh(Request())
        else:
            if os.path.exists(credentials_path):
                raise RuntimeError(
                    f"OAuth tokens are expired or missing. Please run the authentication flow by executing:\n"
                    f"PROJECT_ROOT={ROOT} .venv/bin/python .agents/mcp/gdrive/server.py --auth"
                )
            else:
                raise RuntimeError(
                    f"No Google Drive credentials found. Please place either:\n"
                    f"  1. A service account key JSON at: {service_account_path}\n"
                    f"  2. An OAuth client credentials JSON at: {credentials_path} and run auth using:\n"
                    f"     PROJECT_ROOT={ROOT} .venv/bin/python .agents/mcp/gdrive/server.py --auth"
                )
    return creds

# ── Helper for snake_case conversion ──────────────────────────────────────────

def to_snake_case(filename: str) -> str:
    path = Path(filename)
    stem = path.stem
    ext = path.suffix
    
    s = stem.lower()
    s = re.sub(r'[^a-z0-9_\-]', '_', s)
    s = s.replace('-', '_')
    s = re.sub(r'_+', '_', s)
    s = s.strip('_')
    
    return f"{s}{ext}"

# ── Server ────────────────────────────────────────────────────────────────────

mcp = FastMCP(
    "google-drive-mcp",
    instructions=(
        "Google Drive search and downloader. Allows read-only access to files. "
        "Allows listing, searching, and downloading files to sources/internal_documentation/ "
        "while converting Google Docs/Sheets to Markdown/CSV."
    ),
)

def get_drive_service():
    creds = get_credentials()
    return build("drive", "v3", credentials=creds)

# ── Tools ─────────────────────────────────────────────────────────────────────

@mcp.tool()
async def gdrive_list_files(
    query: Annotated[str | None, "Search query (Google Drive q parameter format e.g. name contains 'design' or mimeType = 'application/vnd.google-apps.folder')"] = None,
    page_size: Annotated[int, "Number of results to return (max 100)"] = 20,
) -> str:
    """List or search files in Google Drive."""
    try:
        service = get_drive_service()
        q_parts = []
        if query:
            q_parts.append(query)
        # Ensure we don't list trashed files
        q_parts.append("trashed = false")
        
        q = " and ".join(q_parts)
        
        results = service.files().list(
            q=q,
            pageSize=min(page_size, 100),
            fields="files(id, name, mimeType, modifiedTime, size)",
        ).execute()
        
        files = results.get("files", [])
        if not files:
            return "No files found."
            
        output = ["| Name | ID | Mime Type | Size (bytes) | Modified Time |", "|---|---|---|---|---|"]
        for f in files:
            size = f.get("size", "N/A")
            output.append(f"| {f['name']} | `{f['id']}` | {f['mimeType']} | {size} | {f['modifiedTime']} |")
            
        return "\n".join(output)
    except Exception as e:
        return f"Error listing files: {str(e)}"

@mcp.tool()
async def gdrive_download_file(
    file_id: Annotated[str, "Google Drive File ID"],
    dest_subdir: Annotated[str | None, "Optional subdirectory name under sources/internal_documentation/ to place the file"] = None,
) -> str:
    """Download a file from Google Drive and copy/convert it to the internal_documentation folder."""
    try:
        service = get_drive_service()
        
        # Get metadata
        meta = service.files().get(fileId=file_id, fields="id, name, mimeType").execute()
        file_name = meta["name"]
        mime_type = meta["mimeType"]
        
        # Determine destination folder
        dest_dir = INTERNAL_DOC_DIR
        if dest_subdir:
            dest_dir = dest_dir / dest_subdir
        dest_dir.mkdir(parents=True, exist_ok=True)
        
        is_workspace_doc = False
        export_mime_type = None
        target_ext = None
        
        if mime_type == "application/vnd.google-apps.document":
            # Google Doc -> export to docx, then convert to markdown
            is_workspace_doc = True
            export_mime_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            target_ext = ".docx"
        elif mime_type == "application/vnd.google-apps.spreadsheet":
            # Google Sheet -> export to CSV
            is_workspace_doc = True
            export_mime_type = "text/csv"
            target_ext = ".csv"
        elif mime_type == "application/vnd.google-apps.presentation":
            # Google Slides -> export to PDF
            is_workspace_doc = True
            export_mime_type = "application/pdf"
            target_ext = ".pdf"
        elif mime_type == "application/vnd.google-apps.folder":
            return f"Error: '{file_name}' is a folder. Downloading folders is not supported directly; please download files individually."
            
        # Standardize target filename to snake_case
        clean_name = to_snake_case(file_name)
        if target_ext and not clean_name.endswith(target_ext):
            # Strip current extension and add target
            path_obj = Path(clean_name)
            clean_name = f"{path_obj.stem}{target_ext}"
            
        # Path where we download the file
        local_path = dest_dir / clean_name
        
        # Perform download
        fh = io.BytesIO()
        if is_workspace_doc:
            request = service.files().export_media(fileId=file_id, mimeType=export_mime_type)
        else:
            request = service.files().get_media(fileId=file_id)
            
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while not done:
            status, done = downloader.next_chunk()
            
        # Write to file
        local_path.write_bytes(fh.getvalue())
        
        # Conversion logic for Google Docs
        if mime_type == "application/vnd.google-apps.document":
            # Convert docx to markdown using MarkItDown
            try:
                md = MarkItDown()
                result = md.convert(str(local_path))
                md_content = result.text_content
                
                # Write to .md file
                md_path = local_path.with_suffix(".md")
                md_path.write_text(md_content, encoding="utf-8")
                
                # Remove temporary docx
                local_path.unlink()
                local_path = md_path
            except Exception as conv_err:
                return f"Downloaded Google Doc to {local_path}, but failed to convert to Markdown: {str(conv_err)}"
                
        # Return success with relative path from workspace root
        rel_path = local_path.relative_to(ROOT)
        return f"Successfully downloaded and processed '{file_name}' -> '{rel_path}'"
        
    except Exception as e:
        return f"Error downloading file: {str(e)}"

# ── Main / CLI ────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    if "--auth" in sys.argv:
        from google_auth_oauthlib.flow import InstalledAppFlow
        credentials_path = os.environ.get("GDRIVE_CREDENTIALS_PATH") or str(
            ROOT / ".agents" / "mcp" / "gdrive" / "credentials.json"
        )
        token_path = os.environ.get("GDRIVE_TOKEN_PATH") or str(
            ROOT / ".agents" / "mcp" / "gdrive" / "token.json"
        )
        
        if not os.path.exists(credentials_path):
            print(f"Error: Credentials file not found at '{credentials_path}'")
            print("Please follow these steps:")
            print("1. Go to Google Cloud Console (https://console.cloud.google.com/)")
            print("2. Enable the Google Drive API for your project")
            print("3. Go to APIs & Services > Credentials")
            print("4. Click Create Credentials > OAuth client ID. Select Application type: Desktop app")
            print(f"5. Download the JSON file and save it to: {credentials_path}")
            sys.exit(1)
            
        print("Starting OAuth interactive flow. Opening browser...")
        flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
        creds = flow.run_local_server(port=0)
        
        with open(token_path, "w") as token:
            token.write(creds.to_json())
            
        print(f"Success! Token saved to '{token_path}'")
        sys.exit(0)
        
    mcp.run()
