"""Wire-format tests for transcripts and insights.

Pins the snake_case field names and lowercase enum values of the transcript
renditions, transcript style and insights status, in both directions.
"""

from __future__ import annotations

import json

import transcodely
from transcodely import types
from transcodely._codec.json_codec import deserialize, serialize
from transcodely.v1 import job_pb2, subtitles_pb2


def test_decodes_job_insights() -> None:
    payload = json.dumps(
        {
            "job": {
                "id": "job_a1b2c3d4e5f6",
                "insights": [
                    {
                        "output_id": "out_a1b2c3d4e5f6g7",
                        "language": "eng",
                        "status": "ready",
                        "summary": "A short talk.",
                        "key_points": ["one", "two"],
                        "questions": [
                            {"question": "Why?", "answer": "Because.", "start_seconds": 12.5}
                        ],
                        "terms": [
                            {"term": "GOP", "definition": "Group of pictures.", "start_seconds": 3}
                        ],
                        "highlights": [
                            {"text": "verbatim", "start_seconds": 1, "end_seconds": 2.5}
                        ],
                        "chapters": [{"start_seconds": 0, "title": "Intro"}],
                        "generated_at": "2026-10-24T10:00:00Z",
                    }
                ],
            }
        }
    ).encode()
    resp = deserialize(payload, job_pb2.GetJobResponse())
    ins = resp.job.insights[0]
    assert ins.status == subtitles_pb2.INSIGHTS_STATUS_READY
    assert list(ins.key_points) == ["one", "two"]
    assert ins.questions[0].start_seconds == 12.5
    assert ins.terms[0].term == "GOP"
    assert ins.highlights[0].end_seconds == 2.5
    assert ins.chapters[0].title == "Intro"
    assert ins.generated_at.seconds > 0


def test_decodes_transcript_renditions_and_style() -> None:
    payload = json.dumps(
        {
            "transcript_style": "literal",
            "transcript_renditions": [
                {"format": "json", "storage_key": "a/t.json", "url": "gs://b/a/t.json"},
                {
                    "format": "txt",
                    "storage_key": "a/t.txt",
                    "url": "gs://b/a/t.txt",
                    "signed_url": "https://x/t.txt",
                },
                {"format": "md", "storage_key": "a/t.md", "url": "gs://b/a/t.md"},
            ],
        }
    ).encode()
    res = deserialize(payload, subtitles_pb2.SubtitleResult())
    assert res.transcript_style == subtitles_pb2.TRANSCRIPT_STYLE_LITERAL
    assert [r.format for r in res.transcript_renditions] == [
        subtitles_pb2.TRANSCRIPT_FORMAT_JSON,
        subtitles_pb2.TRANSCRIPT_FORMAT_TXT,
        subtitles_pb2.TRANSCRIPT_FORMAT_MD,
    ]
    assert res.transcript_renditions[1].signed_url == "https://x/t.txt"


def test_encodes_transcript_and_insights_options() -> None:
    track = subtitles_pb2.SubtitleTrack(
        operation=subtitles_pb2.SUBTITLE_OPERATION_GENERATE,
        transcript=subtitles_pb2.TranscriptOptions(style=subtitles_pb2.TRANSCRIPT_STYLE_CLEAN),
        insights=subtitles_pb2.InsightsOptions(enabled=True, hint="lecture"),
    )
    body = json.loads(serialize(track))
    assert body["operation"] == "generate"
    assert body["transcript"] == {"style": "clean"}
    assert body["insights"] == {"enabled": True, "hint": "lecture"}


def test_new_types_are_re_exported() -> None:
    for name in (
        "TranscriptOptions",
        "InsightsOptions",
        "TranscriptRendition",
        "TranscriptInsights",
        "InsightsQuestion",
        "InsightsTerm",
        "InsightsHighlight",
        "TranscriptStyle",
        "TranscriptFormat",
        "InsightsStatus",
        "GetSeoMarkupRequest",
        "GetSeoMarkupResponse",
    ):
        assert name in types.__all__, name
        assert getattr(types, name) is not None
    for name in (
        "TranscriptOptions",
        "InsightsOptions",
        "TranscriptRendition",
        "TranscriptInsights",
    ):
        assert name in transcodely.__all__, name
