from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class InputMetadata(_message.Message):
    __slots__ = ("format", "duration_ms", "size_bytes", "bit_rate", "video", "audio", "probed_at")
    FORMAT_FIELD_NUMBER: _ClassVar[int]
    DURATION_MS_FIELD_NUMBER: _ClassVar[int]
    SIZE_BYTES_FIELD_NUMBER: _ClassVar[int]
    BIT_RATE_FIELD_NUMBER: _ClassVar[int]
    VIDEO_FIELD_NUMBER: _ClassVar[int]
    AUDIO_FIELD_NUMBER: _ClassVar[int]
    PROBED_AT_FIELD_NUMBER: _ClassVar[int]
    format: str
    duration_ms: int
    size_bytes: int
    bit_rate: int
    video: VideoStreamInfo
    audio: AudioStreamInfo
    probed_at: _timestamp_pb2.Timestamp
    def __init__(self, format: _Optional[str] = ..., duration_ms: _Optional[int] = ..., size_bytes: _Optional[int] = ..., bit_rate: _Optional[int] = ..., video: _Optional[_Union[VideoStreamInfo, _Mapping]] = ..., audio: _Optional[_Union[AudioStreamInfo, _Mapping]] = ..., probed_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class VideoStreamInfo(_message.Message):
    __slots__ = ("codec", "width", "height", "frame_rate", "bit_rate", "pixel_format", "color_space", "color_transfer", "duration_ms", "color_primaries", "chroma_location", "bit_depth", "interlaced", "frame_count", "display_aspect_ratio", "sample_aspect_ratio", "rotation")
    CODEC_FIELD_NUMBER: _ClassVar[int]
    WIDTH_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    FRAME_RATE_FIELD_NUMBER: _ClassVar[int]
    BIT_RATE_FIELD_NUMBER: _ClassVar[int]
    PIXEL_FORMAT_FIELD_NUMBER: _ClassVar[int]
    COLOR_SPACE_FIELD_NUMBER: _ClassVar[int]
    COLOR_TRANSFER_FIELD_NUMBER: _ClassVar[int]
    DURATION_MS_FIELD_NUMBER: _ClassVar[int]
    COLOR_PRIMARIES_FIELD_NUMBER: _ClassVar[int]
    CHROMA_LOCATION_FIELD_NUMBER: _ClassVar[int]
    BIT_DEPTH_FIELD_NUMBER: _ClassVar[int]
    INTERLACED_FIELD_NUMBER: _ClassVar[int]
    FRAME_COUNT_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_ASPECT_RATIO_FIELD_NUMBER: _ClassVar[int]
    SAMPLE_ASPECT_RATIO_FIELD_NUMBER: _ClassVar[int]
    ROTATION_FIELD_NUMBER: _ClassVar[int]
    codec: str
    width: int
    height: int
    frame_rate: float
    bit_rate: int
    pixel_format: str
    color_space: str
    color_transfer: str
    duration_ms: int
    color_primaries: str
    chroma_location: str
    bit_depth: int
    interlaced: bool
    frame_count: int
    display_aspect_ratio: str
    sample_aspect_ratio: str
    rotation: int
    def __init__(self, codec: _Optional[str] = ..., width: _Optional[int] = ..., height: _Optional[int] = ..., frame_rate: _Optional[float] = ..., bit_rate: _Optional[int] = ..., pixel_format: _Optional[str] = ..., color_space: _Optional[str] = ..., color_transfer: _Optional[str] = ..., duration_ms: _Optional[int] = ..., color_primaries: _Optional[str] = ..., chroma_location: _Optional[str] = ..., bit_depth: _Optional[int] = ..., interlaced: bool = ..., frame_count: _Optional[int] = ..., display_aspect_ratio: _Optional[str] = ..., sample_aspect_ratio: _Optional[str] = ..., rotation: _Optional[int] = ...) -> None: ...

class AudioStreamInfo(_message.Message):
    __slots__ = ("codec", "sample_rate", "channels", "channel_layout", "bit_rate", "duration_ms", "bits_per_sample", "language", "is_default")
    CODEC_FIELD_NUMBER: _ClassVar[int]
    SAMPLE_RATE_FIELD_NUMBER: _ClassVar[int]
    CHANNELS_FIELD_NUMBER: _ClassVar[int]
    CHANNEL_LAYOUT_FIELD_NUMBER: _ClassVar[int]
    BIT_RATE_FIELD_NUMBER: _ClassVar[int]
    DURATION_MS_FIELD_NUMBER: _ClassVar[int]
    BITS_PER_SAMPLE_FIELD_NUMBER: _ClassVar[int]
    LANGUAGE_FIELD_NUMBER: _ClassVar[int]
    IS_DEFAULT_FIELD_NUMBER: _ClassVar[int]
    codec: str
    sample_rate: int
    channels: int
    channel_layout: str
    bit_rate: int
    duration_ms: int
    bits_per_sample: int
    language: str
    is_default: bool
    def __init__(self, codec: _Optional[str] = ..., sample_rate: _Optional[int] = ..., channels: _Optional[int] = ..., channel_layout: _Optional[str] = ..., bit_rate: _Optional[int] = ..., duration_ms: _Optional[int] = ..., bits_per_sample: _Optional[int] = ..., language: _Optional[str] = ..., is_default: bool = ...) -> None: ...

class SubtitleStreamInfo(_message.Message):
    __slots__ = ("codec", "language", "title", "is_default", "hearing_impaired", "forced")
    CODEC_FIELD_NUMBER: _ClassVar[int]
    LANGUAGE_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    IS_DEFAULT_FIELD_NUMBER: _ClassVar[int]
    HEARING_IMPAIRED_FIELD_NUMBER: _ClassVar[int]
    FORCED_FIELD_NUMBER: _ClassVar[int]
    codec: str
    language: str
    title: str
    is_default: bool
    hearing_impaired: bool
    forced: bool
    def __init__(self, codec: _Optional[str] = ..., language: _Optional[str] = ..., title: _Optional[str] = ..., is_default: bool = ..., hearing_impaired: bool = ..., forced: bool = ...) -> None: ...
