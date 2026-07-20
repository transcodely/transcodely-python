from buf.validate import validate_pb2 as _validate_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SubtitleOperation(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SUBTITLE_OPERATION_UNSPECIFIED: _ClassVar[SubtitleOperation]
    SUBTITLE_OPERATION_PASSTHROUGH: _ClassVar[SubtitleOperation]
    SUBTITLE_OPERATION_CONVERT: _ClassVar[SubtitleOperation]
    SUBTITLE_OPERATION_BURN_IN: _ClassVar[SubtitleOperation]
    SUBTITLE_OPERATION_EXTRACT: _ClassVar[SubtitleOperation]
    SUBTITLE_OPERATION_GENERATE: _ClassVar[SubtitleOperation]

class SubtitleFormat(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SUBTITLE_FORMAT_UNSPECIFIED: _ClassVar[SubtitleFormat]
    SUBTITLE_FORMAT_SRT: _ClassVar[SubtitleFormat]
    SUBTITLE_FORMAT_WEBVTT: _ClassVar[SubtitleFormat]
    SUBTITLE_FORMAT_TTML: _ClassVar[SubtitleFormat]
    SUBTITLE_FORMAT_ASS: _ClassVar[SubtitleFormat]
SUBTITLE_OPERATION_UNSPECIFIED: SubtitleOperation
SUBTITLE_OPERATION_PASSTHROUGH: SubtitleOperation
SUBTITLE_OPERATION_CONVERT: SubtitleOperation
SUBTITLE_OPERATION_BURN_IN: SubtitleOperation
SUBTITLE_OPERATION_EXTRACT: SubtitleOperation
SUBTITLE_OPERATION_GENERATE: SubtitleOperation
SUBTITLE_FORMAT_UNSPECIFIED: SubtitleFormat
SUBTITLE_FORMAT_SRT: SubtitleFormat
SUBTITLE_FORMAT_WEBVTT: SubtitleFormat
SUBTITLE_FORMAT_TTML: SubtitleFormat
SUBTITLE_FORMAT_ASS: SubtitleFormat

class BurnInStyle(_message.Message):
    __slots__ = ("font_family", "font_size", "font_color", "outline_color", "outline_width", "margin_bottom")
    FONT_FAMILY_FIELD_NUMBER: _ClassVar[int]
    FONT_SIZE_FIELD_NUMBER: _ClassVar[int]
    FONT_COLOR_FIELD_NUMBER: _ClassVar[int]
    OUTLINE_COLOR_FIELD_NUMBER: _ClassVar[int]
    OUTLINE_WIDTH_FIELD_NUMBER: _ClassVar[int]
    MARGIN_BOTTOM_FIELD_NUMBER: _ClassVar[int]
    font_family: str
    font_size: int
    font_color: str
    outline_color: str
    outline_width: int
    margin_bottom: int
    def __init__(self, font_family: _Optional[str] = ..., font_size: _Optional[int] = ..., font_color: _Optional[str] = ..., outline_color: _Optional[str] = ..., outline_width: _Optional[int] = ..., margin_bottom: _Optional[int] = ...) -> None: ...

class SubtitleTrack(_message.Message):
    __slots__ = ("operation", "source_stream_index", "source_url", "input_format", "output_format", "language", "label", "is_default", "hearing_impaired", "forced", "burn_in_style")
    OPERATION_FIELD_NUMBER: _ClassVar[int]
    SOURCE_STREAM_INDEX_FIELD_NUMBER: _ClassVar[int]
    SOURCE_URL_FIELD_NUMBER: _ClassVar[int]
    INPUT_FORMAT_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_FORMAT_FIELD_NUMBER: _ClassVar[int]
    LANGUAGE_FIELD_NUMBER: _ClassVar[int]
    LABEL_FIELD_NUMBER: _ClassVar[int]
    IS_DEFAULT_FIELD_NUMBER: _ClassVar[int]
    HEARING_IMPAIRED_FIELD_NUMBER: _ClassVar[int]
    FORCED_FIELD_NUMBER: _ClassVar[int]
    BURN_IN_STYLE_FIELD_NUMBER: _ClassVar[int]
    operation: SubtitleOperation
    source_stream_index: int
    source_url: str
    input_format: SubtitleFormat
    output_format: SubtitleFormat
    language: str
    label: str
    is_default: bool
    hearing_impaired: bool
    forced: bool
    burn_in_style: BurnInStyle
    def __init__(self, operation: _Optional[_Union[SubtitleOperation, str]] = ..., source_stream_index: _Optional[int] = ..., source_url: _Optional[str] = ..., input_format: _Optional[_Union[SubtitleFormat, str]] = ..., output_format: _Optional[_Union[SubtitleFormat, str]] = ..., language: _Optional[str] = ..., label: _Optional[str] = ..., is_default: bool = ..., hearing_impaired: bool = ..., forced: bool = ..., burn_in_style: _Optional[_Union[BurnInStyle, _Mapping]] = ...) -> None: ...

class SubtitleResult(_message.Message):
    __slots__ = ("output_id", "operation", "format", "language", "label", "auto_generated", "storage_key", "url", "transcript_storage_key", "transcript_url")
    OUTPUT_ID_FIELD_NUMBER: _ClassVar[int]
    OPERATION_FIELD_NUMBER: _ClassVar[int]
    FORMAT_FIELD_NUMBER: _ClassVar[int]
    LANGUAGE_FIELD_NUMBER: _ClassVar[int]
    LABEL_FIELD_NUMBER: _ClassVar[int]
    AUTO_GENERATED_FIELD_NUMBER: _ClassVar[int]
    STORAGE_KEY_FIELD_NUMBER: _ClassVar[int]
    URL_FIELD_NUMBER: _ClassVar[int]
    TRANSCRIPT_STORAGE_KEY_FIELD_NUMBER: _ClassVar[int]
    TRANSCRIPT_URL_FIELD_NUMBER: _ClassVar[int]
    output_id: str
    operation: SubtitleOperation
    format: SubtitleFormat
    language: str
    label: str
    auto_generated: bool
    storage_key: str
    url: str
    transcript_storage_key: str
    transcript_url: str
    def __init__(self, output_id: _Optional[str] = ..., operation: _Optional[_Union[SubtitleOperation, str]] = ..., format: _Optional[_Union[SubtitleFormat, str]] = ..., language: _Optional[str] = ..., label: _Optional[str] = ..., auto_generated: bool = ..., storage_key: _Optional[str] = ..., url: _Optional[str] = ..., transcript_storage_key: _Optional[str] = ..., transcript_url: _Optional[str] = ...) -> None: ...
