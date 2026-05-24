from buf.validate import validate_pb2 as _validate_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from transcodely.v1 import common_pb2 as _common_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class OriginProvider(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ORIGIN_PROVIDER_UNSPECIFIED: _ClassVar[OriginProvider]
    ORIGIN_PROVIDER_GCS: _ClassVar[OriginProvider]
    ORIGIN_PROVIDER_S3: _ClassVar[OriginProvider]
    ORIGIN_PROVIDER_HTTP: _ClassVar[OriginProvider]
    ORIGIN_PROVIDER_TRANSCODELY: _ClassVar[OriginProvider]
    ORIGIN_PROVIDER_R2: _ClassVar[OriginProvider]

class R2Jurisdiction(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    R2_JURISDICTION_UNSPECIFIED: _ClassVar[R2Jurisdiction]
    R2_JURISDICTION_DEFAULT: _ClassVar[R2Jurisdiction]
    R2_JURISDICTION_EU: _ClassVar[R2Jurisdiction]
    R2_JURISDICTION_FEDRAMP: _ClassVar[R2Jurisdiction]

class OriginPermission(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ORIGIN_PERMISSION_UNSPECIFIED: _ClassVar[OriginPermission]
    ORIGIN_PERMISSION_READ: _ClassVar[OriginPermission]
    ORIGIN_PERMISSION_WRITE: _ClassVar[OriginPermission]

class OriginStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ORIGIN_STATUS_UNSPECIFIED: _ClassVar[OriginStatus]
    ORIGIN_STATUS_ACTIVE: _ClassVar[OriginStatus]
    ORIGIN_STATUS_FAILED: _ClassVar[OriginStatus]
    ORIGIN_STATUS_ARCHIVED: _ClassVar[OriginStatus]
ORIGIN_PROVIDER_UNSPECIFIED: OriginProvider
ORIGIN_PROVIDER_GCS: OriginProvider
ORIGIN_PROVIDER_S3: OriginProvider
ORIGIN_PROVIDER_HTTP: OriginProvider
ORIGIN_PROVIDER_TRANSCODELY: OriginProvider
ORIGIN_PROVIDER_R2: OriginProvider
R2_JURISDICTION_UNSPECIFIED: R2Jurisdiction
R2_JURISDICTION_DEFAULT: R2Jurisdiction
R2_JURISDICTION_EU: R2Jurisdiction
R2_JURISDICTION_FEDRAMP: R2Jurisdiction
ORIGIN_PERMISSION_UNSPECIFIED: OriginPermission
ORIGIN_PERMISSION_READ: OriginPermission
ORIGIN_PERMISSION_WRITE: OriginPermission
ORIGIN_STATUS_UNSPECIFIED: OriginStatus
ORIGIN_STATUS_ACTIVE: OriginStatus
ORIGIN_STATUS_FAILED: OriginStatus
ORIGIN_STATUS_ARCHIVED: OriginStatus

class GcsCredentials(_message.Message):
    __slots__ = ("service_account_json",)
    SERVICE_ACCOUNT_JSON_FIELD_NUMBER: _ClassVar[int]
    service_account_json: str
    def __init__(self, service_account_json: _Optional[str] = ...) -> None: ...

class S3Credentials(_message.Message):
    __slots__ = ("access_key_id", "secret_access_key")
    ACCESS_KEY_ID_FIELD_NUMBER: _ClassVar[int]
    SECRET_ACCESS_KEY_FIELD_NUMBER: _ClassVar[int]
    access_key_id: str
    secret_access_key: str
    def __init__(self, access_key_id: _Optional[str] = ..., secret_access_key: _Optional[str] = ...) -> None: ...

class HttpCredentials(_message.Message):
    __slots__ = ("headers",)
    class HeadersEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    HEADERS_FIELD_NUMBER: _ClassVar[int]
    headers: _containers.ScalarMap[str, str]
    def __init__(self, headers: _Optional[_Mapping[str, str]] = ...) -> None: ...

class GcsOriginConfig(_message.Message):
    __slots__ = ("bucket", "credentials")
    BUCKET_FIELD_NUMBER: _ClassVar[int]
    CREDENTIALS_FIELD_NUMBER: _ClassVar[int]
    bucket: str
    credentials: GcsCredentials
    def __init__(self, bucket: _Optional[str] = ..., credentials: _Optional[_Union[GcsCredentials, _Mapping]] = ...) -> None: ...

class S3OriginConfig(_message.Message):
    __slots__ = ("bucket", "region", "credentials", "endpoint")
    BUCKET_FIELD_NUMBER: _ClassVar[int]
    REGION_FIELD_NUMBER: _ClassVar[int]
    CREDENTIALS_FIELD_NUMBER: _ClassVar[int]
    ENDPOINT_FIELD_NUMBER: _ClassVar[int]
    bucket: str
    region: str
    credentials: S3Credentials
    endpoint: str
    def __init__(self, bucket: _Optional[str] = ..., region: _Optional[str] = ..., credentials: _Optional[_Union[S3Credentials, _Mapping]] = ..., endpoint: _Optional[str] = ...) -> None: ...

class HttpOriginConfig(_message.Message):
    __slots__ = ("base_url", "credentials")
    BASE_URL_FIELD_NUMBER: _ClassVar[int]
    CREDENTIALS_FIELD_NUMBER: _ClassVar[int]
    base_url: str
    credentials: HttpCredentials
    def __init__(self, base_url: _Optional[str] = ..., credentials: _Optional[_Union[HttpCredentials, _Mapping]] = ...) -> None: ...

class R2OriginConfig(_message.Message):
    __slots__ = ("bucket", "credentials", "account_id", "jurisdiction", "endpoint")
    BUCKET_FIELD_NUMBER: _ClassVar[int]
    CREDENTIALS_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    JURISDICTION_FIELD_NUMBER: _ClassVar[int]
    ENDPOINT_FIELD_NUMBER: _ClassVar[int]
    bucket: str
    credentials: S3Credentials
    account_id: str
    jurisdiction: R2Jurisdiction
    endpoint: str
    def __init__(self, bucket: _Optional[str] = ..., credentials: _Optional[_Union[S3Credentials, _Mapping]] = ..., account_id: _Optional[str] = ..., jurisdiction: _Optional[_Union[R2Jurisdiction, str]] = ..., endpoint: _Optional[str] = ...) -> None: ...

class OriginRef(_message.Message):
    __slots__ = ("id", "name", "provider", "path", "bucket", "base_url")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    PROVIDER_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    BUCKET_FIELD_NUMBER: _ClassVar[int]
    BASE_URL_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    provider: OriginProvider
    path: str
    bucket: str
    base_url: str
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., provider: _Optional[_Union[OriginProvider, str]] = ..., path: _Optional[str] = ..., bucket: _Optional[str] = ..., base_url: _Optional[str] = ...) -> None: ...

class Origin(_message.Message):
    __slots__ = ("id", "name", "description", "provider", "permissions", "status", "base_path", "path_template", "gcs", "s3", "http", "last_validated_at", "validation_error", "created_at", "updated_at", "archived_at", "is_managed", "r2")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    PROVIDER_FIELD_NUMBER: _ClassVar[int]
    PERMISSIONS_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    BASE_PATH_FIELD_NUMBER: _ClassVar[int]
    PATH_TEMPLATE_FIELD_NUMBER: _ClassVar[int]
    GCS_FIELD_NUMBER: _ClassVar[int]
    S3_FIELD_NUMBER: _ClassVar[int]
    HTTP_FIELD_NUMBER: _ClassVar[int]
    LAST_VALIDATED_AT_FIELD_NUMBER: _ClassVar[int]
    VALIDATION_ERROR_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    ARCHIVED_AT_FIELD_NUMBER: _ClassVar[int]
    IS_MANAGED_FIELD_NUMBER: _ClassVar[int]
    R2_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    description: str
    provider: OriginProvider
    permissions: _containers.RepeatedScalarFieldContainer[OriginPermission]
    status: OriginStatus
    base_path: str
    path_template: str
    gcs: GcsOriginConfig
    s3: S3OriginConfig
    http: HttpOriginConfig
    last_validated_at: _timestamp_pb2.Timestamp
    validation_error: str
    created_at: _timestamp_pb2.Timestamp
    updated_at: _timestamp_pb2.Timestamp
    archived_at: _timestamp_pb2.Timestamp
    is_managed: bool
    r2: R2OriginConfig
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., description: _Optional[str] = ..., provider: _Optional[_Union[OriginProvider, str]] = ..., permissions: _Optional[_Iterable[_Union[OriginPermission, str]]] = ..., status: _Optional[_Union[OriginStatus, str]] = ..., base_path: _Optional[str] = ..., path_template: _Optional[str] = ..., gcs: _Optional[_Union[GcsOriginConfig, _Mapping]] = ..., s3: _Optional[_Union[S3OriginConfig, _Mapping]] = ..., http: _Optional[_Union[HttpOriginConfig, _Mapping]] = ..., last_validated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., validation_error: _Optional[str] = ..., created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., updated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., archived_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., is_managed: bool = ..., r2: _Optional[_Union[R2OriginConfig, _Mapping]] = ...) -> None: ...

class CreateOriginRequest(_message.Message):
    __slots__ = ("name", "description", "permissions", "base_path", "path_template", "gcs", "s3", "http", "r2")
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    PERMISSIONS_FIELD_NUMBER: _ClassVar[int]
    BASE_PATH_FIELD_NUMBER: _ClassVar[int]
    PATH_TEMPLATE_FIELD_NUMBER: _ClassVar[int]
    GCS_FIELD_NUMBER: _ClassVar[int]
    S3_FIELD_NUMBER: _ClassVar[int]
    HTTP_FIELD_NUMBER: _ClassVar[int]
    R2_FIELD_NUMBER: _ClassVar[int]
    name: str
    description: str
    permissions: _containers.RepeatedScalarFieldContainer[OriginPermission]
    base_path: str
    path_template: str
    gcs: GcsOriginConfig
    s3: S3OriginConfig
    http: HttpOriginConfig
    r2: R2OriginConfig
    def __init__(self, name: _Optional[str] = ..., description: _Optional[str] = ..., permissions: _Optional[_Iterable[_Union[OriginPermission, str]]] = ..., base_path: _Optional[str] = ..., path_template: _Optional[str] = ..., gcs: _Optional[_Union[GcsOriginConfig, _Mapping]] = ..., s3: _Optional[_Union[S3OriginConfig, _Mapping]] = ..., http: _Optional[_Union[HttpOriginConfig, _Mapping]] = ..., r2: _Optional[_Union[R2OriginConfig, _Mapping]] = ...) -> None: ...

class CreateOriginResponse(_message.Message):
    __slots__ = ("origin", "validation")
    ORIGIN_FIELD_NUMBER: _ClassVar[int]
    VALIDATION_FIELD_NUMBER: _ClassVar[int]
    origin: Origin
    validation: ValidationResult
    def __init__(self, origin: _Optional[_Union[Origin, _Mapping]] = ..., validation: _Optional[_Union[ValidationResult, _Mapping]] = ...) -> None: ...

class ValidationResult(_message.Message):
    __slots__ = ("success", "can_read", "can_write", "read_error", "write_error", "validated_at")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    CAN_READ_FIELD_NUMBER: _ClassVar[int]
    CAN_WRITE_FIELD_NUMBER: _ClassVar[int]
    READ_ERROR_FIELD_NUMBER: _ClassVar[int]
    WRITE_ERROR_FIELD_NUMBER: _ClassVar[int]
    VALIDATED_AT_FIELD_NUMBER: _ClassVar[int]
    success: bool
    can_read: bool
    can_write: bool
    read_error: str
    write_error: str
    validated_at: _timestamp_pb2.Timestamp
    def __init__(self, success: bool = ..., can_read: bool = ..., can_write: bool = ..., read_error: _Optional[str] = ..., write_error: _Optional[str] = ..., validated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class GetOriginRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GetOriginResponse(_message.Message):
    __slots__ = ("origin",)
    ORIGIN_FIELD_NUMBER: _ClassVar[int]
    origin: Origin
    def __init__(self, origin: _Optional[_Union[Origin, _Mapping]] = ...) -> None: ...

class ListOriginsRequest(_message.Message):
    __slots__ = ("provider", "status", "permission", "include_archived", "pagination")
    PROVIDER_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    PERMISSION_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_ARCHIVED_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    provider: OriginProvider
    status: OriginStatus
    permission: OriginPermission
    include_archived: bool
    pagination: _common_pb2.PaginationRequest
    def __init__(self, provider: _Optional[_Union[OriginProvider, str]] = ..., status: _Optional[_Union[OriginStatus, str]] = ..., permission: _Optional[_Union[OriginPermission, str]] = ..., include_archived: bool = ..., pagination: _Optional[_Union[_common_pb2.PaginationRequest, _Mapping]] = ...) -> None: ...

class ListOriginsResponse(_message.Message):
    __slots__ = ("origins", "pagination")
    ORIGINS_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    origins: _containers.RepeatedCompositeFieldContainer[Origin]
    pagination: _common_pb2.PaginationResponse
    def __init__(self, origins: _Optional[_Iterable[_Union[Origin, _Mapping]]] = ..., pagination: _Optional[_Union[_common_pb2.PaginationResponse, _Mapping]] = ...) -> None: ...

class UpdateOriginRequest(_message.Message):
    __slots__ = ("id", "name", "description", "base_path", "path_template", "gcs_credentials", "s3_credentials", "http_credentials", "r2_credentials")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    BASE_PATH_FIELD_NUMBER: _ClassVar[int]
    PATH_TEMPLATE_FIELD_NUMBER: _ClassVar[int]
    GCS_CREDENTIALS_FIELD_NUMBER: _ClassVar[int]
    S3_CREDENTIALS_FIELD_NUMBER: _ClassVar[int]
    HTTP_CREDENTIALS_FIELD_NUMBER: _ClassVar[int]
    R2_CREDENTIALS_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    description: str
    base_path: str
    path_template: str
    gcs_credentials: GcsCredentials
    s3_credentials: S3Credentials
    http_credentials: HttpCredentials
    r2_credentials: S3Credentials
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., description: _Optional[str] = ..., base_path: _Optional[str] = ..., path_template: _Optional[str] = ..., gcs_credentials: _Optional[_Union[GcsCredentials, _Mapping]] = ..., s3_credentials: _Optional[_Union[S3Credentials, _Mapping]] = ..., http_credentials: _Optional[_Union[HttpCredentials, _Mapping]] = ..., r2_credentials: _Optional[_Union[S3Credentials, _Mapping]] = ...) -> None: ...

class UpdateOriginResponse(_message.Message):
    __slots__ = ("origin", "validation")
    ORIGIN_FIELD_NUMBER: _ClassVar[int]
    VALIDATION_FIELD_NUMBER: _ClassVar[int]
    origin: Origin
    validation: ValidationResult
    def __init__(self, origin: _Optional[_Union[Origin, _Mapping]] = ..., validation: _Optional[_Union[ValidationResult, _Mapping]] = ...) -> None: ...

class ValidateOriginRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class ValidateOriginResponse(_message.Message):
    __slots__ = ("origin", "validation")
    ORIGIN_FIELD_NUMBER: _ClassVar[int]
    VALIDATION_FIELD_NUMBER: _ClassVar[int]
    origin: Origin
    validation: ValidationResult
    def __init__(self, origin: _Optional[_Union[Origin, _Mapping]] = ..., validation: _Optional[_Union[ValidationResult, _Mapping]] = ...) -> None: ...

class ArchiveOriginRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class ArchiveOriginResponse(_message.Message):
    __slots__ = ("origin",)
    ORIGIN_FIELD_NUMBER: _ClassVar[int]
    origin: Origin
    def __init__(self, origin: _Optional[_Union[Origin, _Mapping]] = ...) -> None: ...
