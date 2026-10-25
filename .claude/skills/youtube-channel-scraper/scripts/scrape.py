"""Pull every upload of a YouTube channel via YouTube Data API v3.

Accepts a channel as @handle, a youtube.com URL (/@handle or /channel/UC...), or a
bare UC... channel ID. Returns (channel_info, videos) and caches raw metadata to
<cache_dir>/videos_raw.json.

Each video gets `duration_seconds` and `video_type` ("video" | "short" | "live") so
callers can drop Shorts; the uploads playlist mixes all three.
"""
import json
import re
from pathlib import Path
from urllib.parse import urlparse

from googleapiclient.discovery import build


def parse_channel_ref(ref):
    """Return ('handle', 'name') or ('id', 'UC...') for whatever the user pasted."""
    ref = (ref or "").strip()
    if not ref:
        raise RuntimeError("Empty channel reference.")
    if re.fullmatch(r"UC[\w-]{22}", ref):
        return "id", ref
    if ref.startswith("@"):
        return "handle", ref[1:]
    if "youtube.com" in ref or "youtu.be" in ref:
        path = urlparse(ref if "://" in ref else "https://" + ref).path.strip("/")
        parts = path.split("/")
        if parts and parts[0].startswith("@"):
            return "handle", parts[0][1:]
        if len(parts) >= 2 and parts[0] == "channel" and parts[1].startswith("UC"):
            return "id", parts[1]
        raise RuntimeError(
            f"Can't resolve '{ref}' to a channel. Legacy /c/ and /user/ URLs aren't supported - "
            "open the channel page and copy its @handle or /channel/UC... URL."
        )
    return "handle", ref  # bare name, treat as handle


def ref_to_slug(ref):
    kind, value = parse_channel_ref(ref)
    return re.sub(r"[^\w.-]+", "_", value)


def get_channel_info(youtube, ref):
    kind, value = parse_channel_ref(ref)
    kwargs = {"forHandle": value} if kind == "handle" else {"id": value}
    resp = youtube.channels().list(part="contentDetails,snippet,statistics", **kwargs).execute()
    items = resp.get("items", [])
    if not items:
        raise RuntimeError(f"No channel found for '{ref}'. Check the handle for typos.")
    ch = items[0]
    stats = ch["statistics"]
    return {
        "channel_id": ch["id"],
        "display_name": ch["snippet"]["title"],
        "video_count": int(stats.get("videoCount", 0)),
        "subscriber_count": int(stats["subscriberCount"]) if "subscriberCount" in stats else None,
        "uploads_playlist_id": ch["contentDetails"]["relatedPlaylists"]["uploads"],
    }


def get_all_video_ids(youtube, playlist_id):
    ids = []
    request = youtube.playlistItems().list(part="contentDetails", playlistId=playlist_id, maxResults=50)
    while request is not None:
        response = request.execute()
        ids.extend(i["contentDetails"]["videoId"] for i in response.get("items", []))
        request = youtube.playlistItems().list_next(request, response)
    return ids


def chunked(seq, size):
    for i in range(0, len(seq), size):
        yield seq[i:i + size]


def duration_to_seconds(dur):
    m = re.match(r"P(?:(\d+)D)?T?(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?$", dur or "")
    if not m:
        return None
    d, h, mi, s = (int(x) if x else 0 for x in m.groups())
    return d * 86400 + h * 3600 + mi * 60 + s


def classify_type(item, seconds, shorts_max_seconds):
    if item.get("liveStreamingDetails"):
        return "live"
    if seconds is not None and seconds <= shorts_max_seconds:
        return "short"
    return "video"


def get_video_details(youtube, video_ids, shorts_max_seconds):
    videos = []
    for batch in chunked(video_ids, 50):
        resp = youtube.videos().list(
            part="snippet,statistics,contentDetails,liveStreamingDetails", id=",".join(batch)
        ).execute()
        for item in resp.get("items", []):
            snippet, stats, content = item["snippet"], item.get("statistics", {}), item.get("contentDetails", {})
            seconds = duration_to_seconds(content.get("duration"))
            videos.append({
                "video_id": item["id"],
                "title": snippet.get("title"),
                "description": snippet.get("description"),
                "published_at": snippet.get("publishedAt"),
                "url": f"https://www.youtube.com/watch?v={item['id']}",
                "view_count": int(stats.get("viewCount", 0)),
                "like_count": int(stats["likeCount"]) if "likeCount" in stats else None,
                "comment_count": int(stats["commentCount"]) if "commentCount" in stats else None,
                "duration": content.get("duration"),
                "duration_seconds": seconds,
                "video_type": classify_type(item, seconds, shorts_max_seconds),
            })
    return videos


def scrape_channel(api_key, ref, cache_dir, shorts_max_seconds=60):
    """Scrape all uploads. Returns (channel_info, videos); caches raw data in cache_dir."""
    youtube = build("youtube", "v3", developerKey=api_key, cache_discovery=False)
    channel_info = get_channel_info(youtube, ref)
    print(f"Channel: {channel_info['display_name']} "
          f"({channel_info['video_count']} videos, {channel_info['subscriber_count']} subscribers)")

    video_ids = get_all_video_ids(youtube, channel_info["uploads_playlist_id"])
    print(f"Found {len(video_ids)} uploads.")
    videos = get_video_details(youtube, video_ids, shorts_max_seconds)

    cache_dir = Path(cache_dir)
    cache_dir.mkdir(parents=True, exist_ok=True)
    (cache_dir / "videos_raw.json").write_text(json.dumps(videos, indent=2, ensure_ascii=False), encoding="utf-8")
    return channel_info, videos
