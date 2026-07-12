from buf.validate import validate_pb2 as _validate_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from transcodely.v1 import common_pb2 as _common_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class WebhookEndpoint(_message.Message):
    __slots__ = ("id", "app_id", "url", "description", "enabled_events", "status", "api_version", "metadata", "created_at", "updated_at", "secret", "disabled_reason", "last_rotated_at", "previous_secret_expires_at")
    class MetadataEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    ID_FIELD_NUMBER: _ClassVar[int]
    APP_ID_FIELD_NUMBER: _ClassVar[int]
    URL_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    ENABLED_EVENTS_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    API_VERSION_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    SECRET_FIELD_NUMBER: _ClassVar[int]
    DISABLED_REASON_FIELD_NUMBER: _ClassVar[int]
    LAST_ROTATED_AT_FIELD_NUMBER: _ClassVar[int]
    PREVIOUS_SECRET_EXPIRES_AT_FIELD_NUMBER: _ClassVar[int]
    id: str
    app_id: str
    url: str
    description: str
    enabled_events: _containers.RepeatedScalarFieldContainer[str]
    status: str
    api_version: str
    metadata: _containers.ScalarMap[str, str]
    created_at: _timestamp_pb2.Timestamp
    updated_at: _timestamp_pb2.Timestamp
    secret: str
    disabled_reason: str
    last_rotated_at: _timestamp_pb2.Timestamp
    previous_secret_expires_at: _timestamp_pb2.Timestamp
    def __init__(self, id: _Optional[str] = ..., app_id: _Optional[str] = ..., url: _Optional[str] = ..., description: _Optional[str] = ..., enabled_events: _Optional[_Iterable[str]] = ..., status: _Optional[str] = ..., api_version: _Optional[str] = ..., metadata: _Optional[_Mapping[str, str]] = ..., created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., updated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., secret: _Optional[str] = ..., disabled_reason: _Optional[str] = ..., last_rotated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., previous_secret_expires_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class Event(_message.Message):
    __slots__ = ("id", "app_id", "type", "data", "request_id", "pending_webhooks", "created_at", "api_version", "object")
    ID_FIELD_NUMBER: _ClassVar[int]
    APP_ID_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    PENDING_WEBHOOKS_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    API_VERSION_FIELD_NUMBER: _ClassVar[int]
    OBJECT_FIELD_NUMBER: _ClassVar[int]
    id: str
    app_id: str
    type: str
    data: str
    request_id: str
    pending_webhooks: int
    created_at: _timestamp_pb2.Timestamp
    api_version: str
    object: str
    def __init__(self, id: _Optional[str] = ..., app_id: _Optional[str] = ..., type: _Optional[str] = ..., data: _Optional[str] = ..., request_id: _Optional[str] = ..., pending_webhooks: _Optional[int] = ..., created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., api_version: _Optional[str] = ..., object: _Optional[str] = ...) -> None: ...

class WebhookDelivery(_message.Message):
    __slots__ = ("id", "webhook_endpoint_id", "event_id", "status", "attempt", "response_status", "response_body", "next_attempt_at", "created_at", "updated_at", "latency_ms", "transport_error", "response_headers", "error_message")
    ID_FIELD_NUMBER: _ClassVar[int]
    WEBHOOK_ENDPOINT_ID_FIELD_NUMBER: _ClassVar[int]
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    ATTEMPT_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_STATUS_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_BODY_FIELD_NUMBER: _ClassVar[int]
    NEXT_ATTEMPT_AT_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    LATENCY_MS_FIELD_NUMBER: _ClassVar[int]
    TRANSPORT_ERROR_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_HEADERS_FIELD_NUMBER: _ClassVar[int]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    id: str
    webhook_endpoint_id: str
    event_id: str
    status: str
    attempt: int
    response_status: int
    response_body: str
    next_attempt_at: _timestamp_pb2.Timestamp
    created_at: _timestamp_pb2.Timestamp
    updated_at: _timestamp_pb2.Timestamp
    latency_ms: int
    transport_error: str
    response_headers: str
    error_message: str
    def __init__(self, id: _Optional[str] = ..., webhook_endpoint_id: _Optional[str] = ..., event_id: _Optional[str] = ..., status: _Optional[str] = ..., attempt: _Optional[int] = ..., response_status: _Optional[int] = ..., response_body: _Optional[str] = ..., next_attempt_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., updated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., latency_ms: _Optional[int] = ..., transport_error: _Optional[str] = ..., response_headers: _Optional[str] = ..., error_message: _Optional[str] = ...) -> None: ...

class CreateWebhookEndpointRequest(_message.Message):
    __slots__ = ("app_id", "url", "description", "enabled_events", "api_version", "metadata")
    class MetadataEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    APP_ID_FIELD_NUMBER: _ClassVar[int]
    URL_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    ENABLED_EVENTS_FIELD_NUMBER: _ClassVar[int]
    API_VERSION_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    app_id: str
    url: str
    description: str
    enabled_events: _containers.RepeatedScalarFieldContainer[str]
    api_version: str
    metadata: _containers.ScalarMap[str, str]
    def __init__(self, app_id: _Optional[str] = ..., url: _Optional[str] = ..., description: _Optional[str] = ..., enabled_events: _Optional[_Iterable[str]] = ..., api_version: _Optional[str] = ..., metadata: _Optional[_Mapping[str, str]] = ...) -> None: ...

class CreateWebhookEndpointResponse(_message.Message):
    __slots__ = ("endpoint",)
    ENDPOINT_FIELD_NUMBER: _ClassVar[int]
    endpoint: WebhookEndpoint
    def __init__(self, endpoint: _Optional[_Union[WebhookEndpoint, _Mapping]] = ...) -> None: ...

class RetrieveWebhookEndpointRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class RetrieveWebhookEndpointResponse(_message.Message):
    __slots__ = ("endpoint",)
    ENDPOINT_FIELD_NUMBER: _ClassVar[int]
    endpoint: WebhookEndpoint
    def __init__(self, endpoint: _Optional[_Union[WebhookEndpoint, _Mapping]] = ...) -> None: ...

class UpdateWebhookEndpointRequest(_message.Message):
    __slots__ = ("id", "url", "description", "enabled_events", "status", "metadata")
    class MetadataEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    ID_FIELD_NUMBER: _ClassVar[int]
    URL_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    ENABLED_EVENTS_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    id: str
    url: str
    description: str
    enabled_events: _containers.RepeatedScalarFieldContainer[str]
    status: str
    metadata: _containers.ScalarMap[str, str]
    def __init__(self, id: _Optional[str] = ..., url: _Optional[str] = ..., description: _Optional[str] = ..., enabled_events: _Optional[_Iterable[str]] = ..., status: _Optional[str] = ..., metadata: _Optional[_Mapping[str, str]] = ...) -> None: ...

class UpdateWebhookEndpointResponse(_message.Message):
    __slots__ = ("endpoint",)
    ENDPOINT_FIELD_NUMBER: _ClassVar[int]
    endpoint: WebhookEndpoint
    def __init__(self, endpoint: _Optional[_Union[WebhookEndpoint, _Mapping]] = ...) -> None: ...

class DeleteWebhookEndpointRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class DeleteWebhookEndpointResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListWebhookEndpointsRequest(_message.Message):
    __slots__ = ("app_id", "pagination")
    APP_ID_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    app_id: str
    pagination: _common_pb2.PaginationRequest
    def __init__(self, app_id: _Optional[str] = ..., pagination: _Optional[_Union[_common_pb2.PaginationRequest, _Mapping]] = ...) -> None: ...

class ListWebhookEndpointsResponse(_message.Message):
    __slots__ = ("endpoints", "pagination")
    ENDPOINTS_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    endpoints: _containers.RepeatedCompositeFieldContainer[WebhookEndpoint]
    pagination: _common_pb2.PaginationResponse
    def __init__(self, endpoints: _Optional[_Iterable[_Union[WebhookEndpoint, _Mapping]]] = ..., pagination: _Optional[_Union[_common_pb2.PaginationResponse, _Mapping]] = ...) -> None: ...

class RotateWebhookSecretRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class RotateWebhookSecretResponse(_message.Message):
    __slots__ = ("endpoint",)
    ENDPOINT_FIELD_NUMBER: _ClassVar[int]
    endpoint: WebhookEndpoint
    def __init__(self, endpoint: _Optional[_Union[WebhookEndpoint, _Mapping]] = ...) -> None: ...

class ListEventsRequest(_message.Message):
    __slots__ = ("app_id", "type", "created_after", "created_before", "pagination")
    APP_ID_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    CREATED_AFTER_FIELD_NUMBER: _ClassVar[int]
    CREATED_BEFORE_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    app_id: str
    type: str
    created_after: _timestamp_pb2.Timestamp
    created_before: _timestamp_pb2.Timestamp
    pagination: _common_pb2.PaginationRequest
    def __init__(self, app_id: _Optional[str] = ..., type: _Optional[str] = ..., created_after: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., created_before: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., pagination: _Optional[_Union[_common_pb2.PaginationRequest, _Mapping]] = ...) -> None: ...

class ListEventsResponse(_message.Message):
    __slots__ = ("events", "pagination")
    EVENTS_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    events: _containers.RepeatedCompositeFieldContainer[Event]
    pagination: _common_pb2.PaginationResponse
    def __init__(self, events: _Optional[_Iterable[_Union[Event, _Mapping]]] = ..., pagination: _Optional[_Union[_common_pb2.PaginationResponse, _Mapping]] = ...) -> None: ...

class RetrieveEventRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class RetrieveEventResponse(_message.Message):
    __slots__ = ("event",)
    EVENT_FIELD_NUMBER: _ClassVar[int]
    event: Event
    def __init__(self, event: _Optional[_Union[Event, _Mapping]] = ...) -> None: ...

class ResendEventRequest(_message.Message):
    __slots__ = ("id", "endpoint_ids")
    ID_FIELD_NUMBER: _ClassVar[int]
    ENDPOINT_IDS_FIELD_NUMBER: _ClassVar[int]
    id: str
    endpoint_ids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, id: _Optional[str] = ..., endpoint_ids: _Optional[_Iterable[str]] = ...) -> None: ...

