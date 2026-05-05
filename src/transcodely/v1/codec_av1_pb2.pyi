from buf.validate import validate_pb2 as _validate_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class AV1Options(_message.Message):
    __slots__ = ("preset", "tune", "crf", "bitrate", "max_bitrate", "keyint", "tile_columns", "tile_rows", "film_grain", "enable_dlf", "enable_cdef", "enable_restoration")
    PRESET_FIELD_NUMBER: _ClassVar[int]
    TUNE_FIELD_NUMBER: _ClassVar[int]
    CRF_FIELD_NUMBER: _ClassVar[int]
    BITRATE_FIELD_NUMBER: _ClassVar[int]
    MAX_BITRATE_FIELD_NUMBER: _ClassVar[int]
    KEYINT_FIELD_NUMBER: _ClassVar[int]
    TILE_COLUMNS_FIELD_NUMBER: _ClassVar[int]
    TILE_ROWS_FIELD_NUMBER: _ClassVar[int]
    FILM_GRAIN_FIELD_NUMBER: _ClassVar[int]
    ENABLE_DLF_FIELD_NUMBER: _ClassVar[int]
    ENABLE_CDEF_FIELD_NUMBER: _ClassVar[int]
    ENABLE_RESTORATION_FIELD_NUMBER: _ClassVar[int]
    preset: int
    tune: int
    crf: int
    bitrate: int
    max_bitrate: int
    keyint: int
    tile_columns: int
    tile_rows: int
    film_grain: int
    enable_dlf: bool
    enable_cdef: bool
    enable_restoration: bool
    def __init__(self, preset: _Optional[int] = ..., tune: _Optional[int] = ..., crf: _Optional[int] = ..., bitrate: _Optional[int] = ..., max_bitrate: _Optional[int] = ..., keyint: _Optional[int] = ..., tile_columns: _Optional[int] = ..., tile_rows: _Optional[int] = ..., film_grain: _Optional[int] = ..., enable_dlf: bool = ..., enable_cdef: bool = ..., enable_restoration: bool = ...) -> None: ...
