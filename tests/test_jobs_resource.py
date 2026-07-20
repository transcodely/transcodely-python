"""Tests for the Jobs resource: create/list request construction.

These pin the ergonomic kwargs the public docs promise — snake_case fields,
origin-mode inputs, delayed start, and enum values given as simplified lowercase
strings ("standard", "processing") or the raw proto int. Request construction is
verified against a duck-typed FakeTransport (no live server), mirroring
test_events_resource.py.
"""

from __future__ import annotations

from typing import Any, Callable, Optional, Union

import pytest

from transcodely.resources._helpers import resolve_enum
from transcodely.resources.jobs import Jobs
from transcodely.v1 import common_pb2, job_pb2, streaming_pb2, subtitles_pb2


class FakeTransport:
    """Duck-typed stand-in for Transport that returns canned responses per method."""

    def __init__(self, responses: dict[str, Union[Any, Callable[[Any], Any]]]) -> None:
        self._responses = responses
        self.calls: list[tuple[str, Any]] = []

    def unary(
        self,
        service_name: str,
        method_name: str,
        request: Any,
        response: Any,
        opts: Optional[Any] = None,
    ) -> Any:
        self.calls.append((method_name, request))
        r = self._responses[method_name]
        return r(request) if callable(r) else r


def _capture_create(**kwargs: Any) -> job_pb2.CreateJobRequest:
    """Run ``Jobs.create(**kwargs)`` and return the CreateJobRequest sent to the wire."""
    t = FakeTransport({"Create": job_pb2.CreateJobResponse(job=job_pb2.Job(id="job_created"))})
    Jobs(t).create(**kwargs)  # type: ignore[arg-type]
    return t.calls[0][1]


def _list_first_request(**kwargs: Any) -> job_pb2.ListJobsRequest:
    """Run ``Jobs.list(**kwargs)`` and return the ListJobsRequest for the first page."""
    resp = job_pb2.ListJobsResponse(
        jobs=[job_pb2.Job(id="job_1")],
        pagination=common_pb2.PaginationResponse(next_cursor=""),
    )
    t = FakeTransport({"List": resp})
    Jobs(t).list(**kwargs).items  # `.items` triggers the first fetch  # type: ignore[arg-type]
    return t.calls[0][1]


# ---- Jobs.create — individual kwargs ----------------------------------------


