"""Upload an .xlsx to Google Drive as a native Google Sheet via the gws CLI.

gws refuses paths outside its working directory, so we run it from the file's folder
with a bare filename. Prints the Sheet's id and link.

Usage: python upload_sheet.py <report.xlsx> [--name "Sheet title"] [--folder-id <driveFolderId>]
"""
import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

XLSX_MIME = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
SHEET_MIME = "application/vnd.google-apps.spreadsheet"


def upload_sheet(xlsx_path, name=None, folder_id=None):
    gws = shutil.which("gws")
    if not gws:
        raise RuntimeError("gws CLI not found on PATH (npm global install). Cannot upload to Google Sheets.")
    xlsx = Path(xlsx_path).resolve()
    body = {"name": name or xlsx.stem.replace("_", " "), "mimeType": SHEET_MIME}
    if folder_id:
        body["parents"] = [folder_id]
    cmd = [gws, "drive", "files", "create", "--json", json.dumps(body),
           "--params", json.dumps({"fields": "id,name,webViewLink"}),
           "--upload", xlsx.name, "--upload-content-type", XLSX_MIME]
    proc = subprocess.run(cmd, cwd=xlsx.parent, capture_output=True, text=True, encoding="utf-8")
    if proc.returncode != 0:
        raise RuntimeError(f"gws upload failed: {proc.stderr.strip() or proc.stdout.strip()}")
    return json.loads(proc.stdout)


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("xlsx")
    p.add_argument("--name")
    p.add_argument("--folder-id")
    a = p.parse_args()
    try:
        result = upload_sheet(a.xlsx, a.name, a.folder_id)
    except RuntimeError as e:
        sys.exit(str(e))
    print(f"Google Sheet: {result.get('webViewLink')}  (id {result.get('id')})")
