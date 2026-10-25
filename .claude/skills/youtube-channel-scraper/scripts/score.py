"""Deterministic relevance scoring - no AI.

relevance_score (0-100) = keyword_weight * keyword_component + engagement_weight * engagement_component

keyword_component:    2 pts per keyword found in the title, 1 pt if only in description/transcript,
                      divided by the best score of `keyword_saturation` keywords (default 3). Dividing by
                      the full keyword list instead would make long lists impossible to score well on -
                      11 keywords would cap a title hit at ~9/100.
engagement_component: log-scaled min-max of the rank_by metric (views|likes) across ALL scraped videos.
                      Log scale stops one viral video from flattening every other video to ~0.
"""
import math


def keyword_component(video, total_keywords, saturation):
    if total_keywords == 0:
        return 0.0
    in_title = set(video.get("matched_in_title", []))
    points = sum(2 if kw in in_title else 1 for kw in set(video.get("matched_keywords", [])))
    max_points = 2 * max(1, min(total_keywords, saturation))
    return min(100.0, points / max_points * 100)


def engagement_range(videos, field):
    values = [math.log1p(v.get(field) or 0) for v in videos]
    return min(values), max(values)


def engagement_component(video, field, lo, hi):
    value = math.log1p(video.get(field) or 0)
    if hi == lo:
        return 100.0 if (video.get(field) or 0) > 0 else 0.0
    return max(0.0, min(100.0, (value - lo) / (hi - lo) * 100))


def score_videos(all_videos, config):
    field = "view_count" if config.get("rank_by", "views") == "views" else "like_count"
    kw_w = config.get("keyword_weight", 0.7)
    eng_w = config.get("engagement_weight", 0.3)
    saturation = config.get("keyword_saturation", 3)
    total = len(config["keywords"])
    lo, hi = engagement_range(all_videos, field)

    for v in all_videos:
        if not v.get("is_match"):
            v["relevance_score"] = None
            continue
        kc = keyword_component(v, total, saturation)
        ec = engagement_component(v, field, lo, hi)
        v["relevance_score"] = round(kw_w * kc + eng_w * ec, 2)
    return all_videos