class TestJobsCreateKwargs:
    def test_direct_url_mode_with_output_origin(self) -> None:
        req = _capture_create(input_url="gs://b/in.mp4", output_origin_id="ori_x9y8z7w6v5")
        assert req.input_url == "gs://b/in.mp4"
        assert req.output_origin_id == "ori_x9y8z7w6v5"

    def test_origin_input_mode_with_path(self) -> None:
        req = _capture_create(
            input_origin_id="ori_input12345",
            input_path="uploads/my-video.mp4",
            output_origin_id="ori_output6789",
        )
        assert req.input_origin_id == "ori_input12345"
        assert req.input_path == "uploads/my-video.mp4"
        assert req.output_origin_id == "ori_output6789"
        assert req.input_url == ""

    def test_input_video_id_retro_caption_mode(self) -> None:
        # F5: retro-caption a hosted video — input_video_id source with a single
        # captions-only output (no video[], no type) carrying a generate track.
        req = _capture_create(
            input_video_id="vid_a1b2c3d4e5f6g7",
            outputs=[{"subtitle_tracks": [{"operation": "generate", "language": "auto"}]}],
        )
        assert req.input_video_id == "vid_a1b2c3d4e5f6g7"
        assert req.input_url == ""
        track = req.outputs[0].subtitle_tracks[0]
        assert track.operation == subtitles_pb2.SUBTITLE_OPERATION_GENERATE
        assert track.language == "auto"

    def test_priority_as_lowercase_string(self) -> None:
        req = _capture_create(input_url="gs://b/in.mp4", priority="standard")
        assert req.priority == job_pb2.JOB_PRIORITY_STANDARD

    def test_priority_as_int_backward_compatible(self) -> None:
        req = _capture_create(input_url="gs://b/in.mp4", priority=job_pb2.JOB_PRIORITY_PREMIUM)
        assert req.priority == job_pb2.JOB_PRIORITY_PREMIUM

    def test_priority_as_canonical_enum_name(self) -> None:
        req = _capture_create(input_url="gs://b/in.mp4", priority="JOB_PRIORITY_ECONOMY")
        assert req.priority == job_pb2.JOB_PRIORITY_ECONOMY

    def test_delayed_start(self) -> None:
        req = _capture_create(
            input_origin_id="ori_in",
            input_path="uploads/v.mp4",
            output_origin_id="ori_out",
            delayed_start=True,
        )
        assert req.delayed_start is True

    def test_managed(self) -> None:
        req = _capture_create(input_url="gs://b/in.mp4", managed=True)
        assert req.managed is True

    def test_managed_minimal_shape_without_output_origin(self) -> None:
        # Managed apps write to Transcodely-managed storage, so output_origin_id
        # is not required — the quickstart shape.
        req = _capture_create(input_url="https://storage.example.com/source.mp4", managed=True)
        assert req.managed is True
        assert req.output_origin_id == ""

    def test_managed_omitted_leaves_field_default(self) -> None:
        req = _capture_create(input_url="gs://b/in.mp4", output_origin_id="ori_x")
        assert req.managed is False

    def test_output_path_template(self) -> None:
        req = _capture_create(
            input_url="gs://b/in.mp4",
            output_origin_id="ori_x9y8z7w6v5",
            output_path_template="videos/{job_id}/{output}",
        )
        assert req.output_path_template == "videos/{job_id}/{output}"
        # Survives the wire: optional-field presence is set and round-trips.
        roundtrip = job_pb2.CreateJobRequest.FromString(req.SerializeToString())
        assert roundtrip.output_path_template == "videos/{job_id}/{output}"

    def test_output_path_template_with_origin_mode(self) -> None:
        req = _capture_create(
            input_origin_id="ori_in",
            input_path="uploads/v.mp4",
            output_origin_id="ori_out",
            output_path_template="renders/{job_id}",
        )
        assert req.output_path_template == "renders/{job_id}"
        assert req.input_origin_id == "ori_in"
        assert req.output_origin_id == "ori_out"

    def test_webhook_url(self) -> None:
        req = _capture_create(input_url="gs://b/in.mp4", webhook_url="https://x.test/hook")
        assert req.webhook_url == "https://x.test/hook"

    def test_metadata(self) -> None:
        req = _capture_create(
            input_url="gs://b/in.mp4",
            metadata={"user_id": "usr_12345", "project": "marketing-videos"},
        )
        assert dict(req.metadata) == {"user_id": "usr_12345", "project": "marketing-videos"}

    def test_clip_as_dict(self) -> None:
        req = _capture_create(
            input_url="gs://b/in.mp4",
            clip={"start_seconds": 2, "end_seconds": 7},
        )
        assert req.HasField("clip")
        assert req.clip.start_seconds == 2
        assert req.clip.end_seconds == 7
        # Survives the wire: the sub-message round-trips.
        roundtrip = job_pb2.CreateJobRequest.FromString(req.SerializeToString())
        assert roundtrip.clip.start_seconds == 2
        assert roundtrip.clip.end_seconds == 7

    def test_clip_as_message(self) -> None:
        req = _capture_create(
            input_url="gs://b/in.mp4",
            clip=job_pb2.ClipConfig(start_seconds=1.5, end_seconds=9),
        )
        assert req.HasField("clip")
        assert req.clip.start_seconds == 1.5
        assert req.clip.end_seconds == 9

    def test_clip_open_ended_end_defaults_to_zero(self) -> None:
        # Omitting end_seconds means "end of input"; the double defaults to 0.
        req = _capture_create(input_url="gs://b/in.mp4", clip={"start_seconds": 10})
        assert req.HasField("clip")
        assert req.clip.start_seconds == 10
        assert req.clip.end_seconds == 0

    def test_clip_omitted_leaves_field_unset(self) -> None:
        req = _capture_create(input_url="gs://b/in.mp4")
        assert not req.HasField("clip")

    def test_outputs_accept_simplified_enum_strings(self) -> None:
        req = _capture_create(
            input_url="gs://b/in.mp4",
            output_origin_id="ori_x",
            outputs=[
                {
                    "type": "hls",
                    "video": [{"codec": "h264", "resolution": "1080p", "quality": "standard"}],
                }
            ],
        )
        out = req.outputs[0]
        assert out.type == common_pb2.OUTPUT_FORMAT_HLS
        assert out.video[0].codec == common_pb2.VIDEO_CODEC_H264
        assert out.video[0].resolution == common_pb2.RESOLUTION_1080P
        assert out.video[0].quality == common_pb2.QUALITY_TIER_STANDARD

    def test_outputs_preset_reference(self) -> None:
        req = _capture_create(
            input_url="gs://b/in.mp4",
            output_origin_id="ori_x",
            outputs=[{"preset": "pst_x9y8z7w6v5"}, {"preset": "web_720p_standard"}],
        )
        assert [o.preset for o in req.outputs] == ["pst_x9y8z7w6v5", "web_720p_standard"]

    def test_outputs_nested_segment_enum_string(self) -> None:
        req = _capture_create(
            input_origin_id="ori_in",
            input_path="uploads/source.mp4",
            output_origin_id="ori_out",
            outputs=[
                {
                    "type": "hls",
                    "video": [{"codec": "h264", "resolution": "1080p", "quality": "standard"}],
                    "segments": {"duration": 6, "gop_alignment": "aligned"},
                }
            ],
        )
        seg = req.outputs[0].segments
        assert seg.duration == 6
        assert seg.gop_alignment == streaming_pb2.GOP_ALIGNMENT_MODE_ALIGNED


