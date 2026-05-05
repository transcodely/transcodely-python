"""Internal helpers shared by resource modules."""

from __future__ import annotations

from typing import Any, Mapping, Optional

from google.protobuf import json_format
from google.protobuf.message import Message

from .._codec.json_codec import transform_enums_in_dict


def fill_from_dict(msg: Message, data: Mapping[str, Any]) -> Message:
    """Populate ``msg`` from a plain dict, accepting simplified-enum strings.

    The codec's enum-expand pass lets callers pass ``{"codec": "h264"}`` while
    the proto stores ``VIDEO_CODEC_H264`` (an int after parse).
    """
    payload = dict(data)
    transform_enums_in_dict(payload, msg.DESCRIPTOR, mode="expand")
    json_format.ParseDict(payload, msg, ignore_unknown_fields=True)
    return msg


def assign_pagination(req_pagination: Any, *, limit: Optional[int], cursor: Optional[str]) -> None:
    if limit is not None:
        req_pagination.limit = limit
    if cursor is not None:
        req_pagination.cursor = cursor
