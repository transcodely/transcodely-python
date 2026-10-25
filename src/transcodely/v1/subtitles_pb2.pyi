from buf.validate import validate_pb2 as _validate_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

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

class TranscriptStyle(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    TRANSCRIPT_STYLE_UNSPECIFIED: _ClassVar[TranscriptStyle]
    TRANSCRIPT_STYLE_CLEAN: _ClassVar[TranscriptStyle]
    TRANSCRIPT_STYLE_LITERAL: _ClassVar[TranscriptStyle]

class TranscriptFormat(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    TRANSCRIPT_FORMAT_UNSPECIFIED: _ClassVar[TranscriptFormat]
    TRANSCRIPT_FORMAT_JSON: _ClassVar[TranscriptFormat]
    TRANSCRIPT_FORMAT_TXT: _ClassVar[TranscriptFormat]
    TRANSCRIPT_FORMAT_MD: _ClassVar[TranscriptFormat]

class InsightsSource(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    INSIGHTS_SOURCE_UNSPECIFIED: _ClassVar[InsightsSource]
    INSIGHTS_SOURCE_JOB: _ClassVar[InsightsSource]
    INSIGHTS_SOURCE_VIDEO: _ClassVar[InsightsSource]

class InsightsStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    INSIGHTS_STATUS_UNSPECIFIED: _ClassVar[InsightsStatus]
    INSIGHTS_STATUS_PENDING: _ClassVar[InsightsStatus]
    INSIGHTS_STATUS_READY: _ClassVar[InsightsStatus]
    INSIGHTS_STATUS_FAILED: _ClassVar[InsightsStatus]
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
TRANSCRIPT_STYLE_UNSPECIFIED: TranscriptStyle
TRANSCRIPT_STYLE_CLEAN: TranscriptStyle
TRANSCRIPT_STYLE_LITERAL: TranscriptStyle
TRANSCRIPT_FORMAT_UNSPECIFIED: TranscriptFormat
TRANSCRIPT_FORMAT_JSON: TranscriptFormat
TRANSCRIPT_FORMAT_TXT: TranscriptFormat
TRANSCRIPT_FORMAT_MD: TranscriptFormat
INSIGHTS_SOURCE_UNSPECIFIED: InsightsSource
INSIGHTS_SOURCE_JOB: InsightsSource
INSIGHTS_SOURCE_VIDEO: InsightsSource
INSIGHTS_STATUS_UNSPECIFIED: InsightsStatus
INSIGHTS_STATUS_PENDING: InsightsStatus
INSIGHTS_STATUS_READY: InsightsStatus
INSIGHTS_STATUS_FAILED: InsightsStatus

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
    __slots__ = ("operation", "source_stream_index", "source_url", "input_format", "output_format", "language", "label", "is_default", "hearing_impaired", "forced", "burn_in_style", "generate_chapters", "transcript", "insights")
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
    GENERATE_CHAPTERS_FIELD_NUMBER: _ClassVar[int]
    TRANSCRIPT_FIELD_NUMBER: _ClassVar[int]
    INSIGHTS_FIELD_NUMBER: _ClassVar[int]
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
    generate_chapters: bool
    transcript: TranscriptOptions
    insights: InsightsOptions
    def __init__(self, operation: _Optional[_Union[SubtitleOperation, str]] = ..., source_stream_index: _Optional[int] = ..., source_url: _Optional[str] = ..., input_format: _Optional[_Union[SubtitleFormat, str]] = ..., output_format: _Optional[_Union[SubtitleFormat, str]] = ..., language: _Optional[str] = ..., label: _Optional[str] = ..., is_default: bool = ..., hearing_impaired: bool = ..., forced: bool = ..., burn_in_style: _Optional[_Union[BurnInStyle, _Mapping]] = ..., generate_chapters: bool = ..., transcript: _Optional[_Union[TranscriptOptions, _Mapping]] = ..., insights: _Optional[_Union[InsightsOptions, _Mapping]] = ...) -> None: ...

class TranscriptOptions(_message.Message):
    __slots__ = ("style",)
    STYLE_FIELD_NUMBER: _ClassVar[int]
    style: TranscriptStyle
    def __init__(self, style: _Optional[_Union[TranscriptStyle, str]] = ...) -> None: ...

class InsightsOptions(_message.Message):
    __slots__ = ("enabled", "hint")
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    HINT_FIELD_NUMBER: _ClassVar[int]
    enabled: bool
    hint: str
    def __init__(self, enabled: bool = ..., hint: _Optional[str] = ...) -> None: ...

class TranscriptRendition(_message.Message):
    __slots__ = ("format", "storage_key", "url", "signed_url")
    FORMAT_FIELD_NUMBER: _ClassVar[int]
    STORAGE_KEY_FIELD_NUMBER: _ClassVar[int]
    URL_FIELD_NUMBER: _ClassVar[int]
    SIGNED_URL_FIELD_NUMBER: _ClassVar[int]
    format: TranscriptFormat
    storage_key: str
    url: str
    signed_url: str
    def __init__(self, format: _Optional[_Union[TranscriptFormat, str]] = ..., storage_key: _Optional[str] = ..., url: _Optional[str] = ..., signed_url: _Optional[str] = ...) -> None: ...

class ChapterPoint(_message.Message):
    __slots__ = ("start_seconds", "end_seconds", "title")
    START_SECONDS_FIELD_NUMBER: _ClassVar[int]
    END_SECONDS_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    start_seconds: float
    end_seconds: float
    title: str
    def __init__(self, start_seconds: _Optional[float] = ..., end_seconds: _Optional[float] = ..., title: _Optional[str] = ...) -> None: ...

class ChapterResult(_message.Message):
    __slots__ = ("output_id", "language", "storage_key", "url", "chapters")
    OUTPUT_ID_FIELD_NUMBER: _ClassVar[int]
    LANGUAGE_FIELD_NUMBER: _ClassVar[int]
    STORAGE_KEY_FIELD_NUMBER: _ClassVar[int]
    URL_FIELD_NUMBER: _ClassVar[int]
    CHAPTERS_FIELD_NUMBER: _ClassVar[int]
    output_id: str
    language: str
    storage_key: str
    url: str
    chapters: _containers.RepeatedCompositeFieldContainer[ChapterPoint]
    def __init__(self, output_id: _Optional[str] = ..., language: _Optional[str] = ..., storage_key: _Optional[str] = ..., url: _Optional[str] = ..., chapters: _Optional[_Iterable[_Union[ChapterPoint, _Mapping]]] = ...) -> None: ...

class SubtitleResult(_message.Message):
    __slots__ = ("output_id", "operation", "format", "language", "label", "auto_generated", "storage_key", "url", "transcript_storage_key", "transcript_url", "signed_url", "transcript_signed_url", "transcript_renditions", "transcript_style")
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
    SIGNED_URL_FIELD_NUMBER: _ClassVar[int]
    TRANSCRIPT_SIGNED_URL_FIELD_NUMBER: _ClassVar[int]
    TRANSCRIPT_RENDITIONS_FIELD_NUMBER: _ClassVar[int]
    TRANSCRIPT_STYLE_FIELD_NUMBER: _ClassVar[int]
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
    signed_url: str
    transcript_signed_url: str
    transcript_renditions: _containers.RepeatedCompositeFieldContainer[TranscriptRendition]
    transcript_style: TranscriptStyle
    def __init__(self, output_id: _Optional[str] = ..., operation: _Optional[_Union[SubtitleOperation, str]] = ..., format: _Optional[_Union[SubtitleFormat, str]] = ..., language: _Optional[str] = ..., label: _Optional[str] = ..., auto_generated: bool = ..., storage_key: _Optional[str] = ..., url: _Optional[str] = ..., transcript_storage_key: _Optional[str] = ..., transcript_url: _Optional[str] = ..., signed_url: _Optional[str] = ..., transcript_signed_url: _Optional[str] = ..., transcript_renditions: _Optional[_Iterable[_Union[TranscriptRendition, _Mapping]]] = ..., transcript_style: _Optional[_Union[TranscriptStyle, str]] = ...) -> None: ...

class InsightsQuestion(_message.Message):
    __slots__ = ("question", "answer", "start_seconds")
    QUESTION_FIELD_NUMBER: _ClassVar[int]
    ANSWER_FIELD_NUMBER: _ClassVar[int]
    START_SECONDS_FIELD_NUMBER: _ClassVar[int]
    question: str
    answer: str
    start_seconds: float
    def __init__(self, question: _Optional[str] = ..., answer: _Optional[str] = ..., start_seconds: _Optional[float] = ...) -> None: ...

class InsightsTerm(_message.Message):
    __slots__ = ("term", "definition", "start_seconds")
    TERM_FIELD_NUMBER: _ClassVar[int]
    DEFINITION_FIELD_NUMBER: _ClassVar[int]
    START_SECONDS_FIELD_NUMBER: _ClassVar[int]
    term: str
    definition: str
    start_seconds: float
    def __init__(self, term: _Optional[str] = ..., definition: _Optional[str] = ..., start_seconds: _Optional[float] = ...) -> None: ...

class InsightsHighlight(_message.Message):
    __slots__ = ("text", "start_seconds", "end_seconds")
    TEXT_FIELD_NUMBER: _ClassVar[int]
    START_SECONDS_FIELD_NUMBER: _ClassVar[int]
    END_SECONDS_FIELD_NUMBER: _ClassVar[int]
    text: str
    start_seconds: float
    end_seconds: float
    def __init__(self, text: _Optional[str] = ..., start_seconds: _Optional[float] = ..., end_seconds: _Optional[float] = ...) -> None: ...

class TranscriptInsights(_message.Message):
    __slots__ = ("output_id", "language", "status", "error_code", "title_suggestions", "summary", "key_points", "chapters", "questions", "terms", "highlights", "topics", "storage_key", "url", "signed_url", "chapters_storage_key", "chapters_url", "chapters_signed_url", "markdown_storage_key", "markdown_url", "markdown_signed_url", "generated_at", "hint", "id", "source", "video_id", "fee_eur")
    OUTPUT_ID_FIELD_NUMBER: _ClassVar[int]
    LANGUAGE_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    ERROR_CODE_FIELD_NUMBER: _ClassVar[int]
    TITLE_SUGGESTIONS_FIELD_NUMBER: _ClassVar[int]
    SUMMARY_FIELD_NUMBER: _ClassVar[int]
    KEY_POINTS_FIELD_NUMBER: _ClassVar[int]
    CHAPTERS_FIELD_NUMBER: _ClassVar[int]
    QUESTIONS_FIELD_NUMBER: _ClassVar[int]
    TERMS_FIELD_NUMBER: _ClassVar[int]
    HIGHLIGHTS_FIELD_NUMBER: _ClassVar[int]
    TOPICS_FIELD_NUMBER: _ClassVar[int]
    STORAGE_KEY_FIELD_NUMBER: _ClassVar[int]
    URL_FIELD_NUMBER: _ClassVar[int]
    SIGNED_URL_FIELD_NUMBER: _ClassVar[int]
    CHAPTERS_STORAGE_KEY_FIELD_NUMBER: _ClassVar[int]
    CHAPTERS_URL_FIELD_NUMBER: _ClassVar[int]
    CHAPTERS_SIGNED_URL_FIELD_NUMBER: _ClassVar[int]
    MARKDOWN_STORAGE_KEY_FIELD_NUMBER: _ClassVar[int]
    MARKDOWN_URL_FIELD_NUMBER: _ClassVar[int]
    MARKDOWN_SIGNED_URL_FIELD_NUMBER: _ClassVar[int]
    GENERATED_AT_FIELD_NUMBER: _ClassVar[int]
    HINT_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    VIDEO_ID_FIELD_NUMBER: _ClassVar[int]
    FEE_EUR_FIELD_NUMBER: _ClassVar[int]
    output_id: str
    language: str
    status: InsightsStatus
    error_code: str
    title_suggestions: _containers.RepeatedScalarFieldContainer[str]
    summary: str
    key_points: _containers.RepeatedScalarFieldContainer[str]
    chapters: _containers.RepeatedCompositeFieldContainer[ChapterPoint]
    questions: _containers.RepeatedCompositeFieldContainer[InsightsQuestion]
    terms: _containers.RepeatedCompositeFieldContainer[InsightsTerm]
    highlights: _containers.RepeatedCompositeFieldContainer[InsightsHighlight]
    topics: _containers.RepeatedScalarFieldContainer[str]
    storage_key: str
    url: str
    signed_url: str
    chapters_storage_key: str
    chapters_url: str
    chapters_signed_url: str
    markdown_storage_key: str
    markdown_url: str
    markdown_signed_url: str
    generated_at: _timestamp_pb2.Timestamp
    hint: str
    id: str
    source: InsightsSource
    video_id: str
    fee_eur: float
    def __init__(self, output_id: _Optional[str] = ..., language: _Optional[str] = ..., status: _Optional[_Union[InsightsStatus, str]] = ..., error_code: _Optional[str] = ..., title_suggestions: _Optional[_Iterable[str]] = ..., summary: _Optional[str] = ..., key_points: _Optional[_Iterable[str]] = ..., chapters: _Optional[_Iterable[_Union[ChapterPoint, _Mapping]]] = ..., questions: _Optional[_Iterable[_Union[InsightsQuestion, _Mapping]]] = ..., terms: _Optional[_Iterable[_Union[InsightsTerm, _Mapping]]] = ..., highlights: _Optional[_Iterable[_Union[InsightsHighlight, _Mapping]]] = ..., topics: _Optional[_Iterable[str]] = ..., storage_key: _Optional[str] = ..., url: _Optional[str] = ..., signed_url: _Optional[str] = ..., chapters_storage_key: _Optional[str] = ..., chapters_url: _Optional[str] = ..., chapters_signed_url: _Optional[str] = ..., markdown_storage_key: _Optional[str] = ..., markdown_url: _Optional[str] = ..., markdown_signed_url: _Optional[str] = ..., generated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., hint: _Optional[str] = ..., id: _Optional[str] = ..., source: _Optional[_Union[InsightsSource, str]] = ..., video_id: _Optional[str] = ..., fee_eur: _Optional[float] = ...) -> None: ...
