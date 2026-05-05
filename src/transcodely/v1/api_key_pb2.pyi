from buf.validate import validate_pb2 as _validate_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from transcodely.v1 import common_pb2 as _common_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class APIKeyEnvironment(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    API_KEY_ENVIRONMENT_UNSPECIFIED: _ClassVar[APIKeyEnvironment]
    API_KEY_ENVIRONMENT_LIVE: _ClassVar[APIKeyEnvironment]
    API_KEY_ENVIRONMENT_TEST: _ClassVar[APIKeyEnvironment]
API_KEY_ENVIRONMENT_UNSPECIFIED: APIKeyEnvironment
API_KEY_ENVIRONMENT_LIVE: APIKeyEnvironment
API_KEY_ENVIRONMENT_TEST: APIKeyEnvironment

class APIKey(_message.Message):
    __slots__ = ("id", "name", "description", "key_prefix", "key_hint", "environment", "scopes", "last_used_at", "expires_at", "created_at", "is_revoked", "revoked_at")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    KEY_PREFIX_FIELD_NUMBER: _ClassVar[int]
    KEY_HINT_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_FIELD_NUMBER: _ClassVar[int]
    SCOPES_FIELD_NUMBER: _ClassVar[int]
    LAST_USED_AT_FIELD_NUMBER: _ClassVar[int]
    EXPIRES_AT_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    IS_REVOKED_FIELD_NUMBER: _ClassVar[int]
    REVOKED_AT_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    description: str
    key_prefix: str
    key_hint: str
    environment: APIKeyEnvironment
    scopes: _containers.RepeatedScalarFieldContainer[str]
    last_used_at: _timestamp_pb2.Timestamp
    expires_at: _timestamp_pb2.Timestamp
    created_at: _timestamp_pb2.Timestamp
    is_revoked: bool
    revoked_at: _timestamp_pb2.Timestamp
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., description: _Optional[str] = ..., key_prefix: _Optional[str] = ..., key_hint: _Optional[str] = ..., environment: _Optional[_Union[APIKeyEnvironment, str]] = ..., scopes: _Optional[_Iterable[str]] = ..., last_used_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., expires_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., is_revoked: bool = ..., revoked_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class CreateAPIKeyRequest(_message.Message):
    __slots__ = ("name", "description", "environment", "expires_at", "app_id")
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_FIELD_NUMBER: _ClassVar[int]
    EXPIRES_AT_FIELD_NUMBER: _ClassVar[int]
    APP_ID_FIELD_NUMBER: _ClassVar[int]
    name: str
    description: str
    environment: APIKeyEnvironment
    expires_at: _timestamp_pb2.Timestamp
    app_id: str
    def __init__(self, name: _Optional[str] = ..., description: _Optional[str] = ..., environment: _Optional[_Union[APIKeyEnvironment, str]] = ..., expires_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., app_id: _Optional[str] = ...) -> None: ...

class CreateAPIKeyResponse(_message.Message):
    __slots__ = ("api_key", "secret")
    API_KEY_FIELD_NUMBER: _ClassVar[int]
    SECRET_FIELD_NUMBER: _ClassVar[int]
    api_key: APIKey
    secret: str
    def __init__(self, api_key: _Optional[_Union[APIKey, _Mapping]] = ..., secret: _Optional[str] = ...) -> None: ...

class GetAPIKeyRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GetAPIKeyResponse(_message.Message):
    __slots__ = ("api_key",)
    API_KEY_FIELD_NUMBER: _ClassVar[int]
    api_key: APIKey
    def __init__(self, api_key: _Optional[_Union[APIKey, _Mapping]] = ...) -> None: ...

class ListAPIKeysRequest(_message.Message):
    __slots__ = ("environment", "include_revoked", "pagination")
    ENVIRONMENT_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_REVOKED_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    environment: APIKeyEnvironment
    include_revoked: bool
    pagination: _common_pb2.PaginationRequest
    def __init__(self, environment: _Optional[_Union[APIKeyEnvironment, str]] = ..., include_revoked: bool = ..., pagination: _Optional[_Union[_common_pb2.PaginationRequest, _Mapping]] = ...) -> None: ...

class ListAPIKeysResponse(_message.Message):
    __slots__ = ("api_keys", "pagination")
    API_KEYS_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    api_keys: _containers.RepeatedCompositeFieldContainer[APIKey]
    pagination: _common_pb2.PaginationResponse
    def __init__(self, api_keys: _Optional[_Iterable[_Union[APIKey, _Mapping]]] = ..., pagination: _Optional[_Union[_common_pb2.PaginationResponse, _Mapping]] = ...) -> None: ...

class RevokeAPIKeyRequest(_message.Message):
    __slots__ = ("id", "reason")
    ID_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    id: str
    reason: str
    def __init__(self, id: _Optional[str] = ..., reason: _Optional[str] = ...) -> None: ...

class RevokeAPIKeyResponse(_message.Message):
    __slots__ = ("api_key",)
    API_KEY_FIELD_NUMBER: _ClassVar[int]
    api_key: APIKey
    def __init__(self, api_key: _Optional[_Union[APIKey, _Mapping]] = ...) -> None: ...
