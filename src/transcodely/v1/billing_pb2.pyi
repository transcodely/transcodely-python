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
    INVOICE_LINE_TYPE_HOSTING: _ClassVar[InvoiceLineType]

class TrustTier(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    TRUST_TIER_UNSPECIFIED: _ClassVar[TrustTier]
    TRUST_TIER_NEW: _ClassVar[TrustTier]
    TRUST_TIER_ESTABLISHED: _ClassVar[TrustTier]
    TRUST_TIER_PROVEN: _ClassVar[TrustTier]

class ExposureThresholdSource(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    EXPOSURE_THRESHOLD_SOURCE_UNSPECIFIED: _ClassVar[ExposureThresholdSource]
    EXPOSURE_THRESHOLD_SOURCE_OVERRIDE: _ClassVar[ExposureThresholdSource]
    EXPOSURE_THRESHOLD_SOURCE_TRUST_TIER: _ClassVar[ExposureThresholdSource]
    EXPOSURE_THRESHOLD_SOURCE_ORG_PLAN: _ClassVar[ExposureThresholdSource]
    EXPOSURE_THRESHOLD_SOURCE_PLATFORM_DEFAULT: _ClassVar[ExposureThresholdSource]
    EXPOSURE_THRESHOLD_SOURCE_UNBOUNDED: _ClassVar[ExposureThresholdSource]

class PaymentMethodState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    PAYMENT_METHOD_STATE_UNSPECIFIED: _ClassVar[PaymentMethodState]
    PAYMENT_METHOD_STATE_NONE: _ClassVar[PaymentMethodState]
    PAYMENT_METHOD_STATE_ON_FILE: _ClassVar[PaymentMethodState]
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
INVOICE_LINE_TYPE_HOSTING: InvoiceLineType
TRUST_TIER_UNSPECIFIED: TrustTier
TRUST_TIER_NEW: TrustTier
TRUST_TIER_ESTABLISHED: TrustTier
TRUST_TIER_PROVEN: TrustTier
EXPOSURE_THRESHOLD_SOURCE_UNSPECIFIED: ExposureThresholdSource
EXPOSURE_THRESHOLD_SOURCE_OVERRIDE: ExposureThresholdSource
EXPOSURE_THRESHOLD_SOURCE_TRUST_TIER: ExposureThresholdSource
EXPOSURE_THRESHOLD_SOURCE_ORG_PLAN: ExposureThresholdSource
EXPOSURE_THRESHOLD_SOURCE_PLATFORM_DEFAULT: ExposureThresholdSource
EXPOSURE_THRESHOLD_SOURCE_UNBOUNDED: ExposureThresholdSource
PAYMENT_METHOD_STATE_UNSPECIFIED: PaymentMethodState
PAYMENT_METHOD_STATE_NONE: PaymentMethodState
PAYMENT_METHOD_STATE_ON_FILE: PaymentMethodState

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

class BillingProfile(_message.Message):
    __slots__ = ("object", "org_id", "payment_method_state", "payment_methods", "billing_email", "standing", "grace_until", "standing_reason", "payment_method_required")
    OBJECT_FIELD_NUMBER: _ClassVar[int]
    ORG_ID_FIELD_NUMBER: _ClassVar[int]
    PAYMENT_METHOD_STATE_FIELD_NUMBER: _ClassVar[int]
    PAYMENT_METHODS_FIELD_NUMBER: _ClassVar[int]
    BILLING_EMAIL_FIELD_NUMBER: _ClassVar[int]
    STANDING_FIELD_NUMBER: _ClassVar[int]
    GRACE_UNTIL_FIELD_NUMBER: _ClassVar[int]
    STANDING_REASON_FIELD_NUMBER: _ClassVar[int]
    PAYMENT_METHOD_REQUIRED_FIELD_NUMBER: _ClassVar[int]
    object: str
    org_id: str
    payment_method_state: PaymentMethodState
    payment_methods: _containers.RepeatedCompositeFieldContainer[BillingPaymentMethod]
    billing_email: str
    standing: _common_pb2.BillingStanding
    grace_until: _timestamp_pb2.Timestamp
    standing_reason: str
    payment_method_required: bool
    def __init__(self, object: _Optional[str] = ..., org_id: _Optional[str] = ..., payment_method_state: _Optional[_Union[PaymentMethodState, str]] = ..., payment_methods: _Optional[_Iterable[_Union[BillingPaymentMethod, _Mapping]]] = ..., billing_email: _Optional[str] = ..., standing: _Optional[_Union[_common_pb2.BillingStanding, str]] = ..., grace_until: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., standing_reason: _Optional[str] = ..., payment_method_required: bool = ...) -> None: ...

class BillingPaymentMethod(_message.Message):
    __slots__ = ("id", "type", "brand", "last4", "exp_month", "exp_year", "is_default")
    ID_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    BRAND_FIELD_NUMBER: _ClassVar[int]
    LAST4_FIELD_NUMBER: _ClassVar[int]
    EXP_MONTH_FIELD_NUMBER: _ClassVar[int]
    EXP_YEAR_FIELD_NUMBER: _ClassVar[int]
    IS_DEFAULT_FIELD_NUMBER: _ClassVar[int]
    id: str
    type: str
    brand: str
    last4: str
    exp_month: int
    exp_year: int
    is_default: bool
    def __init__(self, id: _Optional[str] = ..., type: _Optional[str] = ..., brand: _Optional[str] = ..., last4: _Optional[str] = ..., exp_month: _Optional[int] = ..., exp_year: _Optional[int] = ..., is_default: bool = ...) -> None: ...

class BillingPortalSession(_message.Message):
    __slots__ = ("object", "url", "expires_at", "session_token")
    OBJECT_FIELD_NUMBER: _ClassVar[int]
    URL_FIELD_NUMBER: _ClassVar[int]
    EXPIRES_AT_FIELD_NUMBER: _ClassVar[int]
    SESSION_TOKEN_FIELD_NUMBER: _ClassVar[int]
    object: str
    url: str
    expires_at: _timestamp_pb2.Timestamp
    session_token: str
    def __init__(self, object: _Optional[str] = ..., url: _Optional[str] = ..., expires_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., session_token: _Optional[str] = ...) -> None: ...

class Budget(_message.Message):
    __slots__ = ("object", "org_id", "amount_eur", "spent_eur", "used_percent", "period_start", "period_end", "alert_steps", "notified_steps", "currency")
    OBJECT_FIELD_NUMBER: _ClassVar[int]
    ORG_ID_FIELD_NUMBER: _ClassVar[int]
    AMOUNT_EUR_FIELD_NUMBER: _ClassVar[int]
    SPENT_EUR_FIELD_NUMBER: _ClassVar[int]
    USED_PERCENT_FIELD_NUMBER: _ClassVar[int]
    PERIOD_START_FIELD_NUMBER: _ClassVar[int]
    PERIOD_END_FIELD_NUMBER: _ClassVar[int]
    ALERT_STEPS_FIELD_NUMBER: _ClassVar[int]
    NOTIFIED_STEPS_FIELD_NUMBER: _ClassVar[int]
    CURRENCY_FIELD_NUMBER: _ClassVar[int]
    object: str
    org_id: str
    amount_eur: float
    spent_eur: float
    used_percent: float
    period_start: _timestamp_pb2.Timestamp
    period_end: _timestamp_pb2.Timestamp
    alert_steps: _containers.RepeatedScalarFieldContainer[int]
    notified_steps: _containers.RepeatedScalarFieldContainer[int]
    currency: str
    def __init__(self, object: _Optional[str] = ..., org_id: _Optional[str] = ..., amount_eur: _Optional[float] = ..., spent_eur: _Optional[float] = ..., used_percent: _Optional[float] = ..., period_start: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., period_end: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., alert_steps: _Optional[_Iterable[int]] = ..., notified_steps: _Optional[_Iterable[int]] = ..., currency: _Optional[str] = ...) -> None: ...

class OutstandingBalance(_message.Message):
    __slots__ = ("object", "org_id", "outstanding_cents", "tier", "settled_payments", "threshold_cents", "threshold_source", "hard_stop_cents", "blocked", "used_percent", "alert_steps", "notified_steps", "currency", "settlement_available")
    OBJECT_FIELD_NUMBER: _ClassVar[int]
    ORG_ID_FIELD_NUMBER: _ClassVar[int]
    OUTSTANDING_CENTS_FIELD_NUMBER: _ClassVar[int]
    TIER_FIELD_NUMBER: _ClassVar[int]
    SETTLED_PAYMENTS_FIELD_NUMBER: _ClassVar[int]
    THRESHOLD_CENTS_FIELD_NUMBER: _ClassVar[int]
    THRESHOLD_SOURCE_FIELD_NUMBER: _ClassVar[int]
    HARD_STOP_CENTS_FIELD_NUMBER: _ClassVar[int]
    BLOCKED_FIELD_NUMBER: _ClassVar[int]
    USED_PERCENT_FIELD_NUMBER: _ClassVar[int]
    ALERT_STEPS_FIELD_NUMBER: _ClassVar[int]
    NOTIFIED_STEPS_FIELD_NUMBER: _ClassVar[int]
    CURRENCY_FIELD_NUMBER: _ClassVar[int]
    SETTLEMENT_AVAILABLE_FIELD_NUMBER: _ClassVar[int]
    object: str
    org_id: str
    outstanding_cents: int
    tier: TrustTier
    settled_payments: int
    threshold_cents: int
    threshold_source: ExposureThresholdSource
    hard_stop_cents: int
    blocked: bool
    used_percent: float
    alert_steps: _containers.RepeatedScalarFieldContainer[int]
    notified_steps: _containers.RepeatedScalarFieldContainer[int]
    currency: str
    settlement_available: bool
    def __init__(self, object: _Optional[str] = ..., org_id: _Optional[str] = ..., outstanding_cents: _Optional[int] = ..., tier: _Optional[_Union[TrustTier, str]] = ..., settled_payments: _Optional[int] = ..., threshold_cents: _Optional[int] = ..., threshold_source: _Optional[_Union[ExposureThresholdSource, str]] = ..., hard_stop_cents: _Optional[int] = ..., blocked: bool = ..., used_percent: _Optional[float] = ..., alert_steps: _Optional[_Iterable[int]] = ..., notified_steps: _Optional[_Iterable[int]] = ..., currency: _Optional[str] = ..., settlement_available: bool = ...) -> None: ...

class Settlement(_message.Message):
    __slots__ = ("object", "invoice_id", "amount_cents", "period_start", "period_end", "currency")
    OBJECT_FIELD_NUMBER: _ClassVar[int]
    INVOICE_ID_FIELD_NUMBER: _ClassVar[int]
    AMOUNT_CENTS_FIELD_NUMBER: _ClassVar[int]
    PERIOD_START_FIELD_NUMBER: _ClassVar[int]
    PERIOD_END_FIELD_NUMBER: _ClassVar[int]
    CURRENCY_FIELD_NUMBER: _ClassVar[int]
    object: str
    invoice_id: str
    amount_cents: int
    period_start: _timestamp_pb2.Timestamp
    period_end: _timestamp_pb2.Timestamp
    currency: str
    def __init__(self, object: _Optional[str] = ..., invoice_id: _Optional[str] = ..., amount_cents: _Optional[int] = ..., period_start: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., period_end: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., currency: _Optional[str] = ...) -> None: ...

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

class GetBillingProfileRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetBillingProfileResponse(_message.Message):
    __slots__ = ("profile",)
    PROFILE_FIELD_NUMBER: _ClassVar[int]
    profile: BillingProfile
    def __init__(self, profile: _Optional[_Union[BillingProfile, _Mapping]] = ...) -> None: ...

class CreateBillingPortalSessionRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CreateBillingPortalSessionResponse(_message.Message):
    __slots__ = ("session",)
    SESSION_FIELD_NUMBER: _ClassVar[int]
    session: BillingPortalSession
    def __init__(self, session: _Optional[_Union[BillingPortalSession, _Mapping]] = ...) -> None: ...

class GetBudgetRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetBudgetResponse(_message.Message):
    __slots__ = ("budget",)
    BUDGET_FIELD_NUMBER: _ClassVar[int]
    budget: Budget
    def __init__(self, budget: _Optional[_Union[Budget, _Mapping]] = ...) -> None: ...

class UpdateBudgetRequest(_message.Message):
    __slots__ = ("amount_eur",)
    AMOUNT_EUR_FIELD_NUMBER: _ClassVar[int]
    amount_eur: float
    def __init__(self, amount_eur: _Optional[float] = ...) -> None: ...

class UpdateBudgetResponse(_message.Message):
    __slots__ = ("budget",)
    BUDGET_FIELD_NUMBER: _ClassVar[int]
    budget: Budget
    def __init__(self, budget: _Optional[_Union[Budget, _Mapping]] = ...) -> None: ...

class GetOutstandingBalanceRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetOutstandingBalanceResponse(_message.Message):
    __slots__ = ("balance",)
    BALANCE_FIELD_NUMBER: _ClassVar[int]
    balance: OutstandingBalance
    def __init__(self, balance: _Optional[_Union[OutstandingBalance, _Mapping]] = ...) -> None: ...

class SettleOutstandingBalanceRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class SettleOutstandingBalanceResponse(_message.Message):
    __slots__ = ("settlement", "balance")
    SETTLEMENT_FIELD_NUMBER: _ClassVar[int]
    BALANCE_FIELD_NUMBER: _ClassVar[int]
    settlement: Settlement
    balance: OutstandingBalance
    def __init__(self, settlement: _Optional[_Union[Settlement, _Mapping]] = ..., balance: _Optional[_Union[OutstandingBalance, _Mapping]] = ...) -> None: ...
