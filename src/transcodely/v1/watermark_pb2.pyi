from buf.validate import validate_pb2 as _validate_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class WatermarkAnchor(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    WATERMARK_ANCHOR_UNSPECIFIED: _ClassVar[WatermarkAnchor]
    WATERMARK_ANCHOR_TOP_LEFT: _ClassVar[WatermarkAnchor]
    WATERMARK_ANCHOR_TOP_CENTER: _ClassVar[WatermarkAnchor]
    WATERMARK_ANCHOR_TOP_RIGHT: _ClassVar[WatermarkAnchor]
    WATERMARK_ANCHOR_MIDDLE_LEFT: _ClassVar[WatermarkAnchor]
    WATERMARK_ANCHOR_MIDDLE_CENTER: _ClassVar[WatermarkAnchor]
    WATERMARK_ANCHOR_MIDDLE_RIGHT: _ClassVar[WatermarkAnchor]
    WATERMARK_ANCHOR_BOTTOM_LEFT: _ClassVar[WatermarkAnchor]
    WATERMARK_ANCHOR_BOTTOM_CENTER: _ClassVar[WatermarkAnchor]
    WATERMARK_ANCHOR_BOTTOM_RIGHT: _ClassVar[WatermarkAnchor]
WATERMARK_ANCHOR_UNSPECIFIED: WatermarkAnchor
WATERMARK_ANCHOR_TOP_LEFT: WatermarkAnchor
WATERMARK_ANCHOR_TOP_CENTER: WatermarkAnchor
WATERMARK_ANCHOR_TOP_RIGHT: WatermarkAnchor
WATERMARK_ANCHOR_MIDDLE_LEFT: WatermarkAnchor
WATERMARK_ANCHOR_MIDDLE_CENTER: WatermarkAnchor
WATERMARK_ANCHOR_MIDDLE_RIGHT: WatermarkAnchor
WATERMARK_ANCHOR_BOTTOM_LEFT: WatermarkAnchor
WATERMARK_ANCHOR_BOTTOM_CENTER: WatermarkAnchor
WATERMARK_ANCHOR_BOTTOM_RIGHT: WatermarkAnchor

class WatermarkPixelPlacement(_message.Message):
    __slots__ = ("x", "y", "width")
    X_FIELD_NUMBER: _ClassVar[int]
    Y_FIELD_NUMBER: _ClassVar[int]
    WIDTH_FIELD_NUMBER: _ClassVar[int]
    x: int
    y: int
    width: int
    def __init__(self, x: _Optional[int] = ..., y: _Optional[int] = ..., width: _Optional[int] = ...) -> None: ...

class WatermarkConfig(_message.Message):
    __slots__ = ("image_url", "anchor", "width_pct", "margin_pct", "opacity", "pixel")
    IMAGE_URL_FIELD_NUMBER: _ClassVar[int]
    ANCHOR_FIELD_NUMBER: _ClassVar[int]
    WIDTH_PCT_FIELD_NUMBER: _ClassVar[int]
    MARGIN_PCT_FIELD_NUMBER: _ClassVar[int]
    OPACITY_FIELD_NUMBER: _ClassVar[int]
    PIXEL_FIELD_NUMBER: _ClassVar[int]
    image_url: str
    anchor: WatermarkAnchor
    width_pct: float
    margin_pct: float
    opacity: float
    pixel: WatermarkPixelPlacement
    def __init__(self, image_url: _Optional[str] = ..., anchor: _Optional[_Union[WatermarkAnchor, str]] = ..., width_pct: _Optional[float] = ..., margin_pct: _Optional[float] = ..., opacity: _Optional[float] = ..., pixel: _Optional[_Union[WatermarkPixelPlacement, _Mapping]] = ...) -> None: ...
