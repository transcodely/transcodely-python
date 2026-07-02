from buf.validate import validate_pb2 as _validate_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from transcodely.v1 import common_pb2 as _common_pb2
from transcodely.v1 import streaming_pb2 as _streaming_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class VideoSettings(_message.Message):
    __slots__ = ("codec", "resolution", "width", "height", "framerate", "bitrate_mode", "crf", "bitrate_kbps", "max_bitrate_kbps", "buffer_size_kbps", "profile", "level", "encoder_preset", "tune", "keyint", "min_keyint", "bframes", "refs", "rc_lookahead", "aq_mode", "aq_strength", "psy_rd", "deblock")
    CODEC_FIELD_NUMBER: _ClassVar[int]
    RESOLUTION_FIELD_NUMBER: _ClassVar[int]
    WIDTH_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    FRAMERATE_FIELD_NUMBER: _ClassVar[int]
    BITRATE_MODE_FIELD_NUMBER: _ClassVar[int]
    CRF_FIELD_NUMBER: _ClassVar[int]
    BITRATE_KBPS_FIELD_NUMBER: _ClassVar[int]
    MAX_BITRATE_KBPS_FIELD_NUMBER: _ClassVar[int]
    BUFFER_SIZE_KBPS_FIELD_NUMBER: _ClassVar[int]
    PROFILE_FIELD_NUMBER: _ClassVar[int]
    LEVEL_FIELD_NUMBER: _ClassVar[int]
    ENCODER_PRESET_FIELD_NUMBER: _ClassVar[int]
    TUNE_FIELD_NUMBER: _ClassVar[int]
    KEYINT_FIELD_NUMBER: _ClassVar[int]
    MIN_KEYINT_FIELD_NUMBER: _ClassVar[int]
    BFRAMES_FIELD_NUMBER: _ClassVar[int]
    REFS_FIELD_NUMBER: _ClassVar[int]
    RC_LOOKAHEAD_FIELD_NUMBER: _ClassVar[int]
    AQ_MODE_FIELD_NUMBER: _ClassVar[int]
    AQ_STRENGTH_FIELD_NUMBER: _ClassVar[int]
    PSY_RD_FIELD_NUMBER: _ClassVar[int]
    DEBLOCK_FIELD_NUMBER: _ClassVar[int]
    codec: _common_pb2.VideoCodec
    resolution: _common_pb2.Resolution
    width: int
    height: int
    framerate: int
    bitrate_mode: _common_pb2.BitrateMode
    crf: int
    bitrate_kbps: int
    max_bitrate_kbps: int
    buffer_size_kbps: int
    profile: str
    level: str
    encoder_preset: str
    tune: str
    keyint: int
    min_keyint: int
    bframes: int
    refs: int
    rc_lookahead: int
    aq_mode: int
    aq_strength: float
    psy_rd: str
    deblock: str
    def __init__(self, codec: _Optional[_Union[_common_pb2.VideoCodec, str]] = ..., resolution: _Optional[_Union[_common_pb2.Resolution, str]] = ..., width: _Optional[int] = ..., height: _Optional[int] = ..., framerate: _Optional[int] = ..., bitrate_mode: _Optional[_Union[_common_pb2.BitrateMode, str]] = ..., crf: _Optional[int] = ..., bitrate_kbps: _Optional[int] = ..., max_bitrate_kbps: _Optional[int] = ..., buffer_size_kbps: _Optional[int] = ..., profile: _Optional[str] = ..., level: _Optional[str] = ..., encoder_preset: _Optional[str] = ..., tune: _Optional[str] = ..., keyint: _Optional[int] = ..., min_keyint: _Optional[int] = ..., bframes: _Optional[int] = ..., refs: _Optional[int] = ..., rc_lookahead: _Optional[int] = ..., aq_mode: _Optional[int] = ..., aq_strength: _Optional[float] = ..., psy_rd: _Optional[str] = ..., deblock: _Optional[str] = ...) -> None: ...

class AudioSettings(_message.Message):
    __slots__ = ("codec", "bitrate_kbps", "sample_rate", "channels", "normalize")
    CODEC_FIELD_NUMBER: _ClassVar[int]
    BITRATE_KBPS_FIELD_NUMBER: _ClassVar[int]
    SAMPLE_RATE_FIELD_NUMBER: _ClassVar[int]
    CHANNELS_FIELD_NUMBER: _ClassVar[int]
    NORMALIZE_FIELD_NUMBER: _ClassVar[int]
    codec: _common_pb2.AudioCodec
    bitrate_kbps: int
    sample_rate: int
    channels: int
    normalize: bool
    def __init__(self, codec: _Optional[_Union[_common_pb2.AudioCodec, str]] = ..., bitrate_kbps: _Optional[int] = ..., sample_rate: _Optional[int] = ..., channels: _Optional[int] = ..., normalize: bool = ...) -> None: ...

