from buf.validate import validate_pb2 as _validate_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class VideoCodec(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    VIDEO_CODEC_UNSPECIFIED: _ClassVar[VideoCodec]
    VIDEO_CODEC_H264: _ClassVar[VideoCodec]
    VIDEO_CODEC_H265: _ClassVar[VideoCodec]
    VIDEO_CODEC_VP9: _ClassVar[VideoCodec]
    VIDEO_CODEC_AV1: _ClassVar[VideoCodec]

class AudioCodec(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    AUDIO_CODEC_UNSPECIFIED: _ClassVar[AudioCodec]
    AUDIO_CODEC_AAC: _ClassVar[AudioCodec]
    AUDIO_CODEC_OPUS: _ClassVar[AudioCodec]
    AUDIO_CODEC_MP3: _ClassVar[AudioCodec]

class Container(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CONTAINER_UNSPECIFIED: _ClassVar[Container]
    CONTAINER_MP4: _ClassVar[Container]
    CONTAINER_WEBM: _ClassVar[Container]
    CONTAINER_MKV: _ClassVar[Container]
    CONTAINER_TS: _ClassVar[Container]
    CONTAINER_MOV: _ClassVar[Container]

class Resolution(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    RESOLUTION_UNSPECIFIED: _ClassVar[Resolution]
    RESOLUTION_480P: _ClassVar[Resolution]
    RESOLUTION_720P: _ClassVar[Resolution]
    RESOLUTION_1080P: _ClassVar[Resolution]
    RESOLUTION_1440P: _ClassVar[Resolution]
    RESOLUTION_2160P: _ClassVar[Resolution]
    RESOLUTION_4320P: _ClassVar[Resolution]

class QualityTier(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    QUALITY_TIER_UNSPECIFIED: _ClassVar[QualityTier]
    QUALITY_TIER_ECONOMY: _ClassVar[QualityTier]
    QUALITY_TIER_STANDARD: _ClassVar[QualityTier]
    QUALITY_TIER_PREMIUM: _ClassVar[QualityTier]

class OutputFormat(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    OUTPUT_FORMAT_UNSPECIFIED: _ClassVar[OutputFormat]
    OUTPUT_FORMAT_MP4: _ClassVar[OutputFormat]
    OUTPUT_FORMAT_WEBM: _ClassVar[OutputFormat]
    OUTPUT_FORMAT_MKV: _ClassVar[OutputFormat]
    OUTPUT_FORMAT_MOV: _ClassVar[OutputFormat]
    OUTPUT_FORMAT_HLS: _ClassVar[OutputFormat]
    OUTPUT_FORMAT_DASH: _ClassVar[OutputFormat]
    OUTPUT_FORMAT_ADAPTIVE: _ClassVar[OutputFormat]

class ContentType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CONTENT_TYPE_UNSPECIFIED: _ClassVar[ContentType]
    CONTENT_TYPE_FILM: _ClassVar[ContentType]
    CONTENT_TYPE_ANIMATION: _ClassVar[ContentType]
    CONTENT_TYPE_GRAIN: _ClassVar[ContentType]
    CONTENT_TYPE_GAMING: _ClassVar[ContentType]
    CONTENT_TYPE_SPORTS: _ClassVar[ContentType]
    CONTENT_TYPE_STILLIMAGE: _ClassVar[ContentType]

class DeliveryFormat(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DELIVERY_FORMAT_UNSPECIFIED: _ClassVar[DeliveryFormat]
    DELIVERY_FORMAT_PROGRESSIVE: _ClassVar[DeliveryFormat]
    DELIVERY_FORMAT_HLS: _ClassVar[DeliveryFormat]
    DELIVERY_FORMAT_DASH: _ClassVar[DeliveryFormat]
    DELIVERY_FORMAT_CMAF: _ClassVar[DeliveryFormat]

class BitrateMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    BITRATE_MODE_UNSPECIFIED: _ClassVar[BitrateMode]
    BITRATE_MODE_CRF: _ClassVar[BitrateMode]
    BITRATE_MODE_CBR: _ClassVar[BitrateMode]
    BITRATE_MODE_VBR: _ClassVar[BitrateMode]

class BillingStanding(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    BILLING_STANDING_UNSPECIFIED: _ClassVar[BillingStanding]
    BILLING_STANDING_FREE: _ClassVar[BillingStanding]
    BILLING_STANDING_ACTIVE: _ClassVar[BillingStanding]
    BILLING_STANDING_GRACE: _ClassVar[BillingStanding]
    BILLING_STANDING_DELINQUENT: _ClassVar[BillingStanding]

class BillingTreatment(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    BILLING_TREATMENT_UNSPECIFIED: _ClassVar[BillingTreatment]
    BILLING_TREATMENT_NORMAL: _ClassVar[BillingTreatment]
    BILLING_TREATMENT_TRUSTED: _ClassVar[BillingTreatment]
    BILLING_TREATMENT_EXEMPT: _ClassVar[BillingTreatment]

class DunningStage(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DUNNING_STAGE_UNSPECIFIED: _ClassVar[DunningStage]
    DUNNING_STAGE_NONE: _ClassVar[DunningStage]
    DUNNING_STAGE_PAST_DUE: _ClassVar[DunningStage]
    DUNNING_STAGE_WARNED: _ClassVar[DunningStage]
    DUNNING_STAGE_SOFT_LIMITED: _ClassVar[DunningStage]
    DUNNING_STAGE_SUSPENDED: _ClassVar[DunningStage]
    DUNNING_STAGE_DELETION_WARNED: _ClassVar[DunningStage]
    DUNNING_STAGE_WRITTEN_OFF: _ClassVar[DunningStage]
VIDEO_CODEC_UNSPECIFIED: VideoCodec
VIDEO_CODEC_H264: VideoCodec
VIDEO_CODEC_H265: VideoCodec
VIDEO_CODEC_VP9: VideoCodec
VIDEO_CODEC_AV1: VideoCodec
AUDIO_CODEC_UNSPECIFIED: AudioCodec
AUDIO_CODEC_AAC: AudioCodec
AUDIO_CODEC_OPUS: AudioCodec
AUDIO_CODEC_MP3: AudioCodec
CONTAINER_UNSPECIFIED: Container
CONTAINER_MP4: Container
CONTAINER_WEBM: Container
CONTAINER_MKV: Container
CONTAINER_TS: Container
CONTAINER_MOV: Container
RESOLUTION_UNSPECIFIED: Resolution
RESOLUTION_480P: Resolution
RESOLUTION_720P: Resolution
RESOLUTION_1080P: Resolution
RESOLUTION_1440P: Resolution
RESOLUTION_2160P: Resolution
RESOLUTION_4320P: Resolution
QUALITY_TIER_UNSPECIFIED: QualityTier
QUALITY_TIER_ECONOMY: QualityTier
QUALITY_TIER_STANDARD: QualityTier
QUALITY_TIER_PREMIUM: QualityTier
OUTPUT_FORMAT_UNSPECIFIED: OutputFormat
OUTPUT_FORMAT_MP4: OutputFormat
OUTPUT_FORMAT_WEBM: OutputFormat
OUTPUT_FORMAT_MKV: OutputFormat
OUTPUT_FORMAT_MOV: OutputFormat
OUTPUT_FORMAT_HLS: OutputFormat
OUTPUT_FORMAT_DASH: OutputFormat
OUTPUT_FORMAT_ADAPTIVE: OutputFormat
CONTENT_TYPE_UNSPECIFIED: ContentType
CONTENT_TYPE_FILM: ContentType
CONTENT_TYPE_ANIMATION: ContentType
CONTENT_TYPE_GRAIN: ContentType
CONTENT_TYPE_GAMING: ContentType
CONTENT_TYPE_SPORTS: ContentType
CONTENT_TYPE_STILLIMAGE: ContentType
DELIVERY_FORMAT_UNSPECIFIED: DeliveryFormat
DELIVERY_FORMAT_PROGRESSIVE: DeliveryFormat
DELIVERY_FORMAT_HLS: DeliveryFormat
DELIVERY_FORMAT_DASH: DeliveryFormat
DELIVERY_FORMAT_CMAF: DeliveryFormat
BITRATE_MODE_UNSPECIFIED: BitrateMode
BITRATE_MODE_CRF: BitrateMode
BITRATE_MODE_CBR: BitrateMode
BITRATE_MODE_VBR: BitrateMode
BILLING_STANDING_UNSPECIFIED: BillingStanding
BILLING_STANDING_FREE: BillingStanding
BILLING_STANDING_ACTIVE: BillingStanding
BILLING_STANDING_GRACE: BillingStanding
BILLING_STANDING_DELINQUENT: BillingStanding
BILLING_TREATMENT_UNSPECIFIED: BillingTreatment
BILLING_TREATMENT_NORMAL: BillingTreatment
BILLING_TREATMENT_TRUSTED: BillingTreatment
BILLING_TREATMENT_EXEMPT: BillingTreatment
DUNNING_STAGE_UNSPECIFIED: DunningStage
DUNNING_STAGE_NONE: DunningStage
DUNNING_STAGE_PAST_DUE: DunningStage
DUNNING_STAGE_WARNED: DunningStage
DUNNING_STAGE_SOFT_LIMITED: DunningStage
DUNNING_STAGE_SUSPENDED: DunningStage
DUNNING_STAGE_DELETION_WARNED: DunningStage
DUNNING_STAGE_WRITTEN_OFF: DunningStage

class PaginationRequest(_message.Message):
    __slots__ = ("limit", "cursor", "offset")
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    CURSOR_FIELD_NUMBER: _ClassVar[int]
    OFFSET_FIELD_NUMBER: _ClassVar[int]
    limit: int
    cursor: str
    offset: int
    def __init__(self, limit: _Optional[int] = ..., cursor: _Optional[str] = ..., offset: _Optional[int] = ...) -> None: ...

class PaginationResponse(_message.Message):
    __slots__ = ("next_cursor", "total_count")
    NEXT_CURSOR_FIELD_NUMBER: _ClassVar[int]
    TOTAL_COUNT_FIELD_NUMBER: _ClassVar[int]
    next_cursor: str
    total_count: int
    def __init__(self, next_cursor: _Optional[str] = ..., total_count: _Optional[int] = ...) -> None: ...

class ErrorDetails(_message.Message):
    __slots__ = ("code", "message", "field_violations")
    CODE_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    FIELD_VIOLATIONS_FIELD_NUMBER: _ClassVar[int]
    code: str
    message: str
    field_violations: _containers.RepeatedCompositeFieldContainer[FieldViolation]
    def __init__(self, code: _Optional[str] = ..., message: _Optional[str] = ..., field_violations: _Optional[_Iterable[_Union[FieldViolation, _Mapping]]] = ...) -> None: ...

class FieldViolation(_message.Message):
    __slots__ = ("field", "description")
    FIELD_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    field: str
    description: str
    def __init__(self, field: _Optional[str] = ..., description: _Optional[str] = ...) -> None: ...
