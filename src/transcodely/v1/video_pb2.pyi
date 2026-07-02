from buf.validate import validate_pb2 as _validate_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class VideoStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    VIDEO_STATUS_UNSPECIFIED: _ClassVar[VideoStatus]
    VIDEO_STATUS_UPLOADING: _ClassVar[VideoStatus]
    VIDEO_STATUS_PROCESSING: _ClassVar[VideoStatus]
    VIDEO_STATUS_READY: _ClassVar[VideoStatus]
    VIDEO_STATUS_ERROR: _ClassVar[VideoStatus]
    VIDEO_STATUS_ARCHIVED: _ClassVar[VideoStatus]
    VIDEO_STATUS_DELETED: _ClassVar[VideoStatus]

class VideoVisibility(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    VIDEO_VISIBILITY_UNSPECIFIED: _ClassVar[VideoVisibility]
    VIDEO_VISIBILITY_PUBLIC: _ClassVar[VideoVisibility]
    VIDEO_VISIBILITY_UNLISTED: _ClassVar[VideoVisibility]
    VIDEO_VISIBILITY_PRIVATE: _ClassVar[VideoVisibility]
VIDEO_STATUS_UNSPECIFIED: VideoStatus
VIDEO_STATUS_UPLOADING: VideoStatus
VIDEO_STATUS_PROCESSING: VideoStatus
VIDEO_STATUS_READY: VideoStatus
VIDEO_STATUS_ERROR: VideoStatus
VIDEO_STATUS_ARCHIVED: VideoStatus
VIDEO_STATUS_DELETED: VideoStatus
VIDEO_VISIBILITY_UNSPECIFIED: VideoVisibility
VIDEO_VISIBILITY_PUBLIC: VideoVisibility
VIDEO_VISIBILITY_UNLISTED: VideoVisibility
VIDEO_VISIBILITY_PRIVATE: VideoVisibility

class Video(_message.Message):
    __slots__ = ("id", "app_id", "source", "status", "visibility", "title", "description", "tags", "input_size_bytes", "input_content_type", "job_id", "preset", "playback_url", "embed_url", "embed_code", "poster_url", "duration_seconds", "renditions", "output_size_bytes", "encoding_cost", "storage_cost_monthly", "egress_total", "created_at", "updated_at", "ready_at", "object")
    ID_FIELD_NUMBER: _ClassVar[int]
    APP_ID_FIELD_NUMBER: _ClassVar[int]
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    VISIBILITY_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    INPUT_SIZE_BYTES_FIELD_NUMBER: _ClassVar[int]
    INPUT_CONTENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    JOB_ID_FIELD_NUMBER: _ClassVar[int]
    PRESET_FIELD_NUMBER: _ClassVar[int]
    PLAYBACK_URL_FIELD_NUMBER: _ClassVar[int]
    EMBED_URL_FIELD_NUMBER: _ClassVar[int]
    EMBED_CODE_FIELD_NUMBER: _ClassVar[int]
    POSTER_URL_FIELD_NUMBER: _ClassVar[int]
    DURATION_SECONDS_FIELD_NUMBER: _ClassVar[int]
    RENDITIONS_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_SIZE_BYTES_FIELD_NUMBER: _ClassVar[int]
    ENCODING_COST_FIELD_NUMBER: _ClassVar[int]
    STORAGE_COST_MONTHLY_FIELD_NUMBER: _ClassVar[int]
    EGRESS_TOTAL_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    READY_AT_FIELD_NUMBER: _ClassVar[int]
    OBJECT_FIELD_NUMBER: _ClassVar[int]
    id: str
    app_id: str
    source: str
    status: str
    visibility: str
    title: str
    description: str
    tags: _containers.RepeatedScalarFieldContainer[str]
    input_size_bytes: int
    input_content_type: str
    job_id: str
    preset: str
    playback_url: str
    embed_url: str
    embed_code: str
    poster_url: str
    duration_seconds: float
    renditions: _containers.RepeatedCompositeFieldContainer[VideoRendition]
    output_size_bytes: int
    encoding_cost: float
    storage_cost_monthly: float
    egress_total: float
    created_at: _timestamp_pb2.Timestamp
    updated_at: _timestamp_pb2.Timestamp
    ready_at: _timestamp_pb2.Timestamp
    object: str
    def __init__(self, id: _Optional[str] = ..., app_id: _Optional[str] = ..., source: _Optional[str] = ..., status: _Optional[str] = ..., visibility: _Optional[str] = ..., title: _Optional[str] = ..., description: _Optional[str] = ..., tags: _Optional[_Iterable[str]] = ..., input_size_bytes: _Optional[int] = ..., input_content_type: _Optional[str] = ..., job_id: _Optional[str] = ..., preset: _Optional[str] = ..., playback_url: _Optional[str] = ..., embed_url: _Optional[str] = ..., embed_code: _Optional[str] = ..., poster_url: _Optional[str] = ..., duration_seconds: _Optional[float] = ..., renditions: _Optional[_Iterable[_Union[VideoRendition, _Mapping]]] = ..., output_size_bytes: _Optional[int] = ..., encoding_cost: _Optional[float] = ..., storage_cost_monthly: _Optional[float] = ..., egress_total: _Optional[float] = ..., created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., updated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., ready_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., object: _Optional[str] = ...) -> None: ...

class VideoRendition(_message.Message):
    __slots__ = ("id", "resolution", "codec", "bitrate_kbps", "width", "height", "size_bytes")
    ID_FIELD_NUMBER: _ClassVar[int]
    RESOLUTION_FIELD_NUMBER: _ClassVar[int]
    CODEC_FIELD_NUMBER: _ClassVar[int]
    BITRATE_KBPS_FIELD_NUMBER: _ClassVar[int]
    WIDTH_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    SIZE_BYTES_FIELD_NUMBER: _ClassVar[int]
    id: str
    resolution: str
    codec: str
    bitrate_kbps: int
    width: int
    height: int
    size_bytes: int
    def __init__(self, id: _Optional[str] = ..., resolution: _Optional[str] = ..., codec: _Optional[str] = ..., bitrate_kbps: _Optional[int] = ..., width: _Optional[int] = ..., height: _Optional[int] = ..., size_bytes: _Optional[int] = ...) -> None: ...

class CreateUploadRequest(_message.Message):
    __slots__ = ("app_id", "filename", "content_type", "size_bytes", "title", "description", "tags", "visibility", "preset")
    APP_ID_FIELD_NUMBER: _ClassVar[int]
    FILENAME_FIELD_NUMBER: _ClassVar[int]
    CONTENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    SIZE_BYTES_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    VISIBILITY_FIELD_NUMBER: _ClassVar[int]
    PRESET_FIELD_NUMBER: _ClassVar[int]
    app_id: str
    filename: str
    content_type: str
    size_bytes: int
    title: str
    description: str
    tags: _containers.RepeatedScalarFieldContainer[str]
    visibility: str
    preset: str
    def __init__(self, app_id: _Optional[str] = ..., filename: _Optional[str] = ..., content_type: _Optional[str] = ..., size_bytes: _Optional[int] = ..., title: _Optional[str] = ..., description: _Optional[str] = ..., tags: _Optional[_Iterable[str]] = ..., visibility: _Optional[str] = ..., preset: _Optional[str] = ...) -> None: ...

class CreateUploadResponse(_message.Message):
    __slots__ = ("video", "upload_url", "upload_expires_at")
    VIDEO_FIELD_NUMBER: _ClassVar[int]
    UPLOAD_URL_FIELD_NUMBER: _ClassVar[int]
    UPLOAD_EXPIRES_AT_FIELD_NUMBER: _ClassVar[int]
    video: Video
    upload_url: str
    upload_expires_at: _timestamp_pb2.Timestamp
    def __init__(self, video: _Optional[_Union[Video, _Mapping]] = ..., upload_url: _Optional[str] = ..., upload_expires_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class CompleteUploadRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class CompleteUploadResponse(_message.Message):
    __slots__ = ("video",)
    VIDEO_FIELD_NUMBER: _ClassVar[int]
    video: Video
    def __init__(self, video: _Optional[_Union[Video, _Mapping]] = ...) -> None: ...

class UploadPart(_message.Message):
    __slots__ = ("part_number", "upload_url")
    PART_NUMBER_FIELD_NUMBER: _ClassVar[int]
    UPLOAD_URL_FIELD_NUMBER: _ClassVar[int]
    part_number: int
    upload_url: str
    def __init__(self, part_number: _Optional[int] = ..., upload_url: _Optional[str] = ...) -> None: ...

class CompletedPart(_message.Message):
    __slots__ = ("part_number", "etag")
    PART_NUMBER_FIELD_NUMBER: _ClassVar[int]
    ETAG_FIELD_NUMBER: _ClassVar[int]
    part_number: int
    etag: str
    def __init__(self, part_number: _Optional[int] = ..., etag: _Optional[str] = ...) -> None: ...

class CreateMultipartUploadRequest(_message.Message):
    __slots__ = ("app_id", "filename", "content_type", "size_bytes", "total_parts", "part_size_bytes", "title", "description", "tags", "visibility", "preset")
    APP_ID_FIELD_NUMBER: _ClassVar[int]
    FILENAME_FIELD_NUMBER: _ClassVar[int]
    CONTENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    SIZE_BYTES_FIELD_NUMBER: _ClassVar[int]
    TOTAL_PARTS_FIELD_NUMBER: _ClassVar[int]
    PART_SIZE_BYTES_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    VISIBILITY_FIELD_NUMBER: _ClassVar[int]
    PRESET_FIELD_NUMBER: _ClassVar[int]
    app_id: str
    filename: str
    content_type: str
    size_bytes: int
    total_parts: int
    part_size_bytes: int
    title: str
    description: str
    tags: _containers.RepeatedScalarFieldContainer[str]
    visibility: str
    preset: str
    def __init__(self, app_id: _Optional[str] = ..., filename: _Optional[str] = ..., content_type: _Optional[str] = ..., size_bytes: _Optional[int] = ..., total_parts: _Optional[int] = ..., part_size_bytes: _Optional[int] = ..., title: _Optional[str] = ..., description: _Optional[str] = ..., tags: _Optional[_Iterable[str]] = ..., visibility: _Optional[str] = ..., preset: _Optional[str] = ...) -> None: ...

class CreateMultipartUploadResponse(_message.Message):
    __slots__ = ("video", "upload_id", "parts", "urls_expire_at")
    VIDEO_FIELD_NUMBER: _ClassVar[int]
    UPLOAD_ID_FIELD_NUMBER: _ClassVar[int]
    PARTS_FIELD_NUMBER: _ClassVar[int]
    URLS_EXPIRE_AT_FIELD_NUMBER: _ClassVar[int]
    video: Video
    upload_id: str
    parts: _containers.RepeatedCompositeFieldContainer[UploadPart]
    urls_expire_at: _timestamp_pb2.Timestamp
    def __init__(self, video: _Optional[_Union[Video, _Mapping]] = ..., upload_id: _Optional[str] = ..., parts: _Optional[_Iterable[_Union[UploadPart, _Mapping]]] = ..., urls_expire_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class GetUploadPartUrlsRequest(_message.Message):
    __slots__ = ("id", "upload_id", "part_numbers")
    ID_FIELD_NUMBER: _ClassVar[int]
    UPLOAD_ID_FIELD_NUMBER: _ClassVar[int]
    PART_NUMBERS_FIELD_NUMBER: _ClassVar[int]
    id: str
    upload_id: str
    part_numbers: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, id: _Optional[str] = ..., upload_id: _Optional[str] = ..., part_numbers: _Optional[_Iterable[int]] = ...) -> None: ...

class GetUploadPartUrlsResponse(_message.Message):
    __slots__ = ("parts", "urls_expire_at")
    PARTS_FIELD_NUMBER: _ClassVar[int]
    URLS_EXPIRE_AT_FIELD_NUMBER: _ClassVar[int]
    parts: _containers.RepeatedCompositeFieldContainer[UploadPart]
    urls_expire_at: _timestamp_pb2.Timestamp
    def __init__(self, parts: _Optional[_Iterable[_Union[UploadPart, _Mapping]]] = ..., urls_expire_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class CompleteMultipartUploadRequest(_message.Message):
    __slots__ = ("id", "upload_id", "parts")
    ID_FIELD_NUMBER: _ClassVar[int]
    UPLOAD_ID_FIELD_NUMBER: _ClassVar[int]
    PARTS_FIELD_NUMBER: _ClassVar[int]
    id: str
    upload_id: str
    parts: _containers.RepeatedCompositeFieldContainer[CompletedPart]
    def __init__(self, id: _Optional[str] = ..., upload_id: _Optional[str] = ..., parts: _Optional[_Iterable[_Union[CompletedPart, _Mapping]]] = ...) -> None: ...

class CompleteMultipartUploadResponse(_message.Message):
    __slots__ = ("video",)
    VIDEO_FIELD_NUMBER: _ClassVar[int]
    video: Video
    def __init__(self, video: _Optional[_Union[Video, _Mapping]] = ...) -> None: ...

class AbortMultipartUploadRequest(_message.Message):
    __slots__ = ("id", "upload_id")
    ID_FIELD_NUMBER: _ClassVar[int]
    UPLOAD_ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    upload_id: str
    def __init__(self, id: _Optional[str] = ..., upload_id: _Optional[str] = ...) -> None: ...

class AbortMultipartUploadResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetVideoRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GetVideoResponse(_message.Message):
    __slots__ = ("video",)
    VIDEO_FIELD_NUMBER: _ClassVar[int]
    video: Video
    def __init__(self, video: _Optional[_Union[Video, _Mapping]] = ...) -> None: ...

class ListVideosRequest(_message.Message):
    __slots__ = ("page_size", "page_token", "status")
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    page_size: int
    page_token: str
    status: str
    def __init__(self, page_size: _Optional[int] = ..., page_token: _Optional[str] = ..., status: _Optional[str] = ...) -> None: ...

class ListVideosResponse(_message.Message):
    __slots__ = ("videos", "next_page_token", "total_count")
    VIDEOS_FIELD_NUMBER: _ClassVar[int]
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    TOTAL_COUNT_FIELD_NUMBER: _ClassVar[int]
    videos: _containers.RepeatedCompositeFieldContainer[Video]
    next_page_token: str
    total_count: int
    def __init__(self, videos: _Optional[_Iterable[_Union[Video, _Mapping]]] = ..., next_page_token: _Optional[str] = ..., total_count: _Optional[int] = ...) -> None: ...

class UpdateVideoRequest(_message.Message):
    __slots__ = ("id", "title", "description", "tags", "visibility")
    ID_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    VISIBILITY_FIELD_NUMBER: _ClassVar[int]
    id: str
    title: str
    description: str
    tags: _containers.RepeatedScalarFieldContainer[str]
    visibility: str
    def __init__(self, id: _Optional[str] = ..., title: _Optional[str] = ..., description: _Optional[str] = ..., tags: _Optional[_Iterable[str]] = ..., visibility: _Optional[str] = ...) -> None: ...

class UpdateVideoResponse(_message.Message):
    __slots__ = ("video",)
    VIDEO_FIELD_NUMBER: _ClassVar[int]
    video: Video
    def __init__(self, video: _Optional[_Union[Video, _Mapping]] = ...) -> None: ...

class DeleteVideoRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class DeleteVideoResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class WatchVideoRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class WatchVideoResponse(_message.Message):
    __slots__ = ("video", "event_type")
    VIDEO_FIELD_NUMBER: _ClassVar[int]
    EVENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    video: Video
    event_type: str
    def __init__(self, video: _Optional[_Union[Video, _Mapping]] = ..., event_type: _Optional[str] = ...) -> None: ...

class GetUsageRequest(_message.Message):
    __slots__ = ("billing_month",)
    BILLING_MONTH_FIELD_NUMBER: _ClassVar[int]
    billing_month: str
    def __init__(self, billing_month: _Optional[str] = ...) -> None: ...

class GetUsageResponse(_message.Message):
    __slots__ = ("usage",)
    USAGE_FIELD_NUMBER: _ClassVar[int]
    usage: UsageSummary
    def __init__(self, usage: _Optional[_Union[UsageSummary, _Mapping]] = ...) -> None: ...

class UsageSummary(_message.Message):
    __slots__ = ("billing_month", "videos_encoded", "encoding_minutes", "encoding_cost", "storage_gb_avg", "storage_cost", "videos_hosted", "egress_gb", "egress_cost", "total_requests", "total_cost")
    BILLING_MONTH_FIELD_NUMBER: _ClassVar[int]
    VIDEOS_ENCODED_FIELD_NUMBER: _ClassVar[int]
    ENCODING_MINUTES_FIELD_NUMBER: _ClassVar[int]
    ENCODING_COST_FIELD_NUMBER: _ClassVar[int]
    STORAGE_GB_AVG_FIELD_NUMBER: _ClassVar[int]
    STORAGE_COST_FIELD_NUMBER: _ClassVar[int]
    VIDEOS_HOSTED_FIELD_NUMBER: _ClassVar[int]
    EGRESS_GB_FIELD_NUMBER: _ClassVar[int]
    EGRESS_COST_FIELD_NUMBER: _ClassVar[int]
    TOTAL_REQUESTS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_COST_FIELD_NUMBER: _ClassVar[int]
    billing_month: str
    videos_encoded: int
    encoding_minutes: float
    encoding_cost: float
    storage_gb_avg: float
    storage_cost: float
    videos_hosted: int
    egress_gb: float
    egress_cost: float
    total_requests: int
    total_cost: float
    def __init__(self, billing_month: _Optional[str] = ..., videos_encoded: _Optional[int] = ..., encoding_minutes: _Optional[float] = ..., encoding_cost: _Optional[float] = ..., storage_gb_avg: _Optional[float] = ..., storage_cost: _Optional[float] = ..., videos_hosted: _Optional[int] = ..., egress_gb: _Optional[float] = ..., egress_cost: _Optional[float] = ..., total_requests: _Optional[int] = ..., total_cost: _Optional[float] = ...) -> None: ...
