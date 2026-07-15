"""Internal helpers shared by resource modules."""

from __future__ import annotations

from typing import Any, Mapping, Optional, Union

from google.protobuf import json_format
from google.protobuf.descriptor import EnumDescriptor
from google.protobuf.message import Message

from .._codec.json_codec import expand_enum_value, simplify_enum_value, transform_enums_in_dict


def fill_from_dict(msg: Message, data: Mapping[str, Any]) -> Message:
    """Populate ``msg`` from a plain dict, accepting simplified-enum strings.

    The codec's enum-expand pass lets callers pass ``{"codec": "h264"}`` while
    the proto stores ``VIDEO_CODEC_H264`` (an int after parse).
    """
    payload = dict(data)
    transform_enums_in_dict(payload, msg.DESCRIPTOR, mode="expand")
    json_format.ParseDict(payload, msg, ignore_unknown_fields=True)
    return msg


def resolve_enum(value: Union[int, str], enum_desc: EnumDescriptor) -> int:
    """Resolve an enum value from either the raw proto int or a string.

    Strings may be the simplified lowercase wire form (``"standard"``,
    ``"processing"``) or the canonical proto name (``"JOB_PRIORITY_STANDARD"``) —
    both resolve to the same int via the codec's inbound ``expand`` rule. Ints
    pass through unchanged (proto3 enums are open, so an unknown int is the
    caller's responsibility). Used for scalar enum kwargs that are set on a
    request directly rather than through :func:`fill_from_dict`.
    """
    if isinstance(value, bool):  # bool is an int subclass — reject it explicitly.
        raise TypeError(f"{enum_desc.name} value must be an int or str, got bool: {value!r}")
    if isinstance(value, int):
        return value
    if isinstance(value, str):
        name = expand_enum_value(value, enum_desc)
        entry = enum_desc.values_by_name.get(name)
        if entry is None:
            allowed = ", ".join(
                simplify_enum_value(v.name, enum_desc) for v in enum_desc.values if v.number != 0
            )
            raise ValueError(
                f"unknown {enum_desc.name} value {value!r}; expected one of: {allowed}"
            )
        return int(entry.number)
    raise TypeError(f"{enum_desc.name} value must be an int or str, got {type(value).__name__}")


def assign_pagination(
    req_pagination: Any,
    *,
    limit: Optional[int] = None,
    cursor: Optional[str] = None,
    offset: Optional[int] = None,
) -> None:
    if limit is not None:
        req_pagination.limit = limit
    if cursor is not None:
        req_pagination.cursor = cursor
    if offset is not None:
        req_pagination.offset = offset
