"""JSON serialization for the Transcodely wire format.

Wraps protobuf's ``MessageToDict`` / ``ParseDict`` with snake_case field names
and lowercase simplified enum values, mirroring ``internal/connect/codec.go``
on the server. Behavior must stay bit-identical with the TypeScript and Go
codecs — see the cross-language conformance suite.
"""

from __future__ import annotations

import json
import re
from typing import Any, TypeVar

from google.protobuf import json_format
from google.protobuf.descriptor import EnumDescriptor, FieldDescriptor
from google.protobuf.message import Message

T = TypeVar("T", bound=Message)

_CAMEL_BOUNDARY = re.compile(r"(?<!^)(?=[A-Z])")


def camel_to_screaming_snake(name: str) -> str:
    """``"JobStatus" → "JOB_STATUS"``; ``"HLSSegmentFormat" → "HLS_SEGMENT_FORMAT"``."""
    out: list[str] = []
    for i, ch in enumerate(name):
        if i > 0 and ch.isupper():
            prev = name[i - 1]
            nxt = name[i + 1] if i + 1 < len(name) else ""
            if prev.islower() or (nxt and nxt.islower()):
                out.append("_")
        out.append(ch.upper())
    return "".join(out)


def enum_prefix(enum_desc: EnumDescriptor) -> str:
    """``"JobStatus" → "JOB_STATUS_"`` — the prefix the server strips/restores."""
    return camel_to_screaming_snake(enum_desc.name) + "_"


def simplify_enum_value(value: str, enum_desc: EnumDescriptor) -> str:
    """``"JOB_STATUS_PENDING" → "pending"``."""
    prefix = enum_prefix(enum_desc)
    if value.startswith(prefix):
        return value[len(prefix) :].lower()
    return value.lower()


def expand_enum_value(value: str, enum_desc: EnumDescriptor) -> str:
    """``"pending" → "JOB_STATUS_PENDING"`` (using the enum's full-name set)."""
    if enum_desc.values_by_name.get(value) is not None:
        return value
    candidate = enum_prefix(enum_desc) + value.upper()
    if enum_desc.values_by_name.get(candidate) is not None:
        return candidate
    return value


def transform_enums_in_dict(
    obj: Any,
    msg_desc: Any,
    *,
    mode: str,
) -> None:
    """Recursively walk a JSON dict/list tree and translate every enum string.

    ``mode`` is ``"simplify"`` (outbound) or ``"expand"`` (inbound).
    """
    if not isinstance(obj, dict):
        return

    for field in msg_desc.fields:
        key = _pick_key(obj, field)
        if key is None:
            continue
        v = obj[key]
        if v is None:
            continue
        _transform_field(obj, key, v, field, mode)


def _pick_key(obj: dict[str, Any], field: FieldDescriptor) -> str | None:
    # camelCase JSON name (default protobuf JSON) takes precedence; proto name
    # accepted as fallback for tolerant parsing.
    if field.json_name in obj:
        return field.json_name
    if field.name in obj:
        return field.name
    return None


def _transform_field(
    parent: dict[str, Any],
    key: str,
    v: Any,
    field: FieldDescriptor,
    mode: str,
) -> None:
    # Map fields: protobuf models them as repeated message of generated entry types.
    if field.message_type and field.message_type.GetOptions().map_entry:
        if not isinstance(v, dict):
            return
        value_field = field.message_type.fields_by_name["value"]
        if value_field.type == FieldDescriptor.TYPE_ENUM:
            enum_desc = value_field.enum_type
            for k, item in list(v.items()):
                if isinstance(item, str):
                    v[k] = _apply_enum(item, enum_desc, mode)
        elif value_field.type == FieldDescriptor.TYPE_MESSAGE:
            for k, item in list(v.items()):
                if isinstance(item, dict):
                    transform_enums_in_dict(item, value_field.message_type, mode=mode)
        return

    if field.is_repeated:
        if not isinstance(v, list):
            return
        if field.type == FieldDescriptor.TYPE_ENUM:
            enum_desc = field.enum_type
            for i, item in enumerate(v):
                if isinstance(item, str):
                    v[i] = _apply_enum(item, enum_desc, mode)
        elif field.type == FieldDescriptor.TYPE_MESSAGE:
            for item in v:
                if isinstance(item, dict):
                    transform_enums_in_dict(item, field.message_type, mode=mode)
        return

    if field.type == FieldDescriptor.TYPE_ENUM:
        if isinstance(v, str):
            parent[key] = _apply_enum(v, field.enum_type, mode)
        return

    if field.type == FieldDescriptor.TYPE_MESSAGE:
        if isinstance(v, dict):
            transform_enums_in_dict(v, field.message_type, mode=mode)


def _apply_enum(value: str, enum_desc: EnumDescriptor, mode: str) -> str:
    return (
        simplify_enum_value(value, enum_desc)
        if mode == "simplify"
        else expand_enum_value(value, enum_desc)
    )


def _message_to_dict(msg: Message) -> dict[str, Any]:
    """``MessageToDict`` with the right kwarg for both protobuf v5 and v6."""
    try:
        return json_format.MessageToDict(  # type: ignore[call-arg]
            msg,
            preserving_proto_field_name=True,
            always_print_fields_with_no_presence=True,
            use_integers_for_enums=False,
        )
    except TypeError:
        # protobuf < 5.27 used `including_default_value_fields`
        return json_format.MessageToDict(  # type: ignore[call-arg]
            msg,
            preserving_proto_field_name=True,
            including_default_value_fields=True,
            use_integers_for_enums=False,
        )


def serialize(msg: Message) -> bytes:
    """Encode a proto message as Transcodely-wire JSON bytes."""
    obj = _message_to_dict(msg)
    transform_enums_in_dict(obj, msg.DESCRIPTOR, mode="simplify")
    return json.dumps(obj).encode("utf-8")


def deserialize(data: bytes, msg: T) -> T:
    """Decode Transcodely-wire JSON bytes into ``msg`` (mutated in place, returned for chaining)."""
    if not data:
        return msg
    parsed = json.loads(data.decode("utf-8"))
    if isinstance(parsed, dict):
        transform_enums_in_dict(parsed, msg.DESCRIPTOR, mode="expand")
    json_format.ParseDict(parsed, msg, ignore_unknown_fields=True)
    return msg


__all__ = [
    "camel_to_screaming_snake",
    "deserialize",
    "enum_prefix",
    "expand_enum_value",
    "serialize",
    "simplify_enum_value",
    "transform_enums_in_dict",
]
