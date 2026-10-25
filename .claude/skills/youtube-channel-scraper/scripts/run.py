"""Scrape a YouTube channel, classify + score videos against criteria, build a ranked Excel
report, and optionally upload it to Google Sheets via gws.

Usage:
    python run.py --channel @SomeChannel --config criteria.json [--deep-scan] [--include-shorts]
                  [--top-n N] [--out-dir DIR] [--upload [--folder-id ID] [--sheet-name NAME]]

Needs YOUTUBE_API_KEY in the repo-root .env (YouTube Data API v3 key).
"""
import argparse
import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from build_excel import build_excel  # noqa: E402
from classify import classify_videos, compile_keywords  # noqa: E402
from scrape import ref_to_slug, scrape_channel  # noqa: E402
from score import score_videos  # noqa: E402


def find_repo_root():
    for p in [HERE, *HERE.parents]:
        if (p / "CLAUDE.md").exists():
            return p
    return Path.cwd()


def parse_args():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--channel", help="@handle, channel URL, or UC... id. Overrides the config's 'channel'.")
    p.add_argument("--config", required=True, help="Path to a criteria JSON file.")
    p.add_argument("--top-n", type=int, help="Max rows in 'Matched Criteria' (0 = no cap). Overrides config 'top_n'.")
    p.add_argument("--deep-scan", action="store_true", help="Also keyword-match video transcripts (slower).")
    p.add_argument("--include-shorts", action="store_true", help="Keep Shorts (excluded by default).")
    p.add_argument("--out-dir", help="Where to write the .xlsx (default: <repo>/.tmp/yt/<slug>/).")
    p.add_argument("--upload", action="store_true", help="Upload the .xlsx to Google Drive as a Sheet via gws.")
    p.add_argument("--folder-id", help="Drive folder id for --upload (default: My Drive root).")
    p.add_argument("--sheet-name", help="Title for the uploaded Sheet.")
    return p.parse_args()


def main():
    args = parse_args()
    root = find_repo_root()
    load_dotenv(root / ".env")

    config = json.loads(Path(args.config).read_text(encoding="utf-8"))
    if args.channel:
        config["channel"] = args.channel
    if not config.get("channel"):
        raise SystemExit("No channel specified: pass --channel or set 'channel' in the config file.")
    if args.include_shorts:
        config["include_shorts"] = True
    if not config.get("keywords"):
        raise SystemExit("Config needs a non-empty 'keywords' list.")

    api_key = os.environ.get("YOUTUBE_API_KEY")
    if not api_key:
        raise SystemExit("YOUTUBE_API_KEY missing - add it to the repo-root .env (see .env.example).")

    slug = ref_to_slug(config["channel"])
    cache_dir = root / ".tmp" / "yt" / slug
    try:
        channel_info, videos = scrape_channel(api_key, config["channel"], cache_dir,
                                              config.get("shorts_max_seconds", 60))
    except RuntimeError as e:
        raise SystemExit(str(e))
    (cache_dir / "channel_info.json").write_text(json.dumps(channel_info, indent=2), encoding="utf-8")

    videos = classify_videos(videos, config)
    if args.deep_scan:
        from transcripts import deep_scan
        videos = deep_scan(videos, compile_keywords(config["keywords"]),
                           config.get("transcript_languages", ["en", "hi", "bn"]), cache_dir)
        videos = classify_videos(videos, config)  # fold transcript hits into matches

    matched = sum(1 for v in videos if v["is_match"])
    shorts = sum(1 for v in videos if v.get("video_type") == "short")
    print(f"Matched {matched} / {len(videos)} videos ({shorts} Shorts "
          f"{'included' if config.get('include_shorts') else 'excluded'}).")
    if matched == 0:
        print("No matches - consider loosening keywords, min_views/min_likes, or the date range"
              + ("" if args.deep_scan else ", or retry with --deep-scan (topic may only be spoken)."))

    videos = score_videos(videos, config)
    (cache_dir / "videos_final.json").write_text(json.dumps(videos, indent=2, ensure_ascii=False), encoding="utf-8")

    top_n = args.top_n if args.top_n is not None else config.get("top_n", 30)
    out_dir = Path(args.out_dir) if args.out_dir else cache_dir
    xlsx = build_excel(channel_info["display_name"], videos, out_dir, top_n=top_n)

    if args.upload:
        from upload_sheet import upload_sheet
        try:
            res = upload_sheet(xlsx, args.sheet_name or f"{channel_info['display_name']} - Video Report",
                               args.folder_id)
            print(f"Google Sheet: {res.get('webViewLink')}  (id {res.get('id')})")
        except RuntimeError as e:
            print(f"Upload failed ({e}). Local file kept at {xlsx}.")


if __name__ == "__main__":
    main()