class PresetVariant(_message.Message):
    __slots__ = ("resolution", "width", "height", "bitrate_kbps", "max_bitrate_kbps", "buffer_size_kbps", "crf", "quality", "framerate")
    RESOLUTION_FIELD_NUMBER: _ClassVar[int]
    WIDTH_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    BITRATE_KBPS_FIELD_NUMBER: _ClassVar[int]
    MAX_BITRATE_KBPS_FIELD_NUMBER: _ClassVar[int]
    BUFFER_SIZE_KBPS_FIELD_NUMBER: _ClassVar[int]
    CRF_FIELD_NUMBER: _ClassVar[int]
    QUALITY_FIELD_NUMBER: _ClassVar[int]
    FRAMERATE_FIELD_NUMBER: _ClassVar[int]
    resolution: _common_pb2.Resolution
    width: int
    height: int
    bitrate_kbps: int
    max_bitrate_kbps: int
    buffer_size_kbps: int
    crf: int
    quality: _common_pb2.QualityTier
    framerate: int
    def __init__(self, resolution: _Optional[_Union[_common_pb2.Resolution, str]] = ..., width: _Optional[int] = ..., height: _Optional[int] = ..., bitrate_kbps: _Optional[int] = ..., max_bitrate_kbps: _Optional[int] = ..., buffer_size_kbps: _Optional[int] = ..., crf: _Optional[int] = ..., quality: _Optional[_Union[_common_pb2.QualityTier, str]] = ..., framerate: _Optional[int] = ...) -> None: ...

class Preset(_message.Message):
    __slots__ = ("id", "slug", "name", "description", "content_type", "container", "faststart", "delivery_format", "segment_duration", "video", "audio", "quality_tier", "estimated_cost_per_minute", "system_preset", "created_at", "updated_at", "variants", "disable_audio")
    ID_FIELD_NUMBER: _ClassVar[int]
    SLUG_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    CONTENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    CONTAINER_FIELD_NUMBER: _ClassVar[int]
    FASTSTART_FIELD_NUMBER: _ClassVar[int]
    DELIVERY_FORMAT_FIELD_NUMBER: _ClassVar[int]
    SEGMENT_DURATION_FIELD_NUMBER: _ClassVar[int]
    VIDEO_FIELD_NUMBER: _ClassVar[int]
    AUDIO_FIELD_NUMBER: _ClassVar[int]
    QUALITY_TIER_FIELD_NUMBER: _ClassVar[int]
    ESTIMATED_COST_PER_MINUTE_FIELD_NUMBER: _ClassVar[int]
    SYSTEM_PRESET_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    VARIANTS_FIELD_NUMBER: _ClassVar[int]
    DISABLE_AUDIO_FIELD_NUMBER: _ClassVar[int]
    id: str
    slug: str
    name: str
    description: str
    content_type: _common_pb2.ContentType
    container: _common_pb2.Container
    faststart: bool
    delivery_format: _common_pb2.DeliveryFormat
    segment_duration: int
    video: VideoSettings
    audio: AudioSettings
    quality_tier: _common_pb2.QualityTier
    estimated_cost_per_minute: float
    system_preset: bool
    created_at: _timestamp_pb2.Timestamp
    updated_at: _timestamp_pb2.Timestamp
    variants: _containers.RepeatedCompositeFieldContainer[PresetVariant]
    disable_audio: bool
    def __init__(self, id: _Optional[str] = ..., slug: _Optional[str] = ..., name: _Optional[str] = ..., description: _Optional[str] = ..., content_type: _Optional[_Union[_common_pb2.ContentType, str]] = ..., container: _Optional[_Union[_common_pb2.Container, str]] = ..., faststart: bool = ..., delivery_format: _Optional[_Union[_common_pb2.DeliveryFormat, str]] = ..., segment_duration: _Optional[int] = ..., video: _Optional[_Union[VideoSettings, _Mapping]] = ..., audio: _Optional[_Union[AudioSettings, _Mapping]] = ..., quality_tier: _Optional[_Union[_common_pb2.QualityTier, str]] = ..., estimated_cost_per_minute: _Optional[float] = ..., system_preset: bool = ..., created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., updated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., variants: _Optional[_Iterable[_Union[PresetVariant, _Mapping]]] = ..., disable_audio: bool = ...) -> None: ...

