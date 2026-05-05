from buf.validate import validate_pb2 as _validate_pb2
from transcodely.v1 import common_pb2 as _common_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ContentAwareMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CONTENT_AWARE_MODE_UNSPECIFIED: _ClassVar[ContentAwareMode]
    CONTENT_AWARE_MODE_PER_TITLE: _ClassVar[ContentAwareMode]
    CONTENT_AWARE_MODE_AUTO_ABR: _ClassVar[ContentAwareMode]
CONTENT_AWARE_MODE_UNSPECIFIED: ContentAwareMode
CONTENT_AWARE_MODE_PER_TITLE: ContentAwareMode
CONTENT_AWARE_MODE_AUTO_ABR: ContentAwareMode

class AutoABRConfig(_message.Message):
    __slots__ = ("min_variants", "max_variants", "min_resolution", "max_resolution")
    MIN_VARIANTS_FIELD_NUMBER: _ClassVar[int]
    MAX_VARIANTS_FIELD_NUMBER: _ClassVar[int]
    MIN_RESOLUTION_FIELD_NUMBER: _ClassVar[int]
    MAX_RESOLUTION_FIELD_NUMBER: _ClassVar[int]
    min_variants: int
    max_variants: int
    min_resolution: _common_pb2.Resolution
    max_resolution: _common_pb2.Resolution
    def __init__(self, min_variants: _Optional[int] = ..., max_variants: _Optional[int] = ..., min_resolution: _Optional[_Union[_common_pb2.Resolution, str]] = ..., max_resolution: _Optional[_Union[_common_pb2.Resolution, str]] = ...) -> None: ...

class ContentAwareConfig(_message.Message):
    __slots__ = ("mode", "vmaf_target", "auto_abr")
    MODE_FIELD_NUMBER: _ClassVar[int]
    VMAF_TARGET_FIELD_NUMBER: _ClassVar[int]
    AUTO_ABR_FIELD_NUMBER: _ClassVar[int]
    mode: ContentAwareMode
    vmaf_target: float
    auto_abr: AutoABRConfig
    def __init__(self, mode: _Optional[_Union[ContentAwareMode, str]] = ..., vmaf_target: _Optional[float] = ..., auto_abr: _Optional[_Union[AutoABRConfig, _Mapping]] = ...) -> None: ...

class ContentAnalysis(_message.Message):
    __slots__ = ("complexity_score", "motion_score", "texture_score", "content_type")
    COMPLEXITY_SCORE_FIELD_NUMBER: _ClassVar[int]
    MOTION_SCORE_FIELD_NUMBER: _ClassVar[int]
    TEXTURE_SCORE_FIELD_NUMBER: _ClassVar[int]
    CONTENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    complexity_score: float
    motion_score: float
    texture_score: float
    content_type: str
    def __init__(self, complexity_score: _Optional[float] = ..., motion_score: _Optional[float] = ..., texture_score: _Optional[float] = ..., content_type: _Optional[str] = ...) -> None: ...
