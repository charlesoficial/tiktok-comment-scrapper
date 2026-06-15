import csv
import json

import tiktok_exporter.exporter as exporter
from tiktok_exporter.models import Comment


class FakeClient:
    def iter_comments(self, video_id, *, limit, include_replies):
        reply = Comment(
            id="reply-1",
            username="reply_user",
            nickname="Reply User",
            text="reply text",
            created_at="2026-06-15T10:01:00",
            avatar_url="",
            like_count=0,
            reply_count=0,
        )
        comment = Comment(
            id="comment-1",
            username="comment_user",
            nickname="Comment User",
            text="comment text",
            created_at="2026-06-15T10:00:00",
            avatar_url="",
            like_count=3,
            reply_count=1,
            replies=[reply] if include_replies else [],
        )
        return [comment][:limit]

    def get_video_meta(self, video_id):
        return "caption", f"https://www.tiktok.com/@user/video/{video_id}"


def test_export_comments_writes_json(monkeypatch, tmp_path):
    monkeypatch.setattr(exporter, "TikTokClient", FakeClient)

    files = exporter.export_comments(
        "7418294751977327878",
        limit=1,
        output_dir=tmp_path,
        include_replies=True,
    )

    assert len(files) == 1
    data = json.loads(files[0].read_text(encoding="utf-8"))
    assert data["video_id"] == "7418294751977327878"
    assert data["comment_count"] == 1
    assert data["comments"][0]["replies"][0]["id"] == "reply-1"


def test_export_comments_writes_csv(monkeypatch, tmp_path):
    monkeypatch.setattr(exporter, "TikTokClient", FakeClient)

    files = exporter.export_comments(
        "7418294751977327878",
        limit=1,
        output_dir=tmp_path,
        include_replies=True,
        file_format="csv",
    )

    assert files[0].suffix == ".csv"
    with files[0].open(encoding="utf-8-sig", newline="") as file:
        rows = list(csv.DictReader(file))

    assert len(rows) == 2
    assert rows[0]["id"] == "comment-1"
    assert rows[0]["is_reply"] == "False"
    assert rows[1]["id"] == "reply-1"
    assert rows[1]["parent_id"] == "comment-1"
    assert rows[1]["is_reply"] == "True"


def test_export_comments_writes_both_formats(monkeypatch, tmp_path):
    monkeypatch.setattr(exporter, "TikTokClient", FakeClient)

    files = exporter.export_comments(
        "7418294751977327878",
        limit=1,
        output_dir=tmp_path,
        file_format="both",
    )

    assert {file.suffix for file in files} == {".json", ".csv"}
