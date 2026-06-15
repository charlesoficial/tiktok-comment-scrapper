from __future__ import annotations

import csv
import json
from pathlib import Path

from .client import TikTokClient
from .models import Comment
from .models import ExportResult
from .utils import extract_video_id


def export_comments(
    video: str,
    *,
    limit: int,
    output_dir: str | Path,
    include_replies: bool = True,
    pretty: bool = True,
    file_format: str = "json",
) -> list[Path]:
    video_id = extract_video_id(video)
    client = TikTokClient()
    comments = list(
        client.iter_comments(
            video_id,
            limit=limit,
            include_replies=include_replies,
        )
    )
    caption, video_url = client.get_video_meta(video_id)

    result = ExportResult(
        video_id=video_id,
        caption=caption,
        video_url=video_url,
        comment_count=len(comments),
        comments=comments,
    )

    destination = Path(output_dir)
    destination.mkdir(parents=True, exist_ok=True)
    files: list[Path] = []

    if file_format in {"json", "both"}:
        files.append(_write_json(result, destination, pretty=pretty))

    if file_format in {"csv", "both"}:
        files.append(_write_csv(result, destination))

    return files


def _write_json(result: ExportResult, output_dir: Path, *, pretty: bool) -> Path:
    file_path = output_dir / f"{result.video_id}.json"
    file_path.write_text(
        json.dumps(result.to_dict(), ensure_ascii=False, indent=2 if pretty else None),
        encoding="utf-8",
    )
    return file_path


def _write_csv(result: ExportResult, output_dir: Path) -> Path:
    file_path = output_dir / f"{result.video_id}.csv"
    with file_path.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "video_id",
                "parent_id",
                "id",
                "username",
                "nickname",
                "text",
                "created_at",
                "avatar_url",
                "like_count",
                "reply_count",
                "is_reply",
            ],
        )
        writer.writeheader()
        for row in _iter_csv_rows(result.video_id, result.comments):
            writer.writerow(row)
    return file_path


def _iter_csv_rows(video_id: str, comments: list[Comment]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for comment in comments:
        rows.append(_comment_to_row(video_id, comment, parent_id="", is_reply=False))
        for reply in comment.replies:
            rows.append(_comment_to_row(video_id, reply, parent_id=comment.id, is_reply=True))
    return rows


def _comment_to_row(
    video_id: str,
    comment: Comment,
    *,
    parent_id: str,
    is_reply: bool,
) -> dict[str, object]:
    return {
        "video_id": video_id,
        "parent_id": parent_id,
        "id": comment.id,
        "username": comment.username,
        "nickname": comment.nickname,
        "text": comment.text,
        "created_at": comment.created_at,
        "avatar_url": comment.avatar_url,
        "like_count": comment.like_count,
        "reply_count": comment.reply_count,
        "is_reply": is_reply,
    }
