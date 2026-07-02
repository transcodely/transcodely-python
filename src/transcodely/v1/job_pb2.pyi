from buf.validate import validate_pb2 as _validate_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from transcodely.v1 import common_pb2 as _common_pb2
from transcodely.v1 import media_pb2 as _media_pb2
from transcodely.v1 import codec_h264_pb2 as _codec_h264_pb2
from transcodely.v1 import codec_h265_pb2 as _codec_h265_pb2
from transcodely.v1 import codec_vp9_pb2 as _codec_vp9_pb2
from transcodely.v1 import codec_av1_pb2 as _codec_av1_pb2
from transcodely.v1 import origin_pb2 as _origin_pb2
from transcodely.v1 import streaming_pb2 as _streaming_pb2
from transcodely.v1 import thumbnails_pb2 as _thumbnails_pb2
from transcodely.v1 import subtitles_pb2 as _subtitles_pb2
from transcodely.v1 import drm_pb2 as _drm_pb2
from transcodely.v1 import hdr_pb2 as _hdr_pb2
from transcodely.v1 import content_aware_pb2 as _content_aware_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class JobStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    JOB_STATUS_UNSPECIFIED: _ClassVar[JobStatus]
    JOB_STATUS_PENDING: _ClassVar[JobStatus]
    JOB_STATUS_PROBING: _ClassVar[JobStatus]
    JOB_STATUS_PROCESSING: _ClassVar[JobStatus]
    JOB_STATUS_COMPLETED: _ClassVar[JobStatus]
    JOB_STATUS_FAILED: _ClassVar[JobStatus]
    JOB_STATUS_CANCELED: _ClassVar[JobStatus]
    JOB_STATUS_PARTIAL: _ClassVar[JobStatus]
    JOB_STATUS_AWAITING_CONFIRMATION: _ClassVar[JobStatus]

class OutputStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    OUTPUT_STATUS_UNSPECIFIED: _ClassVar[OutputStatus]
    OUTPUT_STATUS_PENDING: _ClassVar[OutputStatus]
    OUTPUT_STATUS_PROCESSING: _ClassVar[OutputStatus]
    OUTPUT_STATUS_COMPLETED: _ClassVar[OutputStatus]
    OUTPUT_STATUS_FAILED: _ClassVar[OutputStatus]
    OUTPUT_STATUS_CANCELED: _ClassVar[OutputStatus]

