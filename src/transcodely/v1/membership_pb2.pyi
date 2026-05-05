from buf.validate import validate_pb2 as _validate_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from transcodely.v1 import common_pb2 as _common_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MembershipRole(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    MEMBERSHIP_ROLE_UNSPECIFIED: _ClassVar[MembershipRole]
    MEMBERSHIP_ROLE_OWNER: _ClassVar[MembershipRole]
    MEMBERSHIP_ROLE_ADMIN: _ClassVar[MembershipRole]
    MEMBERSHIP_ROLE_MEMBER: _ClassVar[MembershipRole]
    MEMBERSHIP_ROLE_VIEWER: _ClassVar[MembershipRole]

class MembershipStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    MEMBERSHIP_STATUS_UNSPECIFIED: _ClassVar[MembershipStatus]
    MEMBERSHIP_STATUS_ACTIVE: _ClassVar[MembershipStatus]
    MEMBERSHIP_STATUS_INVITED: _ClassVar[MembershipStatus]
    MEMBERSHIP_STATUS_SUSPENDED: _ClassVar[MembershipStatus]
MEMBERSHIP_ROLE_UNSPECIFIED: MembershipRole
MEMBERSHIP_ROLE_OWNER: MembershipRole
MEMBERSHIP_ROLE_ADMIN: MembershipRole
MEMBERSHIP_ROLE_MEMBER: MembershipRole
MEMBERSHIP_ROLE_VIEWER: MembershipRole
MEMBERSHIP_STATUS_UNSPECIFIED: MembershipStatus
MEMBERSHIP_STATUS_ACTIVE: MembershipStatus
MEMBERSHIP_STATUS_INVITED: MembershipStatus
MEMBERSHIP_STATUS_SUSPENDED: MembershipStatus

class Membership(_message.Message):
    __slots__ = ("id", "user_id", "org_id", "role", "status", "invited_by", "invited_at", "accepted_at", "created_at", "updated_at")
    ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    ORG_ID_FIELD_NUMBER: _ClassVar[int]
    ROLE_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    INVITED_BY_FIELD_NUMBER: _ClassVar[int]
    INVITED_AT_FIELD_NUMBER: _ClassVar[int]
    ACCEPTED_AT_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    id: str
    user_id: str
    org_id: str
    role: MembershipRole
    status: MembershipStatus
    invited_by: str
    invited_at: _timestamp_pb2.Timestamp
    accepted_at: _timestamp_pb2.Timestamp
    created_at: _timestamp_pb2.Timestamp
    updated_at: _timestamp_pb2.Timestamp
    def __init__(self, id: _Optional[str] = ..., user_id: _Optional[str] = ..., org_id: _Optional[str] = ..., role: _Optional[_Union[MembershipRole, str]] = ..., status: _Optional[_Union[MembershipStatus, str]] = ..., invited_by: _Optional[str] = ..., invited_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., accepted_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., updated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class MembershipWithUser(_message.Message):
    __slots__ = ("membership", "user_email", "user_name", "user_is_active")
    MEMBERSHIP_FIELD_NUMBER: _ClassVar[int]
    USER_EMAIL_FIELD_NUMBER: _ClassVar[int]
    USER_NAME_FIELD_NUMBER: _ClassVar[int]
    USER_IS_ACTIVE_FIELD_NUMBER: _ClassVar[int]
    membership: Membership
    user_email: str
    user_name: str
    user_is_active: bool
    def __init__(self, membership: _Optional[_Union[Membership, _Mapping]] = ..., user_email: _Optional[str] = ..., user_name: _Optional[str] = ..., user_is_active: bool = ...) -> None: ...

class ListMembershipsRequest(_message.Message):
    __slots__ = ("status", "pagination")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    status: MembershipStatus
    pagination: _common_pb2.PaginationRequest
    def __init__(self, status: _Optional[_Union[MembershipStatus, str]] = ..., pagination: _Optional[_Union[_common_pb2.PaginationRequest, _Mapping]] = ...) -> None: ...

class ListMembershipsResponse(_message.Message):
    __slots__ = ("memberships", "pagination")
    MEMBERSHIPS_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    memberships: _containers.RepeatedCompositeFieldContainer[MembershipWithUser]
    pagination: _common_pb2.PaginationResponse
    def __init__(self, memberships: _Optional[_Iterable[_Union[MembershipWithUser, _Mapping]]] = ..., pagination: _Optional[_Union[_common_pb2.PaginationResponse, _Mapping]] = ...) -> None: ...

class GetMembershipRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GetMembershipResponse(_message.Message):
    __slots__ = ("membership",)
    MEMBERSHIP_FIELD_NUMBER: _ClassVar[int]
    membership: MembershipWithUser
    def __init__(self, membership: _Optional[_Union[MembershipWithUser, _Mapping]] = ...) -> None: ...

class UpdateMembershipRoleRequest(_message.Message):
    __slots__ = ("id", "role")
    ID_FIELD_NUMBER: _ClassVar[int]
    ROLE_FIELD_NUMBER: _ClassVar[int]
    id: str
    role: MembershipRole
    def __init__(self, id: _Optional[str] = ..., role: _Optional[_Union[MembershipRole, str]] = ...) -> None: ...

class UpdateMembershipRoleResponse(_message.Message):
    __slots__ = ("membership",)
    MEMBERSHIP_FIELD_NUMBER: _ClassVar[int]
    membership: Membership
    def __init__(self, membership: _Optional[_Union[Membership, _Mapping]] = ...) -> None: ...

class RemoveMembershipRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class RemoveMembershipResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
