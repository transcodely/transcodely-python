from buf.validate import validate_pb2 as _validate_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class HDRFormat(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    HDR_FORMAT_UNSPECIFIED: _ClassVar[HDRFormat]
    HDR_FORMAT_HDR10: _ClassVar[HDRFormat]
    HDR_FORMAT_HDR10_PLUS: _ClassVar[HDRFormat]
    HDR_FORMAT_HLG: _ClassVar[HDRFormat]
    HDR_FORMAT_DOLBY_VISION_5: _ClassVar[HDRFormat]
    HDR_FORMAT_DOLBY_VISION_8: _ClassVar[HDRFormat]

class HDRMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    HDR_MODE_UNSPECIFIED: _ClassVar[HDRMode]
    HDR_MODE_PASSTHROUGH: _ClassVar[HDRMode]
    HDR_MODE_TONEMAP: _ClassVar[HDRMode]
    HDR_MODE_FORCE: _ClassVar[HDRMode]

class ToneMapping(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    TONE_MAPPING_UNSPECIFIED: _ClassVar[ToneMapping]
    TONE_MAPPING_REINHARD: _ClassVar[ToneMapping]
    TONE_MAPPING_HABLE: _ClassVar[ToneMapping]
    TONE_MAPPING_BT2390: _ClassVar[ToneMapping]
    TONE_MAPPING_MOBIUS: _ClassVar[ToneMapping]
HDR_FORMAT_UNSPECIFIED: HDRFormat
HDR_FORMAT_HDR10: HDRFormat
HDR_FORMAT_HDR10_PLUS: HDRFormat
HDR_FORMAT_HLG: HDRFormat
HDR_FORMAT_DOLBY_VISION_5: HDRFormat
HDR_FORMAT_DOLBY_VISION_8: HDRFormat
HDR_MODE_UNSPECIFIED: HDRMode
HDR_MODE_PASSTHROUGH: HDRMode
HDR_MODE_TONEMAP: HDRMode
HDR_MODE_FORCE: HDRMode
TONE_MAPPING_UNSPECIFIED: ToneMapping
TONE_MAPPING_REINHARD: ToneMapping
TONE_MAPPING_HABLE: ToneMapping
TONE_MAPPING_BT2390: ToneMapping
TONE_MAPPING_MOBIUS: ToneMapping

class HDRConfig(_message.Message):
    __slots__ = ("format", "mode", "tone_mapping", "target_peak_nits", "master_display", "content_light_level", "rpu_url")
    FORMAT_FIELD_NUMBER: _ClassVar[int]
    MODE_FIELD_NUMBER: _ClassVar[int]
    TONE_MAPPING_FIELD_NUMBER: _ClassVar[int]
    TARGET_PEAK_NITS_FIELD_NUMBER: _ClassVar[int]
    MASTER_DISPLAY_FIELD_NUMBER: _ClassVar[int]
    CONTENT_LIGHT_LEVEL_FIELD_NUMBER: _ClassVar[int]
    RPU_URL_FIELD_NUMBER: _ClassVar[int]
    format: HDRFormat
    mode: HDRMode
    tone_mapping: ToneMapping
    target_peak_nits: int
    master_display: str
    content_light_level: str
    rpu_url: str
    def __init__(self, format: _Optional[_Union[HDRFormat, str]] = ..., mode: _Optional[_Union[HDRMode, str]] = ..., tone_mapping: _Optional[_Union[ToneMapping, str]] = ..., target_peak_nits: _Optional[int] = ..., master_display: _Optional[str] = ..., content_light_level: _Optional[str] = ..., rpu_url: _Optional[str] = ...) -> None: ...