class JobPriority(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    JOB_PRIORITY_UNSPECIFIED: _ClassVar[JobPriority]
    JOB_PRIORITY_ECONOMY: _ClassVar[JobPriority]
    JOB_PRIORITY_STANDARD: _ClassVar[JobPriority]
    JOB_PRIORITY_PREMIUM: _ClassVar[JobPriority]

class WatchEventType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    WATCH_EVENT_TYPE_UNSPECIFIED: _ClassVar[WatchEventType]
    WATCH_EVENT_TYPE_SNAPSHOT: _ClassVar[WatchEventType]
    WATCH_EVENT_TYPE_PROGRESS: _ClassVar[WatchEventType]
    WATCH_EVENT_TYPE_STATUS_CHANGE: _ClassVar[WatchEventType]
    WATCH_EVENT_TYPE_COMPLETED: _ClassVar[WatchEventType]
    WATCH_EVENT_TYPE_HEARTBEAT: _ClassVar[WatchEventType]
JOB_STATUS_UNSPECIFIED: JobStatus
JOB_STATUS_PENDING: JobStatus
JOB_STATUS_PROBING: JobStatus
JOB_STATUS_PROCESSING: JobStatus
JOB_STATUS_COMPLETED: JobStatus
JOB_STATUS_FAILED: JobStatus
JOB_STATUS_CANCELED: JobStatus
JOB_STATUS_PARTIAL: JobStatus
JOB_STATUS_AWAITING_CONFIRMATION: JobStatus
OUTPUT_STATUS_UNSPECIFIED: OutputStatus
OUTPUT_STATUS_PENDING: OutputStatus
OUTPUT_STATUS_PROCESSING: OutputStatus
OUTPUT_STATUS_COMPLETED: OutputStatus
OUTPUT_STATUS_FAILED: OutputStatus
OUTPUT_STATUS_CANCELED: OutputStatus
JOB_PRIORITY_UNSPECIFIED: JobPriority
JOB_PRIORITY_ECONOMY: JobPriority
JOB_PRIORITY_STANDARD: JobPriority
JOB_PRIORITY_PREMIUM: JobPriority
WATCH_EVENT_TYPE_UNSPECIFIED: WatchEventType
WATCH_EVENT_TYPE_SNAPSHOT: WatchEventType
WATCH_EVENT_TYPE_PROGRESS: WatchEventType
WATCH_EVENT_TYPE_STATUS_CHANGE: WatchEventType
WATCH_EVENT_TYPE_COMPLETED: WatchEventType
WATCH_EVENT_TYPE_HEARTBEAT: WatchEventType

class AudioTrackConfig(_message.Message):
    __slots__ = ("language", "label", "source_track", "is_default")
    LANGUAGE_FIELD_NUMBER: _ClassVar[int]
    LABEL_FIELD_NUMBER: _ClassVar[int]
    SOURCE_TRACK_FIELD_NUMBER: _ClassVar[int]
    IS_DEFAULT_FIELD_NUMBER: _ClassVar[int]
    language: str
    label: str
    source_track: int
    is_default: bool
    def __init__(self, language: _Optional[str] = ..., label: _Optional[str] = ..., source_track: _Optional[int] = ..., is_default: bool = ...) -> None: ...

class VideoVariant(_message.Message):
    __slots__ = ("codec", "resolution", "quality", "framerate", "width", "height", "bitrate", "h264", "h265", "vp9", "av1", "hdr")
    CODEC_FIELD_NUMBER: _ClassVar[int]
    RESOLUTION_FIELD_NUMBER: _ClassVar[int]
    QUALITY_FIELD_NUMBER: _ClassVar[int]
    FRAMERATE_FIELD_NUMBER: _ClassVar[int]
    WIDTH_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    BITRATE_FIELD_NUMBER: _ClassVar[int]
    H264_FIELD_NUMBER: _ClassVar[int]
    H265_FIELD_NUMBER: _ClassVar[int]
    VP9_FIELD_NUMBER: _ClassVar[int]
    AV1_FIELD_NUMBER: _ClassVar[int]
    HDR_FIELD_NUMBER: _ClassVar[int]
    codec: _common_pb2.VideoCodec
    resolution: _common_pb2.Resolution
    quality: _common_pb2.QualityTier
    framerate: int
    width: int
    height: int
    bitrate: int
    h264: _codec_h264_pb2.H264Options
    h265: _codec_h265_pb2.H265Options
    vp9: _codec_vp9_pb2.VP9Options
    av1: _codec_av1_pb2.AV1Options
    hdr: _hdr_pb2.HDRConfig
    def __init__(self, codec: _Optional[_Union[_common_pb2.VideoCodec, str]] = ..., resolution: _Optional[_Union[_common_pb2.Resolution, str]] = ..., quality: _Optional[_Union[_common_pb2.QualityTier, str]] = ..., framerate: _Optional[int] = ..., width: _Optional[int] = ..., height: _Optional[int] = ..., bitrate: _Optional[int] = ..., h264: _Optional[_Union[_codec_h264_pb2.H264Options, _Mapping]] = ..., h265: _Optional[_Union[_codec_h265_pb2.H265Options, _Mapping]] = ..., vp9: _Optional[_Union[_codec_vp9_pb2.VP9Options, _Mapping]] = ..., av1: _Optional[_Union[_codec_av1_pb2.AV1Options, _Mapping]] = ..., hdr: _Optional[_Union[_hdr_pb2.HDRConfig, _Mapping]] = ...) -> None: ...

class HLSConfig(_message.Message):
    __slots__ = ("manifest", "segment_format", "playlist_type", "variant_pattern")
    MANIFEST_FIELD_NUMBER: _ClassVar[int]
    SEGMENT_FORMAT_FIELD_NUMBER: _ClassVar[int]
    PLAYLIST_TYPE_FIELD_NUMBER: _ClassVar[int]
    VARIANT_PATTERN_FIELD_NUMBER: _ClassVar[int]
    manifest: str
    segment_format: _streaming_pb2.HLSSegmentFormat
    playlist_type: _streaming_pb2.HLSPlaylistType
    variant_pattern: str
    def __init__(self, manifest: _Optional[str] = ..., segment_format: _Optional[_Union[_streaming_pb2.HLSSegmentFormat, str]] = ..., playlist_type: _Optional[_Union[_streaming_pb2.HLSPlaylistType, str]] = ..., variant_pattern: _Optional[str] = ...) -> None: ...

class DASHConfig(_message.Message):
    __slots__ = ("manifest",)
    MANIFEST_FIELD_NUMBER: _ClassVar[int]
    manifest: str
    def __init__(self, manifest: _Optional[str] = ...) -> None: ...

class SegmentConfig(_message.Message):
    __slots__ = ("duration", "gop_alignment", "gop_size")
    DURATION_FIELD_NUMBER: _ClassVar[int]
    GOP_ALIGNMENT_FIELD_NUMBER: _ClassVar[int]
    GOP_SIZE_FIELD_NUMBER: _ClassVar[int]
    duration: int
    gop_alignment: _streaming_pb2.GOPAlignmentMode
    gop_size: int
    def __init__(self, duration: _Optional[int] = ..., gop_alignment: _Optional[_Union[_streaming_pb2.GOPAlignmentMode, str]] = ..., gop_size: _Optional[int] = ...) -> None: ...

class OutputSpec(_message.Message):
    __slots__ = ("type", "video", "audio", "hls", "dash", "segments", "path_template", "preset", "subtitle_tracks", "drm", "content_aware", "encoding_mode", "effective_path_template", "disable_audio")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    VIDEO_FIELD_NUMBER: _ClassVar[int]
    AUDIO_FIELD_NUMBER: _ClassVar[int]
    HLS_FIELD_NUMBER: _ClassVar[int]
    DASH_FIELD_NUMBER: _ClassVar[int]
    SEGMENTS_FIELD_NUMBER: _ClassVar[int]
    PATH_TEMPLATE_FIELD_NUMBER: _ClassVar[int]
    PRESET_FIELD_NUMBER: _ClassVar[int]
    SUBTITLE_TRACKS_FIELD_NUMBER: _ClassVar[int]
    DRM_FIELD_NUMBER: _ClassVar[int]
    CONTENT_AWARE_FIELD_NUMBER: _ClassVar[int]
    ENCODING_MODE_FIELD_NUMBER: _ClassVar[int]
    EFFECTIVE_PATH_TEMPLATE_FIELD_NUMBER: _ClassVar[int]
    DISABLE_AUDIO_FIELD_NUMBER: _ClassVar[int]
    type: _common_pb2.OutputFormat
    video: _containers.RepeatedCompositeFieldContainer[VideoVariant]
    audio: _containers.RepeatedCompositeFieldContainer[AudioTrackConfig]
    hls: HLSConfig
    dash: DASHConfig
    segments: SegmentConfig
    path_template: str
    preset: str
    subtitle_tracks: _containers.RepeatedCompositeFieldContainer[_subtitles_pb2.SubtitleTrack]
    drm: _drm_pb2.DRMConfig
    content_aware: _content_aware_pb2.ContentAwareConfig
    encoding_mode: str
    effective_path_template: str
    disable_audio: bool
    def __init__(self, type: _Optional[_Union[_common_pb2.OutputFormat, str]] = ..., video: _Optional[_Iterable[_Union[VideoVariant, _Mapping]]] = ..., audio: _Optional[_Iterable[_Union[AudioTrackConfig, _Mapping]]] = ..., hls: _Optional[_Union[HLSConfig, _Mapping]] = ..., dash: _Optional[_Union[DASHConfig, _Mapping]] = ..., segments: _Optional[_Union[SegmentConfig, _Mapping]] = ..., path_template: _Optional[str] = ..., preset: _Optional[str] = ..., subtitle_tracks: _Optional[_Iterable[_Union[_subtitles_pb2.SubtitleTrack, _Mapping]]] = ..., drm: _Optional[_Union[_drm_pb2.DRMConfig, _Mapping]] = ..., content_aware: _Optional[_Union[_content_aware_pb2.ContentAwareConfig, _Mapping]] = ..., encoding_mode: _Optional[str] = ..., effective_path_template: _Optional[str] = ..., disable_audio: bool = ...) -> None: ...

class PricingSnapshot(_message.Message):
    __slots__ = ("base_price", "codec_multiplier", "resolution_multiplier", "framerate_multiplier", "quality_multiplier", "resolution_tier", "actual_framerate", "pixel_count", "feature_multiplier")
    BASE_PRICE_FIELD_NUMBER: _ClassVar[int]
    CODEC_MULTIPLIER_FIELD_NUMBER: _ClassVar[int]
    RESOLUTION_MULTIPLIER_FIELD_NUMBER: _ClassVar[int]
    FRAMERATE_MULTIPLIER_FIELD_NUMBER: _ClassVar[int]
    QUALITY_MULTIPLIER_FIELD_NUMBER: _ClassVar[int]
    RESOLUTION_TIER_FIELD_NUMBER: _ClassVar[int]
    ACTUAL_FRAMERATE_FIELD_NUMBER: _ClassVar[int]
    PIXEL_COUNT_FIELD_NUMBER: _ClassVar[int]
    FEATURE_MULTIPLIER_FIELD_NUMBER: _ClassVar[int]
    base_price: float
    codec_multiplier: float
    resolution_multiplier: float
    framerate_multiplier: float
    quality_multiplier: float
    resolution_tier: _common_pb2.Resolution
    actual_framerate: float
    pixel_count: int
    feature_multiplier: float
    def __init__(self, base_price: _Optional[float] = ..., codec_multiplier: _Optional[float] = ..., resolution_multiplier: _Optional[float] = ..., framerate_multiplier: _Optional[float] = ..., quality_multiplier: _Optional[float] = ..., resolution_tier: _Optional[_Union[_common_pb2.Resolution, str]] = ..., actual_framerate: _Optional[float] = ..., pixel_count: _Optional[int] = ..., feature_multiplier: _Optional[float] = ...) -> None: ...

class VariantPricingSnapshot(_message.Message):
    __slots__ = ("index", "codec", "resolution", "framerate", "quality", "width", "height", "base_price", "codec_multiplier", "resolution_multiplier", "framerate_multiplier", "quality_multiplier", "resolution_tier", "actual_framerate", "pixel_count", "estimated_cost", "actual_cost", "status", "progress", "feature_multiplier")
    INDEX_FIELD_NUMBER: _ClassVar[int]
    CODEC_FIELD_NUMBER: _ClassVar[int]
    RESOLUTION_FIELD_NUMBER: _ClassVar[int]
    FRAMERATE_FIELD_NUMBER: _ClassVar[int]
    QUALITY_FIELD_NUMBER: _ClassVar[int]
    WIDTH_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    BASE_PRICE_FIELD_NUMBER: _ClassVar[int]
    CODEC_MULTIPLIER_FIELD_NUMBER: _ClassVar[int]
    RESOLUTION_MULTIPLIER_FIELD_NUMBER: _ClassVar[int]
    FRAMERATE_MULTIPLIER_FIELD_NUMBER: _ClassVar[int]
    QUALITY_MULTIPLIER_FIELD_NUMBER: _ClassVar[int]
    RESOLUTION_TIER_FIELD_NUMBER: _ClassVar[int]
    ACTUAL_FRAMERATE_FIELD_NUMBER: _ClassVar[int]
    PIXEL_COUNT_FIELD_NUMBER: _ClassVar[int]
    ESTIMATED_COST_FIELD_NUMBER: _ClassVar[int]
    ACTUAL_COST_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    PROGRESS_FIELD_NUMBER: _ClassVar[int]
    FEATURE_MULTIPLIER_FIELD_NUMBER: _ClassVar[int]
    index: int
    codec: _common_pb2.VideoCodec
    resolution: _common_pb2.Resolution
    framerate: int
    quality: _common_pb2.QualityTier
    width: int
    height: int
    base_price: float
    codec_multiplier: float
    resolution_multiplier: float
    framerate_multiplier: float
    quality_multiplier: float
    resolution_tier: _common_pb2.Resolution
    actual_framerate: float
    pixel_count: int
    estimated_cost: float
    actual_cost: float
    status: str
    progress: int
    feature_multiplier: float
    def __init__(self, index: _Optional[int] = ..., codec: _Optional[_Union[_common_pb2.VideoCodec, str]] = ..., resolution: _Optional[_Union[_common_pb2.Resolution, str]] = ..., framerate: _Optional[int] = ..., quality: _Optional[_Union[_common_pb2.QualityTier, str]] = ..., width: _Optional[int] = ..., height: _Optional[int] = ..., base_price: _Optional[float] = ..., codec_multiplier: _Optional[float] = ..., resolution_multiplier: _Optional[float] = ..., framerate_multiplier: _Optional[float] = ..., quality_multiplier: _Optional[float] = ..., resolution_tier: _Optional[_Union[_common_pb2.Resolution, str]] = ..., actual_framerate: _Optional[float] = ..., pixel_count: _Optional[int] = ..., estimated_cost: _Optional[float] = ..., actual_cost: _Optional[float] = ..., status: _Optional[str] = ..., progress: _Optional[int] = ..., feature_multiplier: _Optional[float] = ...) -> None: ...

class JobOutput(_message.Message):
    __slots__ = ("id", "spec", "status", "progress", "output_url", "output_size_bytes", "duration_seconds", "pricing", "estimated_duration_seconds", "estimated_cost", "actual_cost", "error_code", "error_message", "started_at", "completed_at", "preset_id", "preset_slug", "variant_pricing", "object")
    ID_FIELD_NUMBER: _ClassVar[int]
    SPEC_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    PROGRESS_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_URL_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_SIZE_BYTES_FIELD_NUMBER: _ClassVar[int]
    DURATION_SECONDS_FIELD_NUMBER: _ClassVar[int]
    PRICING_FIELD_NUMBER: _ClassVar[int]
    ESTIMATED_DURATION_SECONDS_FIELD_NUMBER: _ClassVar[int]
    ESTIMATED_COST_FIELD_NUMBER: _ClassVar[int]
    ACTUAL_COST_FIELD_NUMBER: _ClassVar[int]
    ERROR_CODE_FIELD_NUMBER: _ClassVar[int]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    STARTED_AT_FIELD_NUMBER: _ClassVar[int]
    COMPLETED_AT_FIELD_NUMBER: _ClassVar[int]
    PRESET_ID_FIELD_NUMBER: _ClassVar[int]
    PRESET_SLUG_FIELD_NUMBER: _ClassVar[int]
    VARIANT_PRICING_FIELD_NUMBER: _ClassVar[int]
    OBJECT_FIELD_NUMBER: _ClassVar[int]
    id: str
    spec: OutputSpec
    status: OutputStatus
    progress: int
    output_url: str
    output_size_bytes: int
    duration_seconds: int
    pricing: PricingSnapshot
    estimated_duration_seconds: int
    estimated_cost: float
    actual_cost: float
    error_code: str
    error_message: str
    started_at: _timestamp_pb2.Timestamp
    completed_at: _timestamp_pb2.Timestamp
    preset_id: str
    preset_slug: str
    variant_pricing: _containers.RepeatedCompositeFieldContainer[VariantPricingSnapshot]
    object: str
    def __init__(self, id: _Optional[str] = ..., spec: _Optional[_Union[OutputSpec, _Mapping]] = ..., status: _Optional[_Union[OutputStatus, str]] = ..., progress: _Optional[int] = ..., output_url: _Optional[str] = ..., output_size_bytes: _Optional[int] = ..., duration_seconds: _Optional[int] = ..., pricing: _Optional[_Union[PricingSnapshot, _Mapping]] = ..., estimated_duration_seconds: _Optional[int] = ..., estimated_cost: _Optional[float] = ..., actual_cost: _Optional[float] = ..., error_code: _Optional[str] = ..., error_message: _Optional[str] = ..., started_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., completed_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., preset_id: _Optional[str] = ..., preset_slug: _Optional[str] = ..., variant_pricing: _Optional[_Iterable[_Union[VariantPricingSnapshot, _Mapping]]] = ..., object: _Optional[str] = ...) -> None: ...

class ExecutionTiming(_message.Message):
    __slots__ = ("instance_id", "instance_type", "instance_location", "vcpu_count", "memory_mb", "boot_duration_ms", "download_duration_ms", "probe_duration_ms", "encode_duration_ms", "upload_duration_ms", "packaging_duration_ms", "total_duration_ms", "download_bytes", "download_speed_mbps", "upload_bytes", "upload_speed_mbps", "avg_cpu_percent", "peak_cpu_percent", "avg_memory_mb", "peak_memory_mb", "chunk_count", "chunk_strategy", "exit_code", "exit_reason")
    INSTANCE_ID_FIELD_NUMBER: _ClassVar[int]
    INSTANCE_TYPE_FIELD_NUMBER: _ClassVar[int]
    INSTANCE_LOCATION_FIELD_NUMBER: _ClassVar[int]
    VCPU_COUNT_FIELD_NUMBER: _ClassVar[int]
    MEMORY_MB_FIELD_NUMBER: _ClassVar[int]
    BOOT_DURATION_MS_FIELD_NUMBER: _ClassVar[int]
    DOWNLOAD_DURATION_MS_FIELD_NUMBER: _ClassVar[int]
    PROBE_DURATION_MS_FIELD_NUMBER: _ClassVar[int]
    ENCODE_DURATION_MS_FIELD_NUMBER: _ClassVar[int]
    UPLOAD_DURATION_MS_FIELD_NUMBER: _ClassVar[int]
    PACKAGING_DURATION_MS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_DURATION_MS_FIELD_NUMBER: _ClassVar[int]
    DOWNLOAD_BYTES_FIELD_NUMBER: _ClassVar[int]
    DOWNLOAD_SPEED_MBPS_FIELD_NUMBER: _ClassVar[int]
    UPLOAD_BYTES_FIELD_NUMBER: _ClassVar[int]
    UPLOAD_SPEED_MBPS_FIELD_NUMBER: _ClassVar[int]
    AVG_CPU_PERCENT_FIELD_NUMBER: _ClassVar[int]
    PEAK_CPU_PERCENT_FIELD_NUMBER: _ClassVar[int]
    AVG_MEMORY_MB_FIELD_NUMBER: _ClassVar[int]
    PEAK_MEMORY_MB_FIELD_NUMBER: _ClassVar[int]
    CHUNK_COUNT_FIELD_NUMBER: _ClassVar[int]
    CHUNK_STRATEGY_FIELD_NUMBER: _ClassVar[int]
    EXIT_CODE_FIELD_NUMBER: _ClassVar[int]
    EXIT_REASON_FIELD_NUMBER: _ClassVar[int]
    instance_id: str
    instance_type: str
    instance_location: str
    vcpu_count: int
    memory_mb: int
    boot_duration_ms: int
    download_duration_ms: int
    probe_duration_ms: int
    encode_duration_ms: int
    upload_duration_ms: int
    packaging_duration_ms: int
    total_duration_ms: int
    download_bytes: int
    download_speed_mbps: float
    upload_bytes: int
    upload_speed_mbps: float
    avg_cpu_percent: float
    peak_cpu_percent: float
    avg_memory_mb: int
    peak_memory_mb: int
    chunk_count: int
    chunk_strategy: str
    exit_code: int
    exit_reason: str
    def __init__(self, instance_id: _Optional[str] = ..., instance_type: _Optional[str] = ..., instance_location: _Optional[str] = ..., vcpu_count: _Optional[int] = ..., memory_mb: _Optional[int] = ..., boot_duration_ms: _Optional[int] = ..., download_duration_ms: _Optional[int] = ..., probe_duration_ms: _Optional[int] = ..., encode_duration_ms: _Optional[int] = ..., upload_duration_ms: _Optional[int] = ..., packaging_duration_ms: _Optional[int] = ..., total_duration_ms: _Optional[int] = ..., download_bytes: _Optional[int] = ..., download_speed_mbps: _Optional[float] = ..., upload_bytes: _Optional[int] = ..., upload_speed_mbps: _Optional[float] = ..., avg_cpu_percent: _Optional[float] = ..., peak_cpu_percent: _Optional[float] = ..., avg_memory_mb: _Optional[int] = ..., peak_memory_mb: _Optional[int] = ..., chunk_count: _Optional[int] = ..., chunk_strategy: _Optional[str] = ..., exit_code: _Optional[int] = ..., exit_reason: _Optional[str] = ...) -> None: ...

class Job(_message.Message):
    __slots__ = ("id", "input_url", "input_origin", "output_origin", "status", "progress", "priority", "input_metadata", "outputs", "total_estimated_cost", "total_actual_cost", "error_code", "error_message", "webhook_url", "metadata", "created_at", "updated_at", "probed_at", "started_at", "completed_at", "delayed_start", "confirmed_at", "currency", "execution", "thumbnails", "thumbnail_results", "output_path_template", "object")
    class MetadataEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    ID_FIELD_NUMBER: _ClassVar[int]
    INPUT_URL_FIELD_NUMBER: _ClassVar[int]
    INPUT_ORIGIN_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_ORIGIN_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    PROGRESS_FIELD_NUMBER: _ClassVar[int]
    PRIORITY_FIELD_NUMBER: _ClassVar[int]
    INPUT_METADATA_FIELD_NUMBER: _ClassVar[int]
    OUTPUTS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_ESTIMATED_COST_FIELD_NUMBER: _ClassVar[int]
    TOTAL_ACTUAL_COST_FIELD_NUMBER: _ClassVar[int]
    ERROR_CODE_FIELD_NUMBER: _ClassVar[int]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    WEBHOOK_URL_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    PROBED_AT_FIELD_NUMBER: _ClassVar[int]
    STARTED_AT_FIELD_NUMBER: _ClassVar[int]
    COMPLETED_AT_FIELD_NUMBER: _ClassVar[int]
    DELAYED_START_FIELD_NUMBER: _ClassVar[int]
    CONFIRMED_AT_FIELD_NUMBER: _ClassVar[int]
    CURRENCY_FIELD_NUMBER: _ClassVar[int]
    EXECUTION_FIELD_NUMBER: _ClassVar[int]
    THUMBNAILS_FIELD_NUMBER: _ClassVar[int]
    THUMBNAIL_RESULTS_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_PATH_TEMPLATE_FIELD_NUMBER: _ClassVar[int]
    OBJECT_FIELD_NUMBER: _ClassVar[int]
    id: str
    input_url: str
    input_origin: _origin_pb2.OriginRef
    output_origin: _origin_pb2.OriginRef
    status: JobStatus
    progress: int
    priority: JobPriority
    input_metadata: _media_pb2.InputMetadata
    outputs: _containers.RepeatedCompositeFieldContainer[JobOutput]
    total_estimated_cost: float
    total_actual_cost: float
    error_code: str
    error_message: str
    webhook_url: str
    metadata: _containers.ScalarMap[str, str]
    created_at: _timestamp_pb2.Timestamp
    updated_at: _timestamp_pb2.Timestamp
    probed_at: _timestamp_pb2.Timestamp
    started_at: _timestamp_pb2.Timestamp
    completed_at: _timestamp_pb2.Timestamp
    delayed_start: bool
    confirmed_at: _timestamp_pb2.Timestamp
    currency: str
    execution: ExecutionTiming
    thumbnails: _containers.RepeatedCompositeFieldContainer[_thumbnails_pb2.ThumbnailSpec]
    thumbnail_results: _containers.RepeatedCompositeFieldContainer[_thumbnails_pb2.ThumbnailResult]
    output_path_template: str
    object: str
    def __init__(self, id: _Optional[str] = ..., input_url: _Optional[str] = ..., input_origin: _Optional[_Union[_origin_pb2.OriginRef, _Mapping]] = ..., output_origin: _Optional[_Union[_origin_pb2.OriginRef, _Mapping]] = ..., status: _Optional[_Union[JobStatus, str]] = ..., progress: _Optional[int] = ..., priority: _Optional[_Union[JobPriority, str]] = ..., input_metadata: _Optional[_Union[_media_pb2.InputMetadata, _Mapping]] = ..., outputs: _Optional[_Iterable[_Union[JobOutput, _Mapping]]] = ..., total_estimated_cost: _Optional[float] = ..., total_actual_cost: _Optional[float] = ..., error_code: _Optional[str] = ..., error_message: _Optional[str] = ..., webhook_url: _Optional[str] = ..., metadata: _Optional[_Mapping[str, str]] = ..., created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., updated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., probed_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., started_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., completed_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., delayed_start: bool = ..., confirmed_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., currency: _Optional[str] = ..., execution: _Optional[_Union[ExecutionTiming, _Mapping]] = ..., thumbnails: _Optional[_Iterable[_Union[_thumbnails_pb2.ThumbnailSpec, _Mapping]]] = ..., thumbnail_results: _Optional[_Iterable[_Union[_thumbnails_pb2.ThumbnailResult, _Mapping]]] = ..., output_path_template: _Optional[str] = ..., object: _Optional[str] = ...) -> None: ...

class CreateJobRequest(_message.Message):
    __slots__ = ("input_url", "input_origin_id", "input_path", "output_origin_id", "outputs", "priority", "webhook_url", "idempotency_key", "metadata", "delayed_start", "thumbnails", "output_path_template", "managed")
    class MetadataEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    INPUT_URL_FIELD_NUMBER: _ClassVar[int]
    INPUT_ORIGIN_ID_FIELD_NUMBER: _ClassVar[int]
    INPUT_PATH_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_ORIGIN_ID_FIELD_NUMBER: _ClassVar[int]
    OUTPUTS_FIELD_NUMBER: _ClassVar[int]
    PRIORITY_FIELD_NUMBER: _ClassVar[int]
    WEBHOOK_URL_FIELD_NUMBER: _ClassVar[int]
    IDEMPOTENCY_KEY_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    DELAYED_START_FIELD_NUMBER: _ClassVar[int]
    THUMBNAILS_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_PATH_TEMPLATE_FIELD_NUMBER: _ClassVar[int]
    MANAGED_FIELD_NUMBER: _ClassVar[int]
    input_url: str
    input_origin_id: str
    input_path: str
    output_origin_id: str
    outputs: _containers.RepeatedCompositeFieldContainer[OutputSpec]
    priority: JobPriority
    webhook_url: str
    idempotency_key: str
    metadata: _containers.ScalarMap[str, str]
    delayed_start: bool
    thumbnails: _containers.RepeatedCompositeFieldContainer[_thumbnails_pb2.ThumbnailSpec]
    output_path_template: str
    managed: bool
    def __init__(self, input_url: _Optional[str] = ..., input_origin_id: _Optional[str] = ..., input_path: _Optional[str] = ..., output_origin_id: _Optional[str] = ..., outputs: _Optional[_Iterable[_Union[OutputSpec, _Mapping]]] = ..., priority: _Optional[_Union[JobPriority, str]] = ..., webhook_url: _Optional[str] = ..., idempotency_key: _Optional[str] = ..., metadata: _Optional[_Mapping[str, str]] = ..., delayed_start: bool = ..., thumbnails: _Optional[_Iterable[_Union[_thumbnails_pb2.ThumbnailSpec, _Mapping]]] = ..., output_path_template: _Optional[str] = ..., managed: bool = ...) -> None: ...

class CreateJobResponse(_message.Message):
    __slots__ = ("job", "video_id")
    JOB_FIELD_NUMBER: _ClassVar[int]
    VIDEO_ID_FIELD_NUMBER: _ClassVar[int]
    job: Job
    video_id: str
    def __init__(self, job: _Optional[_Union[Job, _Mapping]] = ..., video_id: _Optional[str] = ...) -> None: ...

class GetJobRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GetJobResponse(_message.Message):
    __slots__ = ("job",)
    JOB_FIELD_NUMBER: _ClassVar[int]
    job: Job
    def __init__(self, job: _Optional[_Union[Job, _Mapping]] = ...) -> None: ...

class ListJobsRequest(_message.Message):
    __slots__ = ("status", "pagination")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    status: JobStatus
    pagination: _common_pb2.PaginationRequest
    def __init__(self, status: _Optional[_Union[JobStatus, str]] = ..., pagination: _Optional[_Union[_common_pb2.PaginationRequest, _Mapping]] = ...) -> None: ...

class ListJobsResponse(_message.Message):
    __slots__ = ("jobs", "pagination")
    JOBS_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    jobs: _containers.RepeatedCompositeFieldContainer[Job]
    pagination: _common_pb2.PaginationResponse
    def __init__(self, jobs: _Optional[_Iterable[_Union[Job, _Mapping]]] = ..., pagination: _Optional[_Union[_common_pb2.PaginationResponse, _Mapping]] = ...) -> None: ...

class CancelJobRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class CancelJobResponse(_message.Message):
    __slots__ = ("job",)
    JOB_FIELD_NUMBER: _ClassVar[int]
    job: Job
    def __init__(self, job: _Optional[_Union[Job, _Mapping]] = ...) -> None: ...

class ConfirmJobRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class ConfirmJobResponse(_message.Message):
    __slots__ = ("job",)
    JOB_FIELD_NUMBER: _ClassVar[int]
    job: Job
    def __init__(self, job: _Optional[_Union[Job, _Mapping]] = ...) -> None: ...

class WatchJobRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class WatchJobResponse(_message.Message):
    __slots__ = ("job", "event", "server_time")
    JOB_FIELD_NUMBER: _ClassVar[int]
    EVENT_FIELD_NUMBER: _ClassVar[int]
    SERVER_TIME_FIELD_NUMBER: _ClassVar[int]
    job: Job
    event: WatchEventType
    server_time: _timestamp_pb2.Timestamp
    def __init__(self, job: _Optional[_Union[Job, _Mapping]] = ..., event: _Optional[_Union[WatchEventType, str]] = ..., server_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...
