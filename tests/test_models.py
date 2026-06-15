from tiktok_exporter.models import Comment


def test_comment_from_api_maps_expected_fields():
    comment = Comment.from_api(
        {
            "cid": "123",
            "text": "hello",
            "create_time": 1710000000,
            "digg_count": 7,
            "reply_comment_total": 2,
            "user": {
                "unique_id": "user123",
                "nickname": "User 123",
                "avatar_thumb": {"url_list": ["https://example.com/avatar.jpg"]},
            },
        }
    )

    assert comment.id == "123"
    assert comment.username == "user123"
    assert comment.nickname == "User 123"
    assert comment.text == "hello"
    assert comment.like_count == 7
    assert comment.reply_count == 2
    assert comment.avatar_url == "https://example.com/avatar.jpg"


def test_comment_to_dict_includes_replies():
    reply = Comment(
        id="reply-1",
        username="reply_user",
        nickname="Reply User",
        text="reply",
        created_at="2026-06-15T10:00:00",
        avatar_url="",
        like_count=0,
        reply_count=0,
    )
    comment = Comment(
        id="comment-1",
        username="comment_user",
        nickname="Comment User",
        text="comment",
        created_at="2026-06-15T09:00:00",
        avatar_url="",
        like_count=1,
        reply_count=1,
        replies=[reply],
    )

    data = comment.to_dict()

    assert data["id"] == "comment-1"
    assert data["replies"][0]["id"] == "reply-1"
