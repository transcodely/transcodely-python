from buf.validate import validate_pb2 as _validate_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class VP9Options(_message.Message):
    __slots__ = ("profile", "quality", "crf", "speed", "bitrate", "min_bitrate", "max_bitrate", "keyint", "tile_columns", "tile_rows")
    PROFILE_FIELD_NUMBER: _ClassVar[int]
    QUALITY_FIELD_NUMBER: _ClassVar[int]
    CRF_FIELD_NUMBER: _ClassVar[int]
    SPEED_FIELD_NUMBER: _ClassVar[int]
    BITRATE_FIELD_NUMBER: _ClassVar[int]
    MIN_BITRATE_FIELD_NUMBER: _ClassVar[int]
    MAX_BITRATE_FIELD_NUMBER: _ClassVar[int]
    KEYINT_FIELD_NUMBER: _ClassVar[int]
    TILE_COLUMNS_FIELD_NUMBER: _ClassVar[int]
    TILE_ROWS_FIELD_NUMBER: _ClassVar[int]
    profile: int
    quality: str
    crf: int
    speed: int
    bitrate: int
    min_bitrate: int
    max_bitrate: int
    keyint: int
    tile_columns: int
    tile_rows: int
    def __init__(self, profile: _Optional[int] = ..., quality: _Optional[str] = ..., crf: _Optional[int] = ..., speed: _Optional[int] = ..., bitrate: _Optional[int] = ..., min_bitrate: _Optional[int] = ..., max_bitrate: _Optional[int] = ..., keyint: _Optional[int] = ..., tile_columns: _Optional[int] = ..., tile_rows: _Optional[int] = ...) -> None: ...
