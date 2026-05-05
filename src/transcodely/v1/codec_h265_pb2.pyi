from buf.validate import validate_pb2 as _validate_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class H265Options(_message.Message):
    __slots__ = ("preset", "tune", "profile", "level", "crf", "bitrate", "maxrate", "bufsize", "keyint", "min_keyint", "bframes", "ref", "rc_lookahead", "aq_mode", "aq_strength", "psy_rd")
    PRESET_FIELD_NUMBER: _ClassVar[int]
    TUNE_FIELD_NUMBER: _ClassVar[int]
    PROFILE_FIELD_NUMBER: _ClassVar[int]
    LEVEL_FIELD_NUMBER: _ClassVar[int]
    CRF_FIELD_NUMBER: _ClassVar[int]
    BITRATE_FIELD_NUMBER: _ClassVar[int]
    MAXRATE_FIELD_NUMBER: _ClassVar[int]
    BUFSIZE_FIELD_NUMBER: _ClassVar[int]
    KEYINT_FIELD_NUMBER: _ClassVar[int]
    MIN_KEYINT_FIELD_NUMBER: _ClassVar[int]
    BFRAMES_FIELD_NUMBER: _ClassVar[int]
    REF_FIELD_NUMBER: _ClassVar[int]
    RC_LOOKAHEAD_FIELD_NUMBER: _ClassVar[int]
    AQ_MODE_FIELD_NUMBER: _ClassVar[int]
    AQ_STRENGTH_FIELD_NUMBER: _ClassVar[int]
    PSY_RD_FIELD_NUMBER: _ClassVar[int]
    preset: str
    tune: str
    profile: str
    level: str
    crf: int
    bitrate: int
    maxrate: int
    bufsize: int
    keyint: int
    min_keyint: int
    bframes: int
    ref: int
    rc_lookahead: int
    aq_mode: int
    aq_strength: float
    psy_rd: str
    def __init__(self, preset: _Optional[str] = ..., tune: _Optional[str] = ..., profile: _Optional[str] = ..., level: _Optional[str] = ..., crf: _Optional[int] = ..., bitrate: _Optional[int] = ..., maxrate: _Optional[int] = ..., bufsize: _Optional[int] = ..., keyint: _Optional[int] = ..., min_keyint: _Optional[int] = ..., bframes: _Optional[int] = ..., ref: _Optional[int] = ..., rc_lookahead: _Optional[int] = ..., aq_mode: _Optional[int] = ..., aq_strength: _Optional[float] = ..., psy_rd: _Optional[str] = ...) -> None: ...