class ResendEventResponse(_message.Message):
    __slots__ = ("deliveries",)
    DELIVERIES_FIELD_NUMBER: _ClassVar[int]
    deliveries: _containers.RepeatedCompositeFieldContainer[WebhookDelivery]
    def __init__(self, deliveries: _Optional[_Iterable[_Union[WebhookDelivery, _Mapping]]] = ...) -> None: ...

class SendTestWebhookRequest(_message.Message):
    __slots__ = ("endpoint_id", "event_type")
    ENDPOINT_ID_FIELD_NUMBER: _ClassVar[int]
    EVENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    endpoint_id: str
    event_type: str
    def __init__(self, endpoint_id: _Optional[str] = ..., event_type: _Optional[str] = ...) -> None: ...

class SendTestWebhookResponse(_message.Message):
    __slots__ = ("delivery",)
    DELIVERY_FIELD_NUMBER: _ClassVar[int]
    delivery: WebhookDelivery
    def __init__(self, delivery: _Optional[_Union[WebhookDelivery, _Mapping]] = ...) -> None: ...

class ListWebhookDeliveriesRequest(_message.Message):
    __slots__ = ("endpoint_id", "event_id", "status", "pagination")
    ENDPOINT_ID_FIELD_NUMBER: _ClassVar[int]
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    endpoint_id: str
    event_id: str
    status: str
    pagination: _common_pb2.PaginationRequest
    def __init__(self, endpoint_id: _Optional[str] = ..., event_id: _Optional[str] = ..., status: _Optional[str] = ..., pagination: _Optional[_Union[_common_pb2.PaginationRequest, _Mapping]] = ...) -> None: ...

