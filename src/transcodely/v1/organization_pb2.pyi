from buf.validate import validate_pb2 as _validate_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from transcodely.v1 import common_pb2 as _common_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class OrganizationStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ORGANIZATION_STATUS_UNSPECIFIED: _ClassVar[OrganizationStatus]
    ORGANIZATION_STATUS_ACTIVE: _ClassVar[OrganizationStatus]
    ORGANIZATION_STATUS_SUSPENDED: _ClassVar[OrganizationStatus]
    ORGANIZATION_STATUS_DELETED: _ClassVar[OrganizationStatus]
ORGANIZATION_STATUS_UNSPECIFIED: OrganizationStatus
ORGANIZATION_STATUS_ACTIVE: OrganizationStatus
ORGANIZATION_STATUS_SUSPENDED: OrganizationStatus
ORGANIZATION_STATUS_DELETED: OrganizationStatus

class Organization(_message.Message):
    __slots__ = ("id", "slug", "display_name", "billing_email", "currency", "status", "created_at", "updated_at")
    ID_FIELD_NUMBER: _ClassVar[int]
    SLUG_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    BILLING_EMAIL_FIELD_NUMBER: _ClassVar[int]
    CURRENCY_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    id: str
    slug: str
    display_name: str
    billing_email: str
    currency: str
    status: OrganizationStatus
    created_at: _timestamp_pb2.Timestamp
    updated_at: _timestamp_pb2.Timestamp
    def __init__(self, id: _Optional[str] = ..., slug: _Optional[str] = ..., display_name: _Optional[str] = ..., billing_email: _Optional[str] = ..., currency: _Optional[str] = ..., status: _Optional[_Union[OrganizationStatus, str]] = ..., created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., updated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class CheckSlugRequest(_message.Message):
    __slots__ = ("slug",)
    SLUG_FIELD_NUMBER: _ClassVar[int]
    slug: str
    def __init__(self, slug: _Optional[str] = ...) -> None: ...

class CheckSlugResponse(_message.Message):
    __slots__ = ("available", "normalized_slug", "reason", "message")
    AVAILABLE_FIELD_NUMBER: _ClassVar[int]
    NORMALIZED_SLUG_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    available: bool
    normalized_slug: str
    reason: str
    message: str
    def __init__(self, available: bool = ..., normalized_slug: _Optional[str] = ..., reason: _Optional[str] = ..., message: _Optional[str] = ...) -> None: ...

class CreateOrganizationRequest(_message.Message):
    __slots__ = ("slug", "display_name", "billing_email", "currency")
    SLUG_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    BILLING_EMAIL_FIELD_NUMBER: _ClassVar[int]
    CURRENCY_FIELD_NUMBER: _ClassVar[int]
    slug: str
    display_name: str
    billing_email: str
    currency: str
    def __init__(self, slug: _Optional[str] = ..., display_name: _Optional[str] = ..., billing_email: _Optional[str] = ..., currency: _Optional[str] = ...) -> None: ...

class CreateOrganizationResponse(_message.Message):
    __slots__ = ("organization",)
    ORGANIZATION_FIELD_NUMBER: _ClassVar[int]
    organization: Organization
    def __init__(self, organization: _Optional[_Union[Organization, _Mapping]] = ...) -> None: ...

class GetOrganizationRequest(_message.Message):
    __slots__ = ("id_or_slug",)
    ID_OR_SLUG_FIELD_NUMBER: _ClassVar[int]
    id_or_slug: str
    def __init__(self, id_or_slug: _Optional[str] = ...) -> None: ...

class GetOrganizationResponse(_message.Message):
    __slots__ = ("organization",)
    ORGANIZATION_FIELD_NUMBER: _ClassVar[int]
    organization: Organization
    def __init__(self, organization: _Optional[_Union[Organization, _Mapping]] = ...) -> None: ...

class UpdateOrganizationRequest(_message.Message):
    __slots__ = ("id", "display_name", "billing_email")
    ID_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    BILLING_EMAIL_FIELD_NUMBER: _ClassVar[int]
    id: str
    display_name: str
    billing_email: str
    def __init__(self, id: _Optional[str] = ..., display_name: _Optional[str] = ..., billing_email: _Optional[str] = ...) -> None: ...

class UpdateOrganizationResponse(_message.Message):
    __slots__ = ("organization",)
    ORGANIZATION_FIELD_NUMBER: _ClassVar[int]
    organization: Organization
    def __init__(self, organization: _Optional[_Union[Organization, _Mapping]] = ...) -> None: ...

class ListOrganizationsRequest(_message.Message):
    __slots__ = ("pagination", "include_inactive")
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_INACTIVE_FIELD_NUMBER: _ClassVar[int]
    pagination: _common_pb2.PaginationRequest
    include_inactive: bool
    def __init__(self, pagination: _Optional[_Union[_common_pb2.PaginationRequest, _Mapping]] = ..., include_inactive: bool = ...) -> None: ...

class ListOrganizationsResponse(_message.Message):
    __slots__ = ("organizations", "pagination")
    ORGANIZATIONS_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    organizations: _containers.RepeatedCompositeFieldContainer[Organization]
    pagination: _common_pb2.PaginationResponse
    def __init__(self, organizations: _Optional[_Iterable[_Union[Organization, _Mapping]]] = ..., pagination: _Optional[_Union[_common_pb2.PaginationResponse, _Mapping]] = ...) -> None: ...
