from buf.validate import validate_pb2 as _validate_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from transcodely.v1 import common_pb2 as _common_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AppStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    APP_STATUS_UNSPECIFIED: _ClassVar[AppStatus]
    APP_STATUS_ACTIVE: _ClassVar[AppStatus]
    APP_STATUS_ARCHIVED: _ClassVar[AppStatus]
APP_STATUS_UNSPECIFIED: AppStatus
APP_STATUS_ACTIVE: AppStatus
APP_STATUS_ARCHIVED: AppStatus

class App(_message.Message):
    __slots__ = ("id", "org_id", "name", "description", "status", "created_at", "updated_at", "archived_at", "hosting_enabled", "hosting_status", "cdn_hostname", "hosting_config", "object")
    ID_FIELD_NUMBER: _ClassVar[int]
    ORG_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    ARCHIVED_AT_FIELD_NUMBER: _ClassVar[int]
    HOSTING_ENABLED_FIELD_NUMBER: _ClassVar[int]
    HOSTING_STATUS_FIELD_NUMBER: _ClassVar[int]
    CDN_HOSTNAME_FIELD_NUMBER: _ClassVar[int]
    HOSTING_CONFIG_FIELD_NUMBER: _ClassVar[int]
    OBJECT_FIELD_NUMBER: _ClassVar[int]
    id: str
    org_id: str
    name: str
    description: str
    status: AppStatus
    created_at: _timestamp_pb2.Timestamp
    updated_at: _timestamp_pb2.Timestamp
    archived_at: _timestamp_pb2.Timestamp
    hosting_enabled: bool
    hosting_status: str
    cdn_hostname: str
    hosting_config: HostingConfig
    object: str
    def __init__(self, id: _Optional[str] = ..., org_id: _Optional[str] = ..., name: _Optional[str] = ..., description: _Optional[str] = ..., status: _Optional[_Union[AppStatus, str]] = ..., created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., updated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., archived_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., hosting_enabled: bool = ..., hosting_status: _Optional[str] = ..., cdn_hostname: _Optional[str] = ..., hosting_config: _Optional[_Union[HostingConfig, _Mapping]] = ..., object: _Optional[str] = ...) -> None: ...

class CreateAppRequest(_message.Message):
    __slots__ = ("org_id", "name", "description", "enable_hosting")
    ORG_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    ENABLE_HOSTING_FIELD_NUMBER: _ClassVar[int]
    org_id: str
    name: str
    description: str
    enable_hosting: bool
    def __init__(self, org_id: _Optional[str] = ..., name: _Optional[str] = ..., description: _Optional[str] = ..., enable_hosting: bool = ...) -> None: ...

class CreateAppResponse(_message.Message):
    __slots__ = ("app",)
    APP_FIELD_NUMBER: _ClassVar[int]
    app: App
    def __init__(self, app: _Optional[_Union[App, _Mapping]] = ...) -> None: ...

class GetAppRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GetAppResponse(_message.Message):
    __slots__ = ("app",)
    APP_FIELD_NUMBER: _ClassVar[int]
    app: App
    def __init__(self, app: _Optional[_Union[App, _Mapping]] = ...) -> None: ...

class UpdateAppRequest(_message.Message):
    __slots__ = ("id", "name", "description")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    description: str
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., description: _Optional[str] = ...) -> None: ...

class UpdateAppResponse(_message.Message):
    __slots__ = ("app",)
    APP_FIELD_NUMBER: _ClassVar[int]
    app: App
    def __init__(self, app: _Optional[_Union[App, _Mapping]] = ...) -> None: ...

class ListAppsRequest(_message.Message):
    __slots__ = ("org_id", "pagination", "include_archived")
    ORG_ID_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_ARCHIVED_FIELD_NUMBER: _ClassVar[int]
    org_id: str
    pagination: _common_pb2.PaginationRequest
    include_archived: bool
    def __init__(self, org_id: _Optional[str] = ..., pagination: _Optional[_Union[_common_pb2.PaginationRequest, _Mapping]] = ..., include_archived: bool = ...) -> None: ...

class ListAppsResponse(_message.Message):
    __slots__ = ("apps", "pagination")
    APPS_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    apps: _containers.RepeatedCompositeFieldContainer[App]
    pagination: _common_pb2.PaginationResponse
    def __init__(self, apps: _Optional[_Iterable[_Union[App, _Mapping]]] = ..., pagination: _Optional[_Union[_common_pb2.PaginationResponse, _Mapping]] = ...) -> None: ...

class ArchiveAppRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class ArchiveAppResponse(_message.Message):
    __slots__ = ("app",)
    APP_FIELD_NUMBER: _ClassVar[int]
    app: App
    def __init__(self, app: _Optional[_Union[App, _Mapping]] = ...) -> None: ...

class EnableHostingRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class EnableHostingResponse(_message.Message):
    __slots__ = ("app",)
    APP_FIELD_NUMBER: _ClassVar[int]
    app: App
    def __init__(self, app: _Optional[_Union[App, _Mapping]] = ...) -> None: ...

class HostingConfig(_message.Message):
    __slots__ = ("default_visibility", "max_upload_size_bytes", "cors_allowed_origins", "auto_profile_defaults")
    DEFAULT_VISIBILITY_FIELD_NUMBER: _ClassVar[int]
    MAX_UPLOAD_SIZE_BYTES_FIELD_NUMBER: _ClassVar[int]
    CORS_ALLOWED_ORIGINS_FIELD_NUMBER: _ClassVar[int]
    AUTO_PROFILE_DEFAULTS_FIELD_NUMBER: _ClassVar[int]
    default_visibility: str
    max_upload_size_bytes: int
    cors_allowed_origins: _containers.RepeatedScalarFieldContainer[str]
    auto_profile_defaults: AutoProfileDefaults
    def __init__(self, default_visibility: _Optional[str] = ..., max_upload_size_bytes: _Optional[int] = ..., cors_allowed_origins: _Optional[_Iterable[str]] = ..., auto_profile_defaults: _Optional[_Union[AutoProfileDefaults, _Mapping]] = ...) -> None: ...

class AutoProfileDefaults(_message.Message):
    __slots__ = ("format", "codec", "max_resolution", "quality_tier", "encoding_mode")
    FORMAT_FIELD_NUMBER: _ClassVar[int]
    CODEC_FIELD_NUMBER: _ClassVar[int]
    MAX_RESOLUTION_FIELD_NUMBER: _ClassVar[int]
    QUALITY_TIER_FIELD_NUMBER: _ClassVar[int]
    ENCODING_MODE_FIELD_NUMBER: _ClassVar[int]
    format: str
    codec: str
    max_resolution: str
    quality_tier: str
    encoding_mode: str
    def __init__(self, format: _Optional[str] = ..., codec: _Optional[str] = ..., max_resolution: _Optional[str] = ..., quality_tier: _Optional[str] = ..., encoding_mode: _Optional[str] = ...) -> None: ...

class UpdateHostingConfigRequest(_message.Message):
    __slots__ = ("id", "hosting_config")
    ID_FIELD_NUMBER: _ClassVar[int]
    HOSTING_CONFIG_FIELD_NUMBER: _ClassVar[int]
    id: str
    hosting_config: HostingConfig
    def __init__(self, id: _Optional[str] = ..., hosting_config: _Optional[_Union[HostingConfig, _Mapping]] = ...) -> None: ...

class UpdateHostingConfigResponse(_message.Message):
    __slots__ = ("app",)
    APP_FIELD_NUMBER: _ClassVar[int]
    app: App
    def __init__(self, app: _Optional[_Union[App, _Mapping]] = ...) -> None: ...
