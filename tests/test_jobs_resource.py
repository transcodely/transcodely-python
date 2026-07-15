"""Tests for the Jobs resource — origin/managed kwargs on create()."""

from __future__ import annotations

from typing import Any, Callable, Optional, Union

from transcodely.resources.jobs import Jobs
from transcodely.v1 import job_pb2


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


def _create_response(**job_kwargs: Any) -> job_pb2.CreateJobResponse:
    return job_pb2.CreateJobResponse(job=job_pb2.Job(id="job_1", **job_kwargs))


def test_create_sets_origin_and_managed_kwargs() -> None:
    t = FakeTransport({"Create": _create_response()})
    Jobs(t).create(  # type: ignore[arg-type]
        input_origin_id="ori_in",
        input_path="raw/source.mp4",
        output_origin_id="ori_out",
        output_path_template="{job_id}/{output_id}.{ext}",
        managed=False,
        outputs=[{"type": "mp4", "video": [{"codec": "h264", "resolution": "1080p"}]}],
    )
    req = t.calls[0][1]
    assert req.input_origin_id == "ori_in"
    assert req.input_path == "raw/source.mp4"
    assert req.output_origin_id == "ori_out"
    assert req.output_path_template == "{job_id}/{output_id}.{ext}"
    assert req.managed is False


def test_create_managed_true_needs_no_output_origin_id() -> None:
    t = FakeTransport({"Create": _create_response()})
    Jobs(t).create(  # type: ignore[arg-type]
        input_url="https://example.com/source.mp4",
        outputs=[{"type": "mp4", "video": [{"codec": "h264", "resolution": "1080p"}]}],
        managed=True,
    )
    req = t.calls[0][1]
    assert req.managed is True
    assert req.output_origin_id == ""


def test_create_without_origin_kwargs_leaves_fields_unset() -> None:
    """Additive-only: omitting the new kwargs must not touch their fields."""
    t = FakeTransport({"Create": _create_response()})
    Jobs(t).create(  # type: ignore[arg-type]
        input_url="https://example.com/source.mp4",
        outputs=[{"type": "mp4", "video": [{"codec": "h264", "resolution": "1080p"}]}],
    )
    req = t.calls[0][1]
    assert req.input_origin_id == ""
    assert req.input_path == ""
    assert req.output_origin_id == ""
    assert req.output_path_template == ""
    assert req.managed is False
    assert req.input_url == "https://example.com/source.mp4"


def test_create_request_escape_hatch_bypasses_kwargs() -> None:
    """The request= path is untouched by the new kwargs."""
    t = FakeTransport({"Create": _create_response()})
    explicit = job_pb2.CreateJobRequest(
        input_url="https://example.com/source.mp4",
        output_origin_id="ori_explicit",
        idempotency_key="idem_explicit",
    )
    Jobs(t).create(request=explicit)  # type: ignore[arg-type]
    req = t.calls[0][1]
    assert req is explicit
    assert req.output_origin_id == "ori_explicit"
    assert req.idempotency_key == "idem_explicit"
