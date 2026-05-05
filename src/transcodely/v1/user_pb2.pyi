from buf.validate import validate_pb2 as _validate_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from transcodely.v1 import common_pb2 as _common_pb2
from transcodely.v1 import membership_pb2 as _membership_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class UserStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    USER_STATUS_UNSPECIFIED: _ClassVar[UserStatus]
    USER_STATUS_ACTIVE: _ClassVar[UserStatus]
    USER_STATUS_SUSPENDED: _ClassVar[UserStatus]
    USER_STATUS_DELETED: _ClassVar[UserStatus]

class UserApprovalStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    USER_APPROVAL_STATUS_UNSPECIFIED: _ClassVar[UserApprovalStatus]
    USER_APPROVAL_STATUS_PENDING: _ClassVar[UserApprovalStatus]
    USER_APPROVAL_STATUS_APPROVED: _ClassVar[UserApprovalStatus]
    USER_APPROVAL_STATUS_REJECTED: _ClassVar[UserApprovalStatus]
USER_STATUS_UNSPECIFIED: UserStatus
USER_STATUS_ACTIVE: UserStatus
USER_STATUS_SUSPENDED: UserStatus
USER_STATUS_DELETED: UserStatus
USER_APPROVAL_STATUS_UNSPECIFIED: UserApprovalStatus
USER_APPROVAL_STATUS_PENDING: UserApprovalStatus
USER_APPROVAL_STATUS_APPROVED: UserApprovalStatus
USER_APPROVAL_STATUS_REJECTED: UserApprovalStatus

class User(_message.Message):
    __slots__ = ("id", "email", "email_verified", "first_name", "last_name", "profile_picture_url", "status", "last_login_at", "created_at", "updated_at", "approval_status", "approval_decided_at", "approval_decided_by_user_id")
    ID_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    EMAIL_VERIFIED_FIELD_NUMBER: _ClassVar[int]
    FIRST_NAME_FIELD_NUMBER: _ClassVar[int]
    LAST_NAME_FIELD_NUMBER: _ClassVar[int]
    PROFILE_PICTURE_URL_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    LAST_LOGIN_AT_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    APPROVAL_STATUS_FIELD_NUMBER: _ClassVar[int]
    APPROVAL_DECIDED_AT_FIELD_NUMBER: _ClassVar[int]
    APPROVAL_DECIDED_BY_USER_ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    email: str
    email_verified: bool
    first_name: str
    last_name: str
    profile_picture_url: str
    status: UserStatus
    last_login_at: _timestamp_pb2.Timestamp
    created_at: _timestamp_pb2.Timestamp
    updated_at: _timestamp_pb2.Timestamp
    approval_status: UserApprovalStatus
    approval_decided_at: _timestamp_pb2.Timestamp
    approval_decided_by_user_id: str
    def __init__(self, id: _Optional[str] = ..., email: _Optional[str] = ..., email_verified: bool = ..., first_name: _Optional[str] = ..., last_name: _Optional[str] = ..., profile_picture_url: _Optional[str] = ..., status: _Optional[_Union[UserStatus, str]] = ..., last_login_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., updated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., approval_status: _Optional[_Union[UserApprovalStatus, str]] = ..., approval_decided_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., approval_decided_by_user_id: _Optional[str] = ...) -> None: ...

class UserWithOrganizations(_message.Message):
    __slots__ = ("user", "organizations")
    USER_FIELD_NUMBER: _ClassVar[int]
    ORGANIZATIONS_FIELD_NUMBER: _ClassVar[int]
    user: User
    organizations: _containers.RepeatedCompositeFieldContainer[UserOrganization]
    def __init__(self, user: _Optional[_Union[User, _Mapping]] = ..., organizations: _Optional[_Iterable[_Union[UserOrganization, _Mapping]]] = ...) -> None: ...

class UserOrganization(_message.Message):
    __slots__ = ("org_id", "org_slug", "org_name", "role", "is_active")
    ORG_ID_FIELD_NUMBER: _ClassVar[int]
    ORG_SLUG_FIELD_NUMBER: _ClassVar[int]
    ORG_NAME_FIELD_NUMBER: _ClassVar[int]
    ROLE_FIELD_NUMBER: _ClassVar[int]
    IS_ACTIVE_FIELD_NUMBER: _ClassVar[int]
    org_id: str
    org_slug: str
    org_name: str
    role: _membership_pb2.MembershipRole
    is_active: bool
    def __init__(self, org_id: _Optional[str] = ..., org_slug: _Optional[str] = ..., org_name: _Optional[str] = ..., role: _Optional[_Union[_membership_pb2.MembershipRole, str]] = ..., is_active: bool = ...) -> None: ...

class GetMeRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetMeResponse(_message.Message):
    __slots__ = ("user",)
    USER_FIELD_NUMBER: _ClassVar[int]
    user: UserWithOrganizations
    def __init__(self, user: _Optional[_Union[UserWithOrganizations, _Mapping]] = ...) -> None: ...

class GetUserRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GetUserResponse(_message.Message):
    __slots__ = ("user",)
    USER_FIELD_NUMBER: _ClassVar[int]
    user: User
    def __init__(self, user: _Optional[_Union[User, _Mapping]] = ...) -> None: ...

class UpdateMeRequest(_message.Message):
    __slots__ = ("first_name", "last_name")
    FIRST_NAME_FIELD_NUMBER: _ClassVar[int]
    LAST_NAME_FIELD_NUMBER: _ClassVar[int]
    first_name: str
    last_name: str
    def __init__(self, first_name: _Optional[str] = ..., last_name: _Optional[str] = ...) -> None: ...

class UpdateMeResponse(_message.Message):
    __slots__ = ("user",)
    USER_FIELD_NUMBER: _ClassVar[int]
    user: User
    def __init__(self, user: _Optional[_Union[User, _Mapping]] = ...) -> None: ...

class ListUsersRequest(_message.Message):
    __slots__ = ("status", "pagination")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    status: UserStatus
    pagination: _common_pb2.PaginationRequest
    def __init__(self, status: _Optional[_Union[UserStatus, str]] = ..., pagination: _Optional[_Union[_common_pb2.PaginationRequest, _Mapping]] = ...) -> None: ...

class ListUsersResponse(_message.Message):
    __slots__ = ("users", "pagination")
    USERS_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    users: _containers.RepeatedCompositeFieldContainer[User]
    pagination: _common_pb2.PaginationResponse
    def __init__(self, users: _Optional[_Iterable[_Union[User, _Mapping]]] = ..., pagination: _Optional[_Union[_common_pb2.PaginationResponse, _Mapping]] = ...) -> None: ...
