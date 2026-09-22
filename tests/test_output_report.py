"""Tests for the output report on a job output (Horizon S4).

`JobOutput.report` carries what the produced file actually turned out to be,
measured from the encoded file rather than copied from the request, plus the
verdict of comparing those measurements against what was asked for.
"""

from __future__ import annotations

import json

from transcodely import types
from transcodely._codec.json_codec import deserialize
from transcodely.v1 import job_pb2

WIRE_JOB = {
    "job": {
        "id": "job_abc123def456",
        "status": "completed",
        "outputs": [
            {
                "id": "out_abc123def4567",
                "status": "completed",
                "report": {
                    "container": "mp4",
                    "duration_seconds": 30.5,
                    "checked_at": "2026-09-14T10:00:00Z",
                    "video": {
                        "codec": "hevc",
                        "profile": "main10",
                        "level": "4.0",
                        "pix_fmt": "yuv420p10le",
                        "width": 1920,
                        "height": 1080,
                        "frame_rate": 29.97,
                        "bitrate_kbps": 4800,
                        "hdr_format": "hdr10",
                        "color": {
                            "primaries": "bt2020",
                            "transfer": "smpte2084",
                            "matrix": "bt2020nc",
                            "range": "tv",
                        },
                    },
                    "audio": [
                        {
                            "codec": "aac",
                            "channels": 2,
                            "sample_rate_hz": 48000,
                            "bitrate_kbps": 128,
                            "language": "eng",
                        }
                    ],
                    "verdict": {
                        "matches_request": False,
                        "mismatches": [
                            {
                                "field": "video.codec",
                                "expected": "h264",
                                "actual": "hevc",
                            }
                        ],
                    },
                },
            }
        ],
    }
}


def _decode(payload: dict) -> job_pb2.GetJobResponse:
    return deserialize(json.dumps(payload).encode("utf-8"), job_pb2.GetJobResponse())


def test_report_types_are_reexported_from_the_facade() -> None:
    """`transcodely.types` re-exports every report message, each the generated class."""
    for name in (
        "OutputReport",
        "OutputReportVideo",
        "OutputReportColor",
        "OutputReportAudio",
        "OutputReportVerdict",
        "OutputReportMismatch",
        "OutputReportContentAware",
        "OutputReportContentAwareProbe",
    ):
        assert name in types.__all__, f"{name} missing from transcodely.types.__all__"
        assert getattr(types, name) is getattr(job_pb2, name)


def test_report_decodes_off_the_wire_and_carries_the_verdict() -> None:
    resp = _decode(WIRE_JOB)

    assert len(resp.job.outputs) == 1
    output = resp.job.outputs[0]
    assert output.HasField("report")

    report = output.report
    assert report.verdict.matches_request is False
    assert len(report.verdict.mismatches) == 1
    assert report.verdict.mismatches[0].field == "video.codec"
    assert report.verdict.mismatches[0].expected == "h264"
    assert report.verdict.mismatches[0].actual == "hevc"

    assert report.container == "mp4"
    assert report.duration_seconds == 30.5
    assert report.video.codec == "hevc"
    assert report.video.profile == "main10"
    assert report.video.pix_fmt == "yuv420p10le"
    assert report.video.width == 1920
    assert report.video.height == 1080
    assert report.video.hdr_format == "hdr10"
    assert report.video.color.transfer == "smpte2084"

    assert len(report.audio) == 1
    assert report.audio[0].codec == "aac"
    assert report.audio[0].sample_rate_hz == 48000
    assert report.audio[0].language == "eng"


def test_an_unmeasured_output_has_no_report() -> None:
    """Absence means "not measured", so it must stay distinguishable from an empty report."""
    resp = _decode({"job": {"id": "job_abc123def456", "outputs": [{"id": "out_abc123def4567"}]}})
    assert not resp.job.outputs[0].HasField("report")


def test_report_carries_what_the_per_title_search_decided() -> None:
    """An output encoded with per-title analysis reports the search that shaped it."""
    resp = _decode(
        {
            "job": {
                "id": "job_abc123def456",
                "outputs": [
                    {
                        "id": "out_abc123def4567",
                        "report": {
                            "container": "mp4",
                            "content_aware": {
                                "mode": "per_title",
                                "vmaf_target": 95,
                                "vmaf_achieved": 95.4,
                                "crf_chosen": 24,
                                "seed_crf": 28,
                                "met_target": True,
                                "probes": [
                                    {"crf": 28, "vmaf": 91.2, "bitrate_kbps": 3400.0},
                                    {"crf": 24, "vmaf": 95.4, "bitrate_kbps": 4800.5},
                                ],
                            },
                        },
                    }
                ],
            }
        }
    )

    report = resp.job.outputs[0].report
    assert report.HasField("content_aware")
    assert report.content_aware.mode == "per_title"
    assert report.content_aware.vmaf_target == 95
    assert report.content_aware.vmaf_achieved == 95.4
    assert report.content_aware.crf_chosen == 24
    assert report.content_aware.seed_crf == 28
    assert report.content_aware.met_target is True
    assert len(report.content_aware.probes) == 2
    assert report.content_aware.probes[0].crf == 28
    assert report.content_aware.probes[0].vmaf == 91.2
    assert report.content_aware.probes[0].bitrate_kbps == 3400.0
    assert report.content_aware.probes[1].crf == 24
    assert report.content_aware.probes[1].bitrate_kbps == 4800.5


def test_report_content_aware_curve_absent_on_older_workers() -> None:
    """Workers before 1.29.0 report the decision but not the curve."""
    resp = _decode(
        {
            "job": {
                "id": "job_abc123def456",
                "outputs": [
                    {
                        "id": "out_abc123def4567",
                        "report": {
                            "container": "mp4",
                            "content_aware": {
                                "mode": "per_title",
                                "vmaf_target": 95,
                                "vmaf_achieved": 95.4,
                                "crf_chosen": 24,
                            },
                        },
                    }
                ],
            }
        }
    )

    content_aware = resp.job.outputs[0].report.content_aware
    assert not content_aware.HasField("seed_crf")
    assert not content_aware.HasField("met_target")
    assert len(content_aware.probes) == 0


def test_an_ordinary_output_reports_no_content_aware_block() -> None:
    """Absence is the honest reading: no search shaped that encode."""
    resp = _decode(
        {
            "job": {
                "id": "job_abc123def456",
                "outputs": [{"id": "out_abc123def4567", "report": {"container": "mp4"}}],
            }
        }
    )
    assert not resp.job.outputs[0].report.HasField("content_aware")