class CreatePresetRequest(_message.Message):
    __slots__ = ("slug", "name", "description", "content_type", "container", "faststart", "delivery_format", "streaming", "segment_duration", "video", "audio", "quality_tier", "variants", "disable_audio")
    SLUG_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    CONTENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    CONTAINER_FIELD_NUMBER: _ClassVar[int]
    FASTSTART_FIELD_NUMBER: _ClassVar[int]
    DELIVERY_FORMAT_FIELD_NUMBER: _ClassVar[int]
    STREAMING_FIELD_NUMBER: _ClassVar[int]
    SEGMENT_DURATION_FIELD_NUMBER: _ClassVar[int]
    VIDEO_FIELD_NUMBER: _ClassVar[int]
    AUDIO_FIELD_NUMBER: _ClassVar[int]
    QUALITY_TIER_FIELD_NUMBER: _ClassVar[int]
    VARIANTS_FIELD_NUMBER: _ClassVar[int]
    DISABLE_AUDIO_FIELD_NUMBER: _ClassVar[int]
    slug: str
    name: str
    description: str
    content_type: _common_pb2.ContentType
    container: _common_pb2.Container
    faststart: bool
    delivery_format: _common_pb2.DeliveryFormat
    streaming: _streaming_pb2.StreamingConfig
    segment_duration: int
    video: VideoSettings
    audio: AudioSettings
    quality_tier: _common_pb2.QualityTier
    variants: _containers.RepeatedCompositeFieldContainer[PresetVariant]
    disable_audio: bool
    def __init__(self, slug: _Optional[str] = ..., name: _Optional[str] = ..., description: _Optional[str] = ..., content_type: _Optional[_Union[_common_pb2.ContentType, str]] = ..., container: _Optional[_Union[_common_pb2.Container, str]] = ..., faststart: bool = ..., delivery_format: _Optional[_Union[_common_pb2.DeliveryFormat, str]] = ..., streaming: _Optional[_Union[_streaming_pb2.StreamingConfig, _Mapping]] = ..., segment_duration: _Optional[int] = ..., video: _Optional[_Union[VideoSettings, _Mapping]] = ..., audio: _Optional[_Union[AudioSettings, _Mapping]] = ..., quality_tier: _Optional[_Union[_common_pb2.QualityTier, str]] = ..., variants: _Optional[_Iterable[_Union[PresetVariant, _Mapping]]] = ..., disable_audio: bool = ...) -> None: ...

class CreatePresetResponse(_message.Message):
    __slots__ = ("preset",)
    PRESET_FIELD_NUMBER: _ClassVar[int]
    preset: Preset
    def __init__(self, preset: _Optional[_Union[Preset, _Mapping]] = ...) -> None: ...

class GetPresetRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GetPresetResponse(_message.Message):
    __slots__ = ("preset",)
    PRESET_FIELD_NUMBER: _ClassVar[int]
    preset: Preset
    def __init__(self, preset: _Optional[_Union[Preset, _Mapping]] = ...) -> None: ...

class GetPresetBySlugRequest(_message.Message):
    __slots__ = ("slug",)
    SLUG_FIELD_NUMBER: _ClassVar[int]
    slug: str
    def __init__(self, slug: _Optional[str] = ...) -> None: ...

class GetPresetBySlugResponse(_message.Message):
    __slots__ = ("preset",)
    PRESET_FIELD_NUMBER: _ClassVar[int]
    preset: Preset
    def __init__(self, preset: _Optional[_Union[Preset, _Mapping]] = ...) -> None: ...

class ListPresetsRequest(_message.Message):
    __slots__ = ("include_system", "content_type", "quality_tier", "video_codec", "delivery_format", "pagination")
    INCLUDE_SYSTEM_FIELD_NUMBER: _ClassVar[int]
    CONTENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    QUALITY_TIER_FIELD_NUMBER: _ClassVar[int]
    VIDEO_CODEC_FIELD_NUMBER: _ClassVar[int]
    DELIVERY_FORMAT_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    include_system: bool
    content_type: _common_pb2.ContentType
    quality_tier: _common_pb2.QualityTier
    video_codec: _common_pb2.VideoCodec
    delivery_format: _common_pb2.DeliveryFormat
    pagination: _common_pb2.PaginationRequest
    def __init__(self, include_system: bool = ..., content_type: _Optional[_Union[_common_pb2.ContentType, str]] = ..., quality_tier: _Optional[_Union[_common_pb2.QualityTier, str]] = ..., video_codec: _Optional[_Union[_common_pb2.VideoCodec, str]] = ..., delivery_format: _Optional[_Union[_common_pb2.DeliveryFormat, str]] = ..., pagination: _Optional[_Union[_common_pb2.PaginationRequest, _Mapping]] = ...) -> None: ...