# ---- Jobs.create — combined + idempotency + escape hatch ---------------------


class TestJobsCreateCombined:
    def test_all_kwargs_together(self) -> None:
        req = _capture_create(
            input_origin_id="ori_input12345",
            input_path="uploads/my-video.mp4",
            output_origin_id="ori_output6789",
            output_path_template="videos/{job_id}/{output}",
            managed=True,
            priority="premium",
            delayed_start=True,
            webhook_url="https://x.test/hook",
            metadata={"batch": "b1"},
            clip={"start_seconds": 2, "end_seconds": 7},
            idempotency_key="key-123",
            outputs=[
                {"type": "mp4", "video": [{"codec": "h264", "resolution": "1080p"}]},
                {
                    "type": "hls",
                    "video": [
                        {"codec": "h264", "resolution": "1080p", "quality": "standard"},
                        {"codec": "h264", "resolution": "720p", "quality": "economy"},
                    ],
                },
            ],
        )
        assert req.input_origin_id == "ori_input12345"
        assert req.input_path == "uploads/my-video.mp4"
        assert req.output_origin_id == "ori_output6789"
        assert req.output_path_template == "videos/{job_id}/{output}"
        assert req.managed is True
        assert req.priority == job_pb2.JOB_PRIORITY_PREMIUM
        assert req.delayed_start is True
        assert req.webhook_url == "https://x.test/hook"
        assert dict(req.metadata) == {"batch": "b1"}
        assert req.clip.start_seconds == 2
        assert req.clip.end_seconds == 7
        assert req.idempotency_key == "key-123"
        assert len(req.outputs) == 2
        assert req.outputs[1].video[1].quality == common_pb2.QUALITY_TIER_ECONOMY

    def test_returns_job_from_response(self) -> None:
        t = FakeTransport(
            {"Create": job_pb2.CreateJobResponse(job=job_pb2.Job(id="job_abc", progress=0))}
        )
        job = Jobs(t).create(input_url="gs://b/in.mp4")  # type: ignore[arg-type]
        assert job.id == "job_abc"

    def test_idempotency_key_autofilled_when_omitted(self) -> None:
        req = _capture_create(input_url="gs://b/in.mp4")
        assert req.idempotency_key  # non-empty uuid4

    def test_explicit_idempotency_key_preserved(self) -> None:
        req = _capture_create(input_url="gs://b/in.mp4", idempotency_key="upload_usr12345_x")
        assert req.idempotency_key == "upload_usr12345_x"

    def test_request_escape_hatch_forwarded_and_idempotency_autofilled(self) -> None:
        built = job_pb2.CreateJobRequest(
            input_url="gs://b/in.mp4",
            output_path_template="videos/{job_id}",
            managed=True,
        )
        req = _capture_create(request=built)
        assert req.output_path_template == "videos/{job_id}"
        assert req.managed is True
        assert req.idempotency_key  # auto-filled since the built request had none

    def test_request_escape_hatch_preserves_its_own_idempotency_key(self) -> None:
        built = job_pb2.CreateJobRequest(input_url="gs://b/in.mp4", idempotency_key="mine")
        req = _capture_create(request=built)
        assert req.idempotency_key == "mine"

    def test_request_escape_hatch_ignores_convenience_kwargs(self) -> None:
        built = job_pb2.CreateJobRequest(input_url="from-request")
        req = _capture_create(request=built, input_url="from-kwarg", priority="premium")
        assert req.input_url == "from-request"
        assert req.priority == job_pb2.JOB_PRIORITY_UNSPECIFIED

    def test_conflicting_input_modes_not_validated_client_side(self) -> None:
        # The SDK is a thin client (like the TS/Go SDKs): it forwards both input
        # fields and lets the server's CEL rule reject the combination, rather
        # than raising locally.
        req = _capture_create(input_url="gs://b/in.mp4", input_origin_id="ori_x")
        assert req.input_url == "gs://b/in.mp4"
        assert req.input_origin_id == "ori_x"


