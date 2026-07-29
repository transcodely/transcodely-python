from buf.validate import validate_pb2 as _validate_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from transcodely.v1 import common_pb2 as _common_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class InvoiceStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    INVOICE_STATUS_UNSPECIFIED: _ClassVar[InvoiceStatus]
    INVOICE_STATUS_DRAFT: _ClassVar[InvoiceStatus]
    INVOICE_STATUS_OPEN: _ClassVar[InvoiceStatus]
    INVOICE_STATUS_PAID: _ClassVar[InvoiceStatus]
    INVOICE_STATUS_VOID: _ClassVar[InvoiceStatus]
    INVOICE_STATUS_UNCOLLECTIBLE: _ClassVar[InvoiceStatus]

class InvoiceLineType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    INVOICE_LINE_TYPE_UNSPECIFIED: _ClassVar[InvoiceLineType]
    INVOICE_LINE_TYPE_USAGE: _ClassVar[InvoiceLineType]
    INVOICE_LINE_TYPE_FEE: _ClassVar[InvoiceLineType]
    INVOICE_LINE_TYPE_MIN_CHARGE: _ClassVar[InvoiceLineType]
    INVOICE_LINE_TYPE_ADJUSTMENT: _ClassVar[InvoiceLineType]
INVOICE_STATUS_UNSPECIFIED: InvoiceStatus
INVOICE_STATUS_DRAFT: InvoiceStatus
INVOICE_STATUS_OPEN: InvoiceStatus
INVOICE_STATUS_PAID: InvoiceStatus
INVOICE_STATUS_VOID: InvoiceStatus
INVOICE_STATUS_UNCOLLECTIBLE: InvoiceStatus
INVOICE_LINE_TYPE_UNSPECIFIED: InvoiceLineType
INVOICE_LINE_TYPE_USAGE: InvoiceLineType
INVOICE_LINE_TYPE_FEE: InvoiceLineType
INVOICE_LINE_TYPE_MIN_CHARGE: InvoiceLineType
INVOICE_LINE_TYPE_ADJUSTMENT: InvoiceLineType

class Invoice(_message.Message):
    __slots__ = ("id", "object", "org_id", "status", "period_start", "period_end", "currency", "subtotal_cents", "total_cents", "provider_invoice_number", "finalized_at", "paid_at", "line_items", "created_at")
    ID_FIELD_NUMBER: _ClassVar[int]
    OBJECT_FIELD_NUMBER: _ClassVar[int]
    ORG_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    PERIOD_START_FIELD_NUMBER: _ClassVar[int]
    PERIOD_END_FIELD_NUMBER: _ClassVar[int]
    CURRENCY_FIELD_NUMBER: _ClassVar[int]
    SUBTOTAL_CENTS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_CENTS_FIELD_NUMBER: _ClassVar[int]
    PROVIDER_INVOICE_NUMBER_FIELD_NUMBER: _ClassVar[int]
    FINALIZED_AT_FIELD_NUMBER: _ClassVar[int]
    PAID_AT_FIELD_NUMBER: _ClassVar[int]
    LINE_ITEMS_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    id: str
    object: str
    org_id: str
    status: InvoiceStatus
    period_start: _timestamp_pb2.Timestamp
    period_end: _timestamp_pb2.Timestamp
    currency: str
    subtotal_cents: int
    total_cents: int
    provider_invoice_number: str
    finalized_at: _timestamp_pb2.Timestamp
    paid_at: _timestamp_pb2.Timestamp
    line_items: _containers.RepeatedCompositeFieldContainer[InvoiceLineItem]
    created_at: _timestamp_pb2.Timestamp
    def __init__(self, id: _Optional[str] = ..., object: _Optional[str] = ..., org_id: _Optional[str] = ..., status: _Optional[_Union[InvoiceStatus, str]] = ..., period_start: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., period_end: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., currency: _Optional[str] = ..., subtotal_cents: _Optional[int] = ..., total_cents: _Optional[int] = ..., provider_invoice_number: _Optional[str] = ..., finalized_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., paid_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., line_items: _Optional[_Iterable[_Union[InvoiceLineItem, _Mapping]]] = ..., created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class InvoiceLineItem(_message.Message):
    __slots__ = ("id", "line_type", "description", "quantity", "unit", "amount_cents", "dimensions")
    class DimensionsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    ID_FIELD_NUMBER: _ClassVar[int]
    LINE_TYPE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    QUANTITY_FIELD_NUMBER: _ClassVar[int]
    UNIT_FIELD_NUMBER: _ClassVar[int]
    AMOUNT_CENTS_FIELD_NUMBER: _ClassVar[int]
    DIMENSIONS_FIELD_NUMBER: _ClassVar[int]
    id: str
    line_type: InvoiceLineType
    description: str
    quantity: float
    unit: str
    amount_cents: int
    dimensions: _containers.ScalarMap[str, str]
    def __init__(self, id: _Optional[str] = ..., line_type: _Optional[_Union[InvoiceLineType, str]] = ..., description: _Optional[str] = ..., quantity: _Optional[float] = ..., unit: _Optional[str] = ..., amount_cents: _Optional[int] = ..., dimensions: _Optional[_Mapping[str, str]] = ...) -> None: ...

class ListInvoicesRequest(_message.Message):
    __slots__ = ("pagination",)
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    pagination: _common_pb2.PaginationRequest
    def __init__(self, pagination: _Optional[_Union[_common_pb2.PaginationRequest, _Mapping]] = ...) -> None: ...

class ListInvoicesResponse(_message.Message):
    __slots__ = ("invoices", "pagination")
    INVOICES_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    invoices: _containers.RepeatedCompositeFieldContainer[Invoice]
    pagination: _common_pb2.PaginationResponse
    def __init__(self, invoices: _Optional[_Iterable[_Union[Invoice, _Mapping]]] = ..., pagination: _Optional[_Union[_common_pb2.PaginationResponse, _Mapping]] = ...) -> None: ...

class GetInvoiceRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GetInvoiceResponse(_message.Message):
    __slots__ = ("invoice",)
    INVOICE_FIELD_NUMBER: _ClassVar[int]
    invoice: Invoice
    def __init__(self, invoice: _Optional[_Union[Invoice, _Mapping]] = ...) -> None: ...

class GetUpcomingInvoiceRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetUpcomingInvoiceResponse(_message.Message):
    __slots__ = ("invoice",)
    INVOICE_FIELD_NUMBER: _ClassVar[int]
    invoice: Invoice
    def __init__(self, invoice: _Optional[_Union[Invoice, _Mapping]] = ...) -> None: ...