class ListPresetsResponse(_message.Message):
    __slots__ = ("presets", "pagination")
    PRESETS_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    presets: _containers.RepeatedCompositeFieldContainer[Preset]
    pagination: _common_pb2.PaginationResponse
    def __init__(self, presets: _Optional[_Iterable[_Union[Preset, _Mapping]]] = ..., pagination: _Optional[_Union[_common_pb2.PaginationResponse, _Mapping]] = ...) -> None: ...

class UpdatePresetRequest(_message.Message):
    __slots__ = ("id", "slug", "name", "description", "content_type", "container", "faststart", "delivery_format", "streaming", "segment_duration", "video", "audio", "quality_tier", "variants", "disable_audio")
    ID_FIELD_NUMBER: _ClassVar[int]
    SLUG_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    CONTENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    CONTAINER_FIELD_NUMBER: _ClassVar[int]
    FASTSTART_FIELD_NUMBER: _ClassVar[int]
    DELIVERY_FORMAT_FIELD_NUMBER: _ClassVar[int]
    STREAMING_FIELD_NUMBER: _ClassVar[int]
    SEGMENT_DURATION_FIELD_NUMBER: _ClassVar[int]
    VIDEO_FIELD_NUMBER: _ClassVar[int]
    AUDIO_FIELD_NUMBER: _ClassVar[int]
    QUALITY_TIER_FIELD_NUMBER: _ClassVar[int]
    VARIANTS_FIELD_NUMBER: _ClassVar[int]
    DISABLE_AUDIO_FIELD_NUMBER: _ClassVar[int]
    id: str
    slug: str
    name: str
    description: str
    content_type: _common_pb2.ContentType
    container: _common_pb2.Container
    faststart: bool
    delivery_format: _common_pb2.DeliveryFormat
    streaming: _streaming_pb2.StreamingConfig
    segment_duration: int
    video: VideoSettings
    audio: AudioSettings
    quality_tier: _common_pb2.QualityTier
    variants: _containers.RepeatedCompositeFieldContainer[PresetVariant]
    disable_audio: bool
    def __init__(self, id: _Optional[str] = ..., slug: _Optional[str] = ..., name: _Optional[str] = ..., description: _Optional[str] = ..., content_type: _Optional[_Union[_common_pb2.ContentType, str]] = ..., container: _Optional[_Union[_common_pb2.Container, str]] = ..., faststart: bool = ..., delivery_format: _Optional[_Union[_common_pb2.DeliveryFormat, str]] = ..., streaming: _Optional[_Union[_streaming_pb2.StreamingConfig, _Mapping]] = ..., segment_duration: _Optional[int] = ..., video: _Optional[_Union[VideoSettings, _Mapping]] = ..., audio: _Optional[_Union[AudioSettings, _Mapping]] = ..., quality_tier: _Optional[_Union[_common_pb2.QualityTier, str]] = ..., variants: _Optional[_Iterable[_Union[PresetVariant, _Mapping]]] = ..., disable_audio: bool = ...) -> None: ...

class UpdatePresetResponse(_message.Message):
    __slots__ = ("preset",)
    PRESET_FIELD_NUMBER: _ClassVar[int]
    preset: Preset
    def __init__(self, preset: _Optional[_Union[Preset, _Mapping]] = ...) -> None: ...

class DuplicatePresetRequest(_message.Message):
    __slots__ = ("source_id", "slug", "name")
    SOURCE_ID_FIELD_NUMBER: _ClassVar[int]
    SLUG_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    source_id: str
    slug: str
    name: str
    def __init__(self, source_id: _Optional[str] = ..., slug: _Optional[str] = ..., name: _Optional[str] = ...) -> None: ...

class DuplicatePresetResponse(_message.Message):
    __slots__ = ("preset",)
    PRESET_FIELD_NUMBER: _ClassVar[int]
    preset: Preset
    def __init__(self, preset: _Optional[_Union[Preset, _Mapping]] = ...) -> None: ...

class ArchivePresetRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class ArchivePresetResponse(_message.Message):
    __slots__ = ("preset",)
    PRESET_FIELD_NUMBER: _ClassVar[int]
    preset: Preset
    def __init__(self, preset: _Optional[_Union[Preset, _Mapping]] = ...) -> None: ...
