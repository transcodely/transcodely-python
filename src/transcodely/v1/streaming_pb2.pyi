from buf.validate import validate_pb2 as _validate_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class HLSSegmentFormat(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    HLS_SEGMENT_FORMAT_UNSPECIFIED: _ClassVar[HLSSegmentFormat]
    HLS_SEGMENT_FORMAT_FMP4: _ClassVar[HLSSegmentFormat]
    HLS_SEGMENT_FORMAT_TS: _ClassVar[HLSSegmentFormat]

class GOPAlignmentMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    GOP_ALIGNMENT_MODE_UNSPECIFIED: _ClassVar[GOPAlignmentMode]
    GOP_ALIGNMENT_MODE_ALIGNED: _ClassVar[GOPAlignmentMode]
    GOP_ALIGNMENT_MODE_FIXED: _ClassVar[GOPAlignmentMode]

class HLSPlaylistType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    HLS_PLAYLIST_TYPE_UNSPECIFIED: _ClassVar[HLSPlaylistType]
    HLS_PLAYLIST_TYPE_VOD: _ClassVar[HLSPlaylistType]
    HLS_PLAYLIST_TYPE_EVENT: _ClassVar[HLSPlaylistType]
HLS_SEGMENT_FORMAT_UNSPECIFIED: HLSSegmentFormat
HLS_SEGMENT_FORMAT_FMP4: HLSSegmentFormat
HLS_SEGMENT_FORMAT_TS: HLSSegmentFormat
GOP_ALIGNMENT_MODE_UNSPECIFIED: GOPAlignmentMode
GOP_ALIGNMENT_MODE_ALIGNED: GOPAlignmentMode
GOP_ALIGNMENT_MODE_FIXED: GOPAlignmentMode
HLS_PLAYLIST_TYPE_UNSPECIFIED: HLSPlaylistType
HLS_PLAYLIST_TYPE_VOD: HLSPlaylistType
HLS_PLAYLIST_TYPE_EVENT: HLSPlaylistType

class StreamingConfig(_message.Message):
    __slots__ = ("segment_duration_seconds", "hls_segment_format", "gop_alignment", "gop_size_seconds", "multi_codec_master", "hls_playlist_type", "hls_master_name", "dash_manifest_name", "hls_variant_pattern")
    SEGMENT_DURATION_SECONDS_FIELD_NUMBER: _ClassVar[int]
    HLS_SEGMENT_FORMAT_FIELD_NUMBER: _ClassVar[int]
    GOP_ALIGNMENT_FIELD_NUMBER: _ClassVar[int]
    GOP_SIZE_SECONDS_FIELD_NUMBER: _ClassVar[int]
    MULTI_CODEC_MASTER_FIELD_NUMBER: _ClassVar[int]
    HLS_PLAYLIST_TYPE_FIELD_NUMBER: _ClassVar[int]
    HLS_MASTER_NAME_FIELD_NUMBER: _ClassVar[int]
    DASH_MANIFEST_NAME_FIELD_NUMBER: _ClassVar[int]
    HLS_VARIANT_PATTERN_FIELD_NUMBER: _ClassVar[int]
    segment_duration_seconds: int
    hls_segment_format: HLSSegmentFormat
    gop_alignment: GOPAlignmentMode
    gop_size_seconds: int
    multi_codec_master: bool
    hls_playlist_type: HLSPlaylistType
    hls_master_name: str
    dash_manifest_name: str
    hls_variant_pattern: str
    def __init__(self, segment_duration_seconds: _Optional[int] = ..., hls_segment_format: _Optional[_Union[HLSSegmentFormat, str]] = ..., gop_alignment: _Optional[_Union[GOPAlignmentMode, str]] = ..., gop_size_seconds: _Optional[int] = ..., multi_codec_master: bool = ..., hls_playlist_type: _Optional[_Union[HLSPlaylistType, str]] = ..., hls_master_name: _Optional[str] = ..., dash_manifest_name: _Optional[str] = ..., hls_variant_pattern: _Optional[str] = ...) -> None: ...