class ListWebhookDeliveriesResponse(_message.Message):
    __slots__ = ("deliveries", "pagination")
    DELIVERIES_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    deliveries: _containers.RepeatedCompositeFieldContainer[WebhookDelivery]
    pagination: _common_pb2.PaginationResponse
    def __init__(self, deliveries: _Optional[_Iterable[_Union[WebhookDelivery, _Mapping]]] = ..., pagination: _Optional[_Union[_common_pb2.PaginationResponse, _Mapping]] = ...) -> None: ...

class GetEndpointHealthRequest(_message.Message):
    __slots__ = ("endpoint_id", "window")
    ENDPOINT_ID_FIELD_NUMBER: _ClassVar[int]
    WINDOW_FIELD_NUMBER: _ClassVar[int]
    endpoint_id: str
    window: str
    def __init__(self, endpoint_id: _Optional[str] = ..., window: _Optional[str] = ...) -> None: ...

class GetEndpointHealthResponse(_message.Message):
    __slots__ = ("window", "total_attempts", "succeeded", "failed", "pending", "success_rate", "p50_latency_ms", "p95_latency_ms", "buckets")
    WINDOW_FIELD_NUMBER: _ClassVar[int]
    TOTAL_ATTEMPTS_FIELD_NUMBER: _ClassVar[int]
    SUCCEEDED_FIELD_NUMBER: _ClassVar[int]
    FAILED_FIELD_NUMBER: _ClassVar[int]
    PENDING_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_RATE_FIELD_NUMBER: _ClassVar[int]
    P50_LATENCY_MS_FIELD_NUMBER: _ClassVar[int]
    P95_LATENCY_MS_FIELD_NUMBER: _ClassVar[int]
    BUCKETS_FIELD_NUMBER: _ClassVar[int]
    window: str
    total_attempts: int
    succeeded: int
    failed: int
    pending: int
    success_rate: float
    p50_latency_ms: int
    p95_latency_ms: int
    buckets: _containers.RepeatedCompositeFieldContainer[HealthBucket]
    def __init__(self, window: _Optional[str] = ..., total_attempts: _Optional[int] = ..., succeeded: _Optional[int] = ..., failed: _Optional[int] = ..., pending: _Optional[int] = ..., success_rate: _Optional[float] = ..., p50_latency_ms: _Optional[int] = ..., p95_latency_ms: _Optional[int] = ..., buckets: _Optional[_Iterable[_Union[HealthBucket, _Mapping]]] = ...) -> None: ...

class HealthBucket(_message.Message):
    __slots__ = ("bucket_start", "attempts", "succeeded", "failed", "pending")
    BUCKET_START_FIELD_NUMBER: _ClassVar[int]
    ATTEMPTS_FIELD_NUMBER: _ClassVar[int]
    SUCCEEDED_FIELD_NUMBER: _ClassVar[int]
    FAILED_FIELD_NUMBER: _ClassVar[int]
    PENDING_FIELD_NUMBER: _ClassVar[int]
    bucket_start: _timestamp_pb2.Timestamp
    attempts: int
    succeeded: int
    failed: int
    pending: int
    def __init__(self, bucket_start: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., attempts: _Optional[int] = ..., succeeded: _Optional[int] = ..., failed: _Optional[int] = ..., pending: _Optional[int] = ...) -> None: ...