# ---- Jobs.create — every collected docs call shape --------------------------

# Each entry is a kwargs dict copied from a Python fence in the public docs.
DOCS_CREATE_SHAPES: list[dict[str, Any]] = [
    # getting-started/sdks/python, resources/metadata, resources/idempotency,
    # core-concepts/jobs, api-reference, getting-started/quickstart
    {
        "input_url": "https://storage.example.com/source.mp4",
        "output_origin_id": "ori_x9y8z7w6v5",
        "outputs": [
            {
                "type": "hls",
                "video": [
                    {"codec": "h264", "resolution": "1080p"},
                    {"codec": "h264", "resolution": "720p"},
                ],
            }
        ],
    },
    # getting-started/quickstart, README (managed app — no output origin required)
    {
        "input_url": "https://storage.example.com/source.mp4",
        "managed": True,
        "outputs": [
            {
                "type": "hls",
                "video": [
                    {"codec": "h264", "resolution": "1080p"},
                    {"codec": "h264", "resolution": "720p"},
                ],
            }
        ],
    },
    # api-reference/jobs, getting-started/quickstart, core-concepts/jobs
    {
        "input_url": "gs://my-bucket/uploads/video.mp4",
        "output_origin_id": "ori_x9y8z7w6v5",
        "outputs": [
            {
                "type": "mp4",
                "video": [{"codec": "h264", "resolution": "1080p", "quality": "standard"}],
            }
        ],
        "priority": "standard",
    },
    # getting-started/first-job (metadata + priority)
    {
        "input_url": "https://storage.example.com/uploads/interview.mp4",
        "output_origin_id": "ori_x9y8z7w6v5",
        "outputs": [
            {
                "type": "mp4",
                "video": [{"codec": "h264", "resolution": "1080p", "quality": "standard"}],
            },
            {
                "type": "webm",
                "video": [{"codec": "vp9", "resolution": "720p", "quality": "economy"}],
            },
        ],
        "priority": "standard",
        "metadata": {"user_id": "usr_12345", "project": "marketing-videos"},
    },
    # getting-started/first-job (preset outputs)
    {
        "input_url": "https://storage.example.com/uploads/interview.mp4",
        "output_origin_id": "ori_x9y8z7w6v5",
        "outputs": [{"preset": "pst_x9y8z7w6v5"}, {"preset": "web_720p_standard"}],
        "priority": "standard",
    },
    # resources/idempotency, api-reference (explicit idempotency key)
    {
        "input_url": "gs://my-bucket/video.mp4",
        "output_origin_id": "ori_x9y8z7w6v5",
        "outputs": [
            {
                "type": "mp4",
                "video": [{"codec": "h264", "resolution": "1080p", "quality": "standard"}],
            }
        ],
        "idempotency_key": "upload_usr12345_2026-01-15T10:30:00Z",
    },
    # resources/metadata (rich metadata)
    {
        "input_url": "gs://my-bucket/video.mp4",
        "output_origin_id": "ori_x9y8z7w6v5",
        "outputs": [
            {
                "type": "mp4",
                "video": [{"codec": "h264", "resolution": "1080p", "quality": "standard"}],
            }
        ],
        "metadata": {
            "user_id": "usr_12345",
            "campaign": "summer-2026",
            "source": "upload-api",
            "content_id": "vid_abc123",
        },
    },
    # guides/storage-setup, guides/batch-encoding (origin mode)
    {
        "input_origin_id": "ori_input12345",
        "input_path": "uploads/my-video.mp4",
        "output_origin_id": "ori_output6789",
        "outputs": [
            {
                "type": "mp4",
                "video": [{"codec": "h264", "resolution": "1080p", "quality": "standard"}],
            }
        ],
    },
    # guides/batch-encoding (origin mode + idempotency key)
    {
        "input_origin_id": "ori_input12345",
        "input_path": "uploads/episode-01.mp4",
        "output_origin_id": "ori_output6789",
        "idempotency_key": "batch_2026-02-28_episode-01.mp4",
        "outputs": [
            {
                "type": "mp4",
                "video": [{"codec": "h264", "resolution": "1080p", "quality": "standard"}],
            }
        ],
    },
    # guides/delayed-jobs (origin mode + delayed_start + multi-output)
    {
        "input_origin_id": "ori_input12345",
        "input_path": "uploads/my-video.mp4",
        "output_origin_id": "ori_output6789",
        "delayed_start": True,
        "outputs": [
            {
                "type": "mp4",
                "video": [{"codec": "h264", "resolution": "1080p", "quality": "standard"}],
            },
            {
                "type": "hls",
                "video": [
                    {"codec": "h264", "resolution": "1080p", "quality": "standard"},
                    {"codec": "h264", "resolution": "720p", "quality": "standard"},
                    {"codec": "h264", "resolution": "480p", "quality": "economy"},
                ],
            },
        ],
    },
    # guides/adaptive-streaming (origin mode + segments config)
    {
        "input_origin_id": "ori_input12345",
        "input_path": "uploads/source.mp4",
        "output_origin_id": "ori_output6789",
        "outputs": [
            {
                "type": "hls",
                "video": [
                    {"codec": "h264", "resolution": "1080p", "quality": "standard"},
                    {"codec": "h264", "resolution": "720p", "quality": "standard"},
                    {"codec": "h264", "resolution": "480p", "quality": "standard"},
                ],
                "segments": {"duration": 6, "gop_alignment": "aligned"},
            }
        ],
    },
    # getting-started/sdks/python (intentional error example: empty outputs)
    {"input_url": "...", "outputs": []},
]


