from buf.validate import validate_pb2 as _validate_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ThumbnailMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    THUMBNAIL_MODE_UNSPECIFIED: _ClassVar[ThumbnailMode]
    THUMBNAIL_MODE_SINGLE: _ClassVar[ThumbnailMode]
    THUMBNAIL_MODE_INTERVAL: _ClassVar[ThumbnailMode]
    THUMBNAIL_MODE_SPRITE: _ClassVar[ThumbnailMode]
    THUMBNAIL_MODE_TIMESTAMPS: _ClassVar[ThumbnailMode]

class ThumbnailFormat(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    THUMBNAIL_FORMAT_UNSPECIFIED: _ClassVar[ThumbnailFormat]
    THUMBNAIL_FORMAT_JPEG: _ClassVar[ThumbnailFormat]
    THUMBNAIL_FORMAT_PNG: _ClassVar[ThumbnailFormat]
    THUMBNAIL_FORMAT_WEBP: _ClassVar[ThumbnailFormat]
THUMBNAIL_MODE_UNSPECIFIED: ThumbnailMode
THUMBNAIL_MODE_SINGLE: ThumbnailMode
THUMBNAIL_MODE_INTERVAL: ThumbnailMode
THUMBNAIL_MODE_SPRITE: ThumbnailMode
THUMBNAIL_MODE_TIMESTAMPS: ThumbnailMode
THUMBNAIL_FORMAT_UNSPECIFIED: ThumbnailFormat
THUMBNAIL_FORMAT_JPEG: ThumbnailFormat
THUMBNAIL_FORMAT_PNG: ThumbnailFormat
THUMBNAIL_FORMAT_WEBP: ThumbnailFormat

class ThumbnailSpec(_message.Message):
    __slots__ = ("mode", "format", "width", "height", "quality", "timestamp", "interval_seconds", "timestamps", "sprite_columns")
    MODE_FIELD_NUMBER: _ClassVar[int]
    FORMAT_FIELD_NUMBER: _ClassVar[int]
    WIDTH_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    QUALITY_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    INTERVAL_SECONDS_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMPS_FIELD_NUMBER: _ClassVar[int]
    SPRITE_COLUMNS_FIELD_NUMBER: _ClassVar[int]
    mode: ThumbnailMode
    format: ThumbnailFormat
    width: int
    height: int
    quality: int
    timestamp: float
    interval_seconds: float
    timestamps: _containers.RepeatedScalarFieldContainer[float]
    sprite_columns: int
    def __init__(self, mode: _Optional[_Union[ThumbnailMode, str]] = ..., format: _Optional[_Union[ThumbnailFormat, str]] = ..., width: _Optional[int] = ..., height: _Optional[int] = ..., quality: _Optional[int] = ..., timestamp: _Optional[float] = ..., interval_seconds: _Optional[float] = ..., timestamps: _Optional[_Iterable[float]] = ..., sprite_columns: _Optional[int] = ...) -> None: ...
