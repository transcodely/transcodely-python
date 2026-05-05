from buf.validate import validate_pb2 as _validate_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DRMSystem(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DRM_SYSTEM_UNSPECIFIED: _ClassVar[DRMSystem]
    DRM_SYSTEM_WIDEVINE: _ClassVar[DRMSystem]
    DRM_SYSTEM_FAIRPLAY: _ClassVar[DRMSystem]
    DRM_SYSTEM_PLAYREADY: _ClassVar[DRMSystem]

class EncryptionScheme(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ENCRYPTION_SCHEME_UNSPECIFIED: _ClassVar[EncryptionScheme]
    ENCRYPTION_SCHEME_CENC: _ClassVar[EncryptionScheme]
    ENCRYPTION_SCHEME_CBCS: _ClassVar[EncryptionScheme]
DRM_SYSTEM_UNSPECIFIED: DRMSystem
DRM_SYSTEM_WIDEVINE: DRMSystem
DRM_SYSTEM_FAIRPLAY: DRMSystem
DRM_SYSTEM_PLAYREADY: DRMSystem
ENCRYPTION_SCHEME_UNSPECIFIED: EncryptionScheme
ENCRYPTION_SCHEME_CENC: EncryptionScheme
ENCRYPTION_SCHEME_CBCS: EncryptionScheme

class BYOKConfig(_message.Message):
    __slots__ = ("key_id", "key", "pssh_widevine", "pssh_playready", "fairplay_iv", "fairplay_uri")
    KEY_ID_FIELD_NUMBER: _ClassVar[int]
    KEY_FIELD_NUMBER: _ClassVar[int]
    PSSH_WIDEVINE_FIELD_NUMBER: _ClassVar[int]
    PSSH_PLAYREADY_FIELD_NUMBER: _ClassVar[int]
    FAIRPLAY_IV_FIELD_NUMBER: _ClassVar[int]
    FAIRPLAY_URI_FIELD_NUMBER: _ClassVar[int]
    key_id: str
    key: str
    pssh_widevine: str
    pssh_playready: str
    fairplay_iv: str
    fairplay_uri: str
    def __init__(self, key_id: _Optional[str] = ..., key: _Optional[str] = ..., pssh_widevine: _Optional[str] = ..., pssh_playready: _Optional[str] = ..., fairplay_iv: _Optional[str] = ..., fairplay_uri: _Optional[str] = ...) -> None: ...

class KeyServerConfig(_message.Message):
    __slots__ = ("license_server_url", "auth_token", "content_id")
    LICENSE_SERVER_URL_FIELD_NUMBER: _ClassVar[int]
    AUTH_TOKEN_FIELD_NUMBER: _ClassVar[int]
    CONTENT_ID_FIELD_NUMBER: _ClassVar[int]
    license_server_url: str
    auth_token: str
    content_id: str
    def __init__(self, license_server_url: _Optional[str] = ..., auth_token: _Optional[str] = ..., content_id: _Optional[str] = ...) -> None: ...

class DRMConfig(_message.Message):
    __slots__ = ("systems", "scheme", "byok", "key_server", "clear_lead_seconds")
    SYSTEMS_FIELD_NUMBER: _ClassVar[int]
    SCHEME_FIELD_NUMBER: _ClassVar[int]
    BYOK_FIELD_NUMBER: _ClassVar[int]
    KEY_SERVER_FIELD_NUMBER: _ClassVar[int]
    CLEAR_LEAD_SECONDS_FIELD_NUMBER: _ClassVar[int]
    systems: _containers.RepeatedScalarFieldContainer[DRMSystem]
    scheme: EncryptionScheme
    byok: BYOKConfig
    key_server: KeyServerConfig
    clear_lead_seconds: float
    def __init__(self, systems: _Optional[_Iterable[_Union[DRMSystem, str]]] = ..., scheme: _Optional[_Union[EncryptionScheme, str]] = ..., byok: _Optional[_Union[BYOKConfig, _Mapping]] = ..., key_server: _Optional[_Union[KeyServerConfig, _Mapping]] = ..., clear_lead_seconds: _Optional[float] = ...) -> None: ...
