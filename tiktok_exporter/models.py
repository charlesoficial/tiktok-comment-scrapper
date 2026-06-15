from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


def _format_timestamp(value: int | None) -> str:
    if not value:
        return ""
    return datetime.fromtimestamp(value).strftime("%Y-%m-%dT%H:%M:%S")


@dataclass(slots=True)
class Comment:
    id: str
    username: str
    nickname: str
    text: str
    created_at: str
    avatar_url: str
    like_count: int
    reply_count: int
    replies: list["Comment"] = field(default_factory=list)

    @classmethod
    def from_api(cls, payload: dict[str, Any]) -> "Comment":
        user = payload.get("user") or {}
        avatar = user.get("avatar_thumb") or {}
        avatars = avatar.get("url_list") or []

        return cls(
            id=str(payload.get("cid") or ""),
            username=str(user.get("unique_id") or ""),
            nickname=str(user.get("nickname") or ""),
            text=str(payload.get("text") or ""),
            created_at=_format_timestamp(payload.get("create_time")),
            avatar_url=str(avatars[0] if avatars else ""),
            like_count=int(payload.get("digg_count") or 0),
            reply_count=int(payload.get("reply_comment_total") or 0),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "username": self.username,
            "nickname": self.nickname,
            "text": self.text,
            "created_at": self.created_at,
            "avatar_url": self.avatar_url,
            "like_count": self.like_count,
            "reply_count": self.reply_count,
            "replies": [reply.to_dict() for reply in self.replies],
        }


@dataclass(slots=True)
class ExportResult:
    video_id: str
    caption: str
    video_url: str
    comment_count: int
    comments: list[Comment]

    def to_dict(self) -> dict[str, Any]:
        return {
            "video_id": self.video_id,
            "caption": self.caption,
            "video_url": self.video_url,
            "comment_count": self.comment_count,
            "comments": [comment.to_dict() for comment in self.comments],
        }
