from buf.validate import validate_pb2 as _validate_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from transcodely.v1 import common_pb2 as _common_pb2
from transcodely.v1 import job_pb2 as _job_pb2
from transcodely.v1 import thumbnails_pb2 as _thumbnails_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class StorageEventSource(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    STORAGE_EVENT_SOURCE_UNSPECIFIED: _ClassVar[StorageEventSource]
    STORAGE_EVENT_SOURCE_S3_SNS: _ClassVar[StorageEventSource]
    STORAGE_EVENT_SOURCE_GCS_PUBSUB: _ClassVar[StorageEventSource]
    STORAGE_EVENT_SOURCE_SUPABASE: _ClassVar[StorageEventSource]
    STORAGE_EVENT_SOURCE_GENERIC: _ClassVar[StorageEventSource]

class StorageEventStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    STORAGE_EVENT_STATUS_UNSPECIFIED: _ClassVar[StorageEventStatus]
    STORAGE_EVENT_STATUS_RECEIVED: _ClassVar[StorageEventStatus]
    STORAGE_EVENT_STATUS_MATCHED: _ClassVar[StorageEventStatus]
    STORAGE_EVENT_STATUS_SKIPPED: _ClassVar[StorageEventStatus]
    STORAGE_EVENT_STATUS_CREATED: _ClassVar[StorageEventStatus]
    STORAGE_EVENT_STATUS_FAILED: _ClassVar[StorageEventStatus]
STORAGE_EVENT_SOURCE_UNSPECIFIED: StorageEventSource
STORAGE_EVENT_SOURCE_S3_SNS: StorageEventSource
STORAGE_EVENT_SOURCE_GCS_PUBSUB: StorageEventSource
STORAGE_EVENT_SOURCE_SUPABASE: StorageEventSource
STORAGE_EVENT_SOURCE_GENERIC: StorageEventSource
STORAGE_EVENT_STATUS_UNSPECIFIED: StorageEventStatus
STORAGE_EVENT_STATUS_RECEIVED: StorageEventStatus
STORAGE_EVENT_STATUS_MATCHED: StorageEventStatus
STORAGE_EVENT_STATUS_SKIPPED: StorageEventStatus
STORAGE_EVENT_STATUS_CREATED: StorageEventStatus
STORAGE_EVENT_STATUS_FAILED: StorageEventStatus

class IngestRule(_message.Message):
    __slots__ = ("id", "app_id", "origin_id", "name", "enabled", "filters", "action", "endpoint_url", "secret_prefix", "secret_hint", "secret_rotated_at", "previous_secret_expires_at", "events_received", "jobs_created", "last_event_at", "created_at", "updated_at")
    ID_FIELD_NUMBER: _ClassVar[int]
    APP_ID_FIELD_NUMBER: _ClassVar[int]
    ORIGIN_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    FILTERS_FIELD_NUMBER: _ClassVar[int]
    ACTION_FIELD_NUMBER: _ClassVar[int]
    ENDPOINT_URL_FIELD_NUMBER: _ClassVar[int]
    SECRET_PREFIX_FIELD_NUMBER: _ClassVar[int]
    SECRET_HINT_FIELD_NUMBER: _ClassVar[int]
    SECRET_ROTATED_AT_FIELD_NUMBER: _ClassVar[int]
    PREVIOUS_SECRET_EXPIRES_AT_FIELD_NUMBER: _ClassVar[int]
    EVENTS_RECEIVED_FIELD_NUMBER: _ClassVar[int]
    JOBS_CREATED_FIELD_NUMBER: _ClassVar[int]
    LAST_EVENT_AT_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    id: str
    app_id: str
    origin_id: str
    name: str
    enabled: bool
    filters: IngestRuleFilters
    action: IngestRuleAction
    endpoint_url: str
    secret_prefix: str
    secret_hint: str
    secret_rotated_at: _timestamp_pb2.Timestamp
    previous_secret_expires_at: _timestamp_pb2.Timestamp
    events_received: int
    jobs_created: int
    last_event_at: _timestamp_pb2.Timestamp
    created_at: _timestamp_pb2.Timestamp
    updated_at: _timestamp_pb2.Timestamp
    def __init__(self, id: _Optional[str] = ..., app_id: _Optional[str] = ..., origin_id: _Optional[str] = ..., name: _Optional[str] = ..., enabled: bool = ..., filters: _Optional[_Union[IngestRuleFilters, _Mapping]] = ..., action: _Optional[_Union[IngestRuleAction, _Mapping]] = ..., endpoint_url: _Optional[str] = ..., secret_prefix: _Optional[str] = ..., secret_hint: _Optional[str] = ..., secret_rotated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., previous_secret_expires_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., events_received: _Optional[int] = ..., jobs_created: _Optional[int] = ..., last_event_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., updated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class IngestRuleFilters(_message.Message):
    __slots__ = ("prefix", "suffixes", "content_types", "min_bytes", "max_bytes")
    PREFIX_FIELD_NUMBER: _ClassVar[int]
    SUFFIXES_FIELD_NUMBER: _ClassVar[int]
    CONTENT_TYPES_FIELD_NUMBER: _ClassVar[int]
    MIN_BYTES_FIELD_NUMBER: _ClassVar[int]
    MAX_BYTES_FIELD_NUMBER: _ClassVar[int]
    prefix: str
    suffixes: _containers.RepeatedScalarFieldContainer[str]
    content_types: _containers.RepeatedScalarFieldContainer[str]
    min_bytes: int
    max_bytes: int
    def __init__(self, prefix: _Optional[str] = ..., suffixes: _Optional[_Iterable[str]] = ..., content_types: _Optional[_Iterable[str]] = ..., min_bytes: _Optional[int] = ..., max_bytes: _Optional[int] = ...) -> None: ...

class IngestRuleAction(_message.Message):
    __slots__ = ("outputs", "managed", "output_origin_id", "output_path_template", "thumbnails", "priority", "metadata")
    class MetadataEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    OUTPUTS_FIELD_NUMBER: _ClassVar[int]
    MANAGED_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_ORIGIN_ID_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_PATH_TEMPLATE_FIELD_NUMBER: _ClassVar[int]
    THUMBNAILS_FIELD_NUMBER: _ClassVar[int]
    PRIORITY_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    outputs: _containers.RepeatedCompositeFieldContainer[_job_pb2.OutputSpec]
    managed: bool
    output_origin_id: str
    output_path_template: str
    thumbnails: _containers.RepeatedCompositeFieldContainer[_thumbnails_pb2.ThumbnailSpec]
    priority: _job_pb2.JobPriority
    metadata: _containers.ScalarMap[str, str]
    def __init__(self, outputs: _Optional[_Iterable[_Union[_job_pb2.OutputSpec, _Mapping]]] = ..., managed: bool = ..., output_origin_id: _Optional[str] = ..., output_path_template: _Optional[str] = ..., thumbnails: _Optional[_Iterable[_Union[_thumbnails_pb2.ThumbnailSpec, _Mapping]]] = ..., priority: _Optional[_Union[_job_pb2.JobPriority, str]] = ..., metadata: _Optional[_Mapping[str, str]] = ...) -> None: ...

class StorageEvent(_message.Message):
    __slots__ = ("id", "rule_id", "app_id", "bucket", "object_key", "etag", "size_bytes", "content_type", "source", "status", "reason", "job_id", "received_at", "processed_at")
    ID_FIELD_NUMBER: _ClassVar[int]
    RULE_ID_FIELD_NUMBER: _ClassVar[int]
    APP_ID_FIELD_NUMBER: _ClassVar[int]
    BUCKET_FIELD_NUMBER: _ClassVar[int]
    OBJECT_KEY_FIELD_NUMBER: _ClassVar[int]
    ETAG_FIELD_NUMBER: _ClassVar[int]
    SIZE_BYTES_FIELD_NUMBER: _ClassVar[int]
    CONTENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    JOB_ID_FIELD_NUMBER: _ClassVar[int]
    RECEIVED_AT_FIELD_NUMBER: _ClassVar[int]
    PROCESSED_AT_FIELD_NUMBER: _ClassVar[int]
    id: str
    rule_id: str
    app_id: str
    bucket: str
    object_key: str
    etag: str
    size_bytes: int
    content_type: str
    source: StorageEventSource
    status: StorageEventStatus
    reason: str
    job_id: str
    received_at: _timestamp_pb2.Timestamp
    processed_at: _timestamp_pb2.Timestamp
    def __init__(self, id: _Optional[str] = ..., rule_id: _Optional[str] = ..., app_id: _Optional[str] = ..., bucket: _Optional[str] = ..., object_key: _Optional[str] = ..., etag: _Optional[str] = ..., size_bytes: _Optional[int] = ..., content_type: _Optional[str] = ..., source: _Optional[_Union[StorageEventSource, str]] = ..., status: _Optional[_Union[StorageEventStatus, str]] = ..., reason: _Optional[str] = ..., job_id: _Optional[str] = ..., received_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., processed_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class CreateIngestRuleRequest(_message.Message):
    __slots__ = ("origin_id", "name", "filters", "action", "enabled", "app_id")
    ORIGIN_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    FILTERS_FIELD_NUMBER: _ClassVar[int]
    ACTION_FIELD_NUMBER: _ClassVar[int]
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    APP_ID_FIELD_NUMBER: _ClassVar[int]
    origin_id: str
    name: str
    filters: IngestRuleFilters
    action: IngestRuleAction
    enabled: bool
    app_id: str
    def __init__(self, origin_id: _Optional[str] = ..., name: _Optional[str] = ..., filters: _Optional[_Union[IngestRuleFilters, _Mapping]] = ..., action: _Optional[_Union[IngestRuleAction, _Mapping]] = ..., enabled: bool = ..., app_id: _Optional[str] = ...) -> None: ...

class CreateIngestRuleResponse(_message.Message):
    __slots__ = ("rule", "secret")
    RULE_FIELD_NUMBER: _ClassVar[int]
    SECRET_FIELD_NUMBER: _ClassVar[int]
    rule: IngestRule
    secret: str
    def __init__(self, rule: _Optional[_Union[IngestRule, _Mapping]] = ..., secret: _Optional[str] = ...) -> None: ...

class GetIngestRuleRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GetIngestRuleResponse(_message.Message):
    __slots__ = ("rule",)
    RULE_FIELD_NUMBER: _ClassVar[int]
    rule: IngestRule
    def __init__(self, rule: _Optional[_Union[IngestRule, _Mapping]] = ...) -> None: ...

class ListIngestRulesRequest(_message.Message):
    __slots__ = ("origin_id", "enabled", "pagination", "app_id")
    ORIGIN_ID_FIELD_NUMBER: _ClassVar[int]
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    APP_ID_FIELD_NUMBER: _ClassVar[int]
    origin_id: str
    enabled: bool
    pagination: _common_pb2.PaginationRequest
    app_id: str
    def __init__(self, origin_id: _Optional[str] = ..., enabled: bool = ..., pagination: _Optional[_Union[_common_pb2.PaginationRequest, _Mapping]] = ..., app_id: _Optional[str] = ...) -> None: ...

class ListIngestRulesResponse(_message.Message):
    __slots__ = ("rules", "pagination")
    RULES_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    rules: _containers.RepeatedCompositeFieldContainer[IngestRule]
    pagination: _common_pb2.PaginationResponse
    def __init__(self, rules: _Optional[_Iterable[_Union[IngestRule, _Mapping]]] = ..., pagination: _Optional[_Union[_common_pb2.PaginationResponse, _Mapping]] = ...) -> None: ...

class UpdateIngestRuleRequest(_message.Message):
    __slots__ = ("id", "name", "enabled", "filters", "action", "rotate_secret")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    FILTERS_FIELD_NUMBER: _ClassVar[int]
    ACTION_FIELD_NUMBER: _ClassVar[int]
    ROTATE_SECRET_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    enabled: bool
    filters: IngestRuleFilters
    action: IngestRuleAction
    rotate_secret: bool
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., enabled: bool = ..., filters: _Optional[_Union[IngestRuleFilters, _Mapping]] = ..., action: _Optional[_Union[IngestRuleAction, _Mapping]] = ..., rotate_secret: bool = ...) -> None: ...

class UpdateIngestRuleResponse(_message.Message):
    __slots__ = ("rule", "secret", "events_skipped_while_disabled")
    RULE_FIELD_NUMBER: _ClassVar[int]
    SECRET_FIELD_NUMBER: _ClassVar[int]
    EVENTS_SKIPPED_WHILE_DISABLED_FIELD_NUMBER: _ClassVar[int]
    rule: IngestRule
    secret: str
    events_skipped_while_disabled: int
    def __init__(self, rule: _Optional[_Union[IngestRule, _Mapping]] = ..., secret: _Optional[str] = ..., events_skipped_while_disabled: _Optional[int] = ...) -> None: ...

class DeleteIngestRuleRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class DeleteIngestRuleResponse(_message.Message):
    __slots__ = ("rule",)
    RULE_FIELD_NUMBER: _ClassVar[int]
    rule: IngestRule
    def __init__(self, rule: _Optional[_Union[IngestRule, _Mapping]] = ...) -> None: ...

class ListIngestEventsRequest(_message.Message):
    __slots__ = ("rule_id", "status", "pagination", "app_id")
    RULE_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    APP_ID_FIELD_NUMBER: _ClassVar[int]
    rule_id: str
    status: StorageEventStatus
    pagination: _common_pb2.PaginationRequest
    app_id: str
    def __init__(self, rule_id: _Optional[str] = ..., status: _Optional[_Union[StorageEventStatus, str]] = ..., pagination: _Optional[_Union[_common_pb2.PaginationRequest, _Mapping]] = ..., app_id: _Optional[str] = ...) -> None: ...

class ListIngestEventsResponse(_message.Message):
    __slots__ = ("events", "pagination")
    EVENTS_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    events: _containers.RepeatedCompositeFieldContainer[StorageEvent]
    pagination: _common_pb2.PaginationResponse
    def __init__(self, events: _Optional[_Iterable[_Union[StorageEvent, _Mapping]]] = ..., pagination: _Optional[_Union[_common_pb2.PaginationResponse, _Mapping]] = ...) -> None: ...

class TestIngestRuleRequest(_message.Message):
    __slots__ = ("id", "object_key", "bucket", "size_bytes", "content_type", "etag")
    ID_FIELD_NUMBER: _ClassVar[int]
    OBJECT_KEY_FIELD_NUMBER: _ClassVar[int]
    BUCKET_FIELD_NUMBER: _ClassVar[int]
    SIZE_BYTES_FIELD_NUMBER: _ClassVar[int]
    CONTENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    ETAG_FIELD_NUMBER: _ClassVar[int]
    id: str
    object_key: str
    bucket: str
    size_bytes: int
    content_type: str
    etag: str
    def __init__(self, id: _Optional[str] = ..., object_key: _Optional[str] = ..., bucket: _Optional[str] = ..., size_bytes: _Optional[int] = ..., content_type: _Optional[str] = ..., etag: _Optional[str] = ...) -> None: ...

class ReplayIngestEventRequest(_message.Message):
    __slots__ = ("event_id",)
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    event_id: str
    def __init__(self, event_id: _Optional[str] = ...) -> None: ...

class ReplayIngestEventResponse(_message.Message):
    __slots__ = ("event",)
    EVENT_FIELD_NUMBER: _ClassVar[int]
    event: StorageEvent
    def __init__(self, event: _Optional[_Union[StorageEvent, _Mapping]] = ...) -> None: ...

class TestIngestRuleResponse(_message.Message):
    __slots__ = ("matched", "reason", "job_request")
    MATCHED_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    JOB_REQUEST_FIELD_NUMBER: _ClassVar[int]
    matched: bool
    reason: str
    job_request: _job_pb2.CreateJobRequest
    def __init__(self, matched: bool = ..., reason: _Optional[str] = ..., job_request: _Optional[_Union[_job_pb2.CreateJobRequest, _Mapping]] = ...) -> None: ...