@pytest.mark.parametrize("shape", DOCS_CREATE_SHAPES)
def test_docs_create_shapes_build_valid_requests(shape: dict[str, Any]) -> None:
    req = _capture_create(**shape)
    assert isinstance(req, job_pb2.CreateJobRequest)
    # An input mode is always present in the collected shapes.
    assert req.input_url or req.input_origin_id
    # Idempotency key is auto-filled unless the caller supplied one.
    assert req.idempotency_key
    if "idempotency_key" in shape:
        assert req.idempotency_key == shape["idempotency_key"]


# ---- Jobs.list --------------------------------------------------------------


class TestJobsList:
    def test_no_arguments(self) -> None:
        req = _list_first_request()
        assert req.HasField("status") is False
        assert req.pagination.limit == 0
        assert req.pagination.offset == 0

    def test_status_as_lowercase_string(self) -> None:
        req = _list_first_request(status="processing")
        assert req.status == job_pb2.JOB_STATUS_PROCESSING

    def test_status_as_int_backward_compatible(self) -> None:
        req = _list_first_request(status=job_pb2.JOB_STATUS_COMPLETED)
        assert req.status == job_pb2.JOB_STATUS_COMPLETED

    def test_limit_kwarg(self) -> None:
        req = _list_first_request(limit=50)
        assert req.pagination.limit == 50

    def test_limit_and_offset_kwargs(self) -> None:
        req = _list_first_request(limit=10, offset=20)
        assert req.pagination.limit == 10
        assert req.pagination.offset == 20

    def test_pagination_dict(self) -> None:
        req = _list_first_request(pagination={"limit": 50})
        assert req.pagination.limit == 50

    def test_status_string_with_pagination_dict(self) -> None:
        req = _list_first_request(status="processing", pagination={"limit": 20})
        assert req.status == job_pb2.JOB_STATUS_PROCESSING
        assert req.pagination.limit == 20

    def test_pagination_dict_offset_and_cursor(self) -> None:
        req = _list_first_request(pagination={"limit": 5, "offset": 15, "cursor": "c0"})
        assert req.pagination.limit == 5
        assert req.pagination.offset == 15
        assert req.pagination.cursor == "c0"

    def test_explicit_kwargs_win_over_pagination_dict(self) -> None:
        req = _list_first_request(limit=99, offset=1, pagination={"limit": 5, "offset": 50})
        assert req.pagination.limit == 99
        assert req.pagination.offset == 1

    def test_auto_paging_advances_cursor(self) -> None:
        page1 = job_pb2.ListJobsResponse(
            jobs=[job_pb2.Job(id="job_1")],
            pagination=common_pb2.PaginationResponse(next_cursor="c1"),
        )
        page2 = job_pb2.ListJobsResponse(
            jobs=[job_pb2.Job(id="job_2")],
            pagination=common_pb2.PaginationResponse(next_cursor=""),
        )

        def respond(req: job_pb2.ListJobsRequest) -> job_pb2.ListJobsResponse:
            return page2 if req.pagination.cursor == "c1" else page1

        t = FakeTransport({"List": respond})
        page = Jobs(t).list(limit=1)  # type: ignore[arg-type]
        assert [j.id for j in page.auto_paging_iter()] == ["job_1", "job_2"]
        # First fetch carries no cursor; second carries the returned cursor.
        assert t.calls[0][1].pagination.cursor == ""
        assert t.calls[1][1].pagination.cursor == "c1"

    def test_pagination_dict_cursor_seeds_only_first_page(self) -> None:
        page1 = job_pb2.ListJobsResponse(
            jobs=[job_pb2.Job(id="job_1")],
            pagination=common_pb2.PaginationResponse(next_cursor="c1"),
        )
        page2 = job_pb2.ListJobsResponse(
            jobs=[job_pb2.Job(id="job_2")],
            pagination=common_pb2.PaginationResponse(next_cursor=""),
        )
        t = FakeTransport({"List": lambda req: page2 if req.pagination.cursor == "c1" else page1})
        page = Jobs(t).list(pagination={"cursor": "seed"})  # type: ignore[arg-type]
        list(page.auto_paging_iter())
        # Seed cursor used for the first fetch, server cursor for the second.
        assert t.calls[0][1].pagination.cursor == "seed"
        assert t.calls[1][1].pagination.cursor == "c1"


# ---- resolve_enum helper ----------------------------------------------------


class TestResolveEnum:
    STATUS = job_pb2.JobStatus.DESCRIPTOR
    PRIORITY = job_pb2.JobPriority.DESCRIPTOR

    def test_simplified_string(self) -> None:
        assert resolve_enum("processing", self.STATUS) == job_pb2.JOB_STATUS_PROCESSING
        assert resolve_enum("premium", self.PRIORITY) == job_pb2.JOB_PRIORITY_PREMIUM

    def test_canonical_name_string(self) -> None:
        assert resolve_enum("JOB_STATUS_FAILED", self.STATUS) == job_pb2.JOB_STATUS_FAILED

    def test_int_passthrough(self) -> None:
        assert (
            resolve_enum(job_pb2.JOB_STATUS_COMPLETED, self.STATUS) == job_pb2.JOB_STATUS_COMPLETED
        )
        assert resolve_enum(7, self.STATUS) == 7

    def test_unknown_string_raises_value_error(self) -> None:
        with pytest.raises(ValueError, match="unknown JobStatus value"):
            resolve_enum("bogus", self.STATUS)

    def test_bool_rejected(self) -> None:
        with pytest.raises(TypeError, match="got bool"):
            resolve_enum(True, self.STATUS)
