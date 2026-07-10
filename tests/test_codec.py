"""Tests for the JSON wire-format codec.

These tests pin the Transcodely wire format: snake_case field names + simplified
lowercase enum values. They are the Python mirror of the TS / Go codec tests
and should produce bit-identical output for matching inputs.
"""

from __future__ import annotations

import json

import pytest

from transcodely._codec.json_codec import (
    camel_to_screaming_snake,
    deserialize,
    enum_prefix,
    expand_enum_value,
    serialize,
    simplify_enum_value,
    transform_enums_in_dict,
)
from transcodely.v1 import common_pb2, job_pb2, origin_pb2


# ---- Helper enum descriptors -------------------------------------------------

JOB_STATUS = job_pb2.JobStatus.DESCRIPTOR
JOB_PRIORITY = job_pb2.JobPriority.DESCRIPTOR
VIDEO_CODEC = common_pb2.VideoCodec.DESCRIPTOR
RESOLUTION = common_pb2.Resolution.DESCRIPTOR
OUTPUT_FORMAT = common_pb2.OutputFormat.DESCRIPTOR
ORIGIN_PROVIDER = origin_pb2.OriginProvider.DESCRIPTOR
R2_JURISDICTION = origin_pb2.R2Jurisdiction.DESCRIPTOR


# ---- camel_to_screaming_snake -----------------------------------------------


class TestCamelToScreamingSnake:
    def test_splits_camelcase(self) -> None:
        assert camel_to_screaming_snake("JobStatus") == "JOB_STATUS"
        assert camel_to_screaming_snake("OutputFormat") == "OUTPUT_FORMAT"

    def test_keeps_acronyms_together_when_followed_by_lowercase(self) -> None:
        assert camel_to_screaming_snake("APIKeyEnvironment") == "API_KEY_ENVIRONMENT"
        assert camel_to_screaming_snake("HTTPCredentials") == "HTTP_CREDENTIALS"

    def test_treats_digit_uppercase_lowercase_as_a_single_token(self) -> None:
        # Pins R2 enum prefix derivation. The digit-letter boundary inserts no
        # underscore; the letter-letter boundary (2J before lowercase 'u') does.
        assert camel_to_screaming_snake("R2Jurisdiction") == "R2_JURISDICTION"


# ---- enum_prefix -------------------------------------------------------------


class TestEnumPrefix:
    def test_derives_prefix_from_simple_enum_name(self) -> None:
        assert enum_prefix(JOB_STATUS) == "JOB_STATUS_"
        assert enum_prefix(VIDEO_CODEC) == "VIDEO_CODEC_"
        assert enum_prefix(OUTPUT_FORMAT) == "OUTPUT_FORMAT_"
        assert enum_prefix(ORIGIN_PROVIDER) == "ORIGIN_PROVIDER_"
        assert enum_prefix(R2_JURISDICTION) == "R2_JURISDICTION_"


# ---- simplify_enum_value -----------------------------------------------------


class TestSimplifyEnumValue:
    def test_strips_prefix_and_lowercases(self) -> None:
        assert simplify_enum_value("JOB_STATUS_PENDING", JOB_STATUS) == "pending"
        assert simplify_enum_value("VIDEO_CODEC_H264", VIDEO_CODEC) == "h264"
        assert simplify_enum_value("RESOLUTION_1080P", RESOLUTION) == "1080p"

    def test_falls_back_to_lowercase_when_prefix_absent(self) -> None:
        assert simplify_enum_value("UNKNOWN", JOB_STATUS) == "unknown"


# ---- expand_enum_value -------------------------------------------------------


class TestExpandEnumValue:
    def test_turns_simplified_form_back_into_canonical(self) -> None:
        assert expand_enum_value("pending", JOB_STATUS) == "JOB_STATUS_PENDING"
        assert expand_enum_value("h264", VIDEO_CODEC) == "VIDEO_CODEC_H264"
        assert expand_enum_value("1080p", RESOLUTION) == "RESOLUTION_1080P"

    def test_returns_input_unchanged_when_already_canonical(self) -> None:
        assert expand_enum_value("JOB_STATUS_PENDING", JOB_STATUS) == "JOB_STATUS_PENDING"

    def test_returns_input_unchanged_when_no_match(self) -> None:
        assert expand_enum_value("totally_unknown", JOB_STATUS) == "totally_unknown"


# ---- transform_enums_in_dict -------------------------------------------------


class TestTransformEnumsInDict:
    def test_simplify_walks_scalar_repeated_and_nested_message_fields(self) -> None:
        obj = {
            "input_url": "https://example.com/in.mp4",
            "priority": "JOB_PRIORITY_PREMIUM",
            "outputs": [
                {
                    "type": "OUTPUT_FORMAT_HLS",
                    "video": [
                        {"codec": "VIDEO_CODEC_H264", "resolution": "RESOLUTION_1080P"},
                        {"codec": "VIDEO_CODEC_AV1", "resolution": "RESOLUTION_2160P"},
                    ],
                }
            ],
        }
        transform_enums_in_dict(obj, job_pb2.CreateJobRequest.DESCRIPTOR, mode="simplify")
        assert obj["priority"] == "premium"
        assert obj["outputs"][0]["type"] == "hls"
        assert obj["outputs"][0]["video"][0]["codec"] == "h264"
        assert obj["outputs"][0]["video"][0]["resolution"] == "1080p"
        assert obj["outputs"][0]["video"][1]["codec"] == "av1"

    def test_expand_performs_inverse_rewrite(self) -> None:
        obj = {"job": {"id": "job_a", "status": "processing", "priority": "premium"}}
        transform_enums_in_dict(obj, job_pb2.GetJobResponse.DESCRIPTOR, mode="expand")
        assert obj["job"]["status"] == "JOB_STATUS_PROCESSING"
        assert obj["job"]["priority"] == "JOB_PRIORITY_PREMIUM"


# ---- serialize ---------------------------------------------------------------


class TestSerialize:
    def test_emits_snake_case_fields(self) -> None:
        req = job_pb2.CreateJobRequest(input_url="https://example.com/in.mp4")
        obj = json.loads(serialize(req).decode())
        assert obj["input_url"] == "https://example.com/in.mp4"
        assert "inputUrl" not in obj

    def test_simplifies_enum_values_throughout_the_message_tree(self) -> None:
        req = job_pb2.CreateJobRequest(
            input_url="https://example.com/in.mp4",
            priority=job_pb2.JOB_PRIORITY_PREMIUM,
            outputs=[
                job_pb2.OutputSpec(
                    type=common_pb2.OUTPUT_FORMAT_HLS,
                    video=[
                        job_pb2.VideoVariant(
                            codec=common_pb2.VIDEO_CODEC_H264,
                            resolution=common_pb2.RESOLUTION_1080P,
                        )
                    ],
                )
            ],
        )
        obj = json.loads(serialize(req).decode())
        assert obj["priority"] == "premium"
        assert obj["outputs"][0]["type"] == "hls"
        assert obj["outputs"][0]["video"][0]["codec"] == "h264"
        assert obj["outputs"][0]["video"][0]["resolution"] == "1080p"


# ---- deserialize -------------------------------------------------------------


class TestDeserialize:
    def test_expands_simplified_enums_into_proto_int_values(self) -> None:
        payload = json.dumps(
            {"job": {"id": "job_a", "status": "processing", "priority": "premium"}}
        ).encode()
        resp = deserialize(payload, job_pb2.GetJobResponse())
        assert resp.job.id == "job_a"
        assert resp.job.status == job_pb2.JOB_STATUS_PROCESSING
        assert resp.job.priority == job_pb2.JOB_PRIORITY_PREMIUM

    def test_accepts_canonical_form_for_backward_compatibility(self) -> None:
        payload = json.dumps({"job": {"id": "job_a", "status": "JOB_STATUS_PROCESSING"}}).encode()
        resp = deserialize(payload, job_pb2.GetJobResponse())
        assert resp.job.status == job_pb2.JOB_STATUS_PROCESSING

    def test_returns_empty_message_for_empty_bytes(self) -> None:
        msg = job_pb2.GetJobResponse()
        out = deserialize(b"", msg)
        assert out is msg
        assert not out.HasField("job")

    def test_ignores_unknown_fields(self) -> None:
        payload = json.dumps({"job": {"id": "job_a"}, "made_up_field": 42}).encode()
        resp = deserialize(payload, job_pb2.GetJobResponse())
        assert resp.job.id == "job_a"


# ---- round-trip --------------------------------------------------------------


class TestRoundTrip:
    def test_preserves_enum_values_and_nested_structure(self) -> None:
        original = job_pb2.CreateJobRequest(
            input_url="https://example.com/in.mp4",
            outputs=[
                job_pb2.OutputSpec(
                    type=common_pb2.OUTPUT_FORMAT_DASH,
                    video=[
                        job_pb2.VideoVariant(
                            codec=common_pb2.VIDEO_CODEC_AV1,
                            resolution=common_pb2.RESOLUTION_2160P,
                        )
                    ],
                )
            ],
        )
        decoded = deserialize(serialize(original), job_pb2.CreateJobRequest())
        assert decoded.input_url == original.input_url
        assert decoded.outputs[0].type == common_pb2.OUTPUT_FORMAT_DASH
        assert decoded.outputs[0].video[0].codec == common_pb2.VIDEO_CODEC_AV1
        assert decoded.outputs[0].video[0].resolution == common_pb2.RESOLUTION_2160P


# ---- Parametrised wire-format vector ----------------------------------------


@pytest.mark.parametrize(
    "value,enum_desc,wire",
    [
        ("JOB_STATUS_PENDING", JOB_STATUS, "pending"),
        ("JOB_STATUS_PROCESSING", JOB_STATUS, "processing"),
        ("JOB_STATUS_COMPLETED", JOB_STATUS, "completed"),
        ("JOB_PRIORITY_STANDARD", JOB_PRIORITY, "standard"),
        ("JOB_PRIORITY_ECONOMY", JOB_PRIORITY, "economy"),
        ("VIDEO_CODEC_H264", VIDEO_CODEC, "h264"),
        ("VIDEO_CODEC_AV1", VIDEO_CODEC, "av1"),
        ("RESOLUTION_1080P", RESOLUTION, "1080p"),
        ("RESOLUTION_2160P", RESOLUTION, "2160p"),
        ("OUTPUT_FORMAT_HLS", OUTPUT_FORMAT, "hls"),
        ("OUTPUT_FORMAT_DASH", OUTPUT_FORMAT, "dash"),
        ("ORIGIN_PROVIDER_GCS", ORIGIN_PROVIDER, "gcs"),
        ("ORIGIN_PROVIDER_S3", ORIGIN_PROVIDER, "s3"),
        ("ORIGIN_PROVIDER_HTTP", ORIGIN_PROVIDER, "http"),
        ("ORIGIN_PROVIDER_R2", ORIGIN_PROVIDER, "r2"),
        ("R2_JURISDICTION_DEFAULT", R2_JURISDICTION, "default"),
        ("R2_JURISDICTION_EU", R2_JURISDICTION, "eu"),
        ("R2_JURISDICTION_FEDRAMP", R2_JURISDICTION, "fedramp"),
    ],
)
def test_canonical_to_simplified_round_trip(value: str, enum_desc, wire: str) -> None:  # type: ignore[no-untyped-def]
    assert simplify_enum_value(value, enum_desc) == wire
    assert expand_enum_value(wire, enum_desc) == value


# ---- R2 origin JSON wire format ---------------------------------------------


class TestR2OriginJsonWireFormat:
    ACCOUNT_ID = "0123456789abcdef0123456789abcdef"

    def _account_id_form(
        self, jurisdiction: origin_pb2.R2Jurisdiction = origin_pb2.R2_JURISDICTION_EU
    ) -> origin_pb2.CreateOriginRequest:
        return origin_pb2.CreateOriginRequest(
            name="my-r2",
            permissions=[origin_pb2.ORIGIN_PERMISSION_READ, origin_pb2.ORIGIN_PERMISSION_WRITE],
            r2=origin_pb2.R2OriginConfig(
                bucket="media",
                account_id=self.ACCOUNT_ID,
                jurisdiction=jurisdiction,
                credentials=origin_pb2.S3Credentials(
                    access_key_id="AKIAEXAMPLE",
                    secret_access_key="shhh",
                ),
            ),
        )

    def _endpoint_form(self) -> origin_pb2.CreateOriginRequest:
        return origin_pb2.CreateOriginRequest(
            name="my-r2-custom",
            permissions=[origin_pb2.ORIGIN_PERMISSION_READ],
            r2=origin_pb2.R2OriginConfig(
                bucket="media",
                endpoint="https://media.example.com",
                credentials=origin_pb2.S3Credentials(
                    access_key_id="AKIAEXAMPLE",
                    secret_access_key="shhh",
                ),
            ),
        )

    def test_serializes_account_id_form_with_snake_case_and_simplified_enums(self) -> None:
        obj = json.loads(serialize(self._account_id_form()).decode())
        assert obj["permissions"] == ["read", "write"]
        r2 = obj["r2"]
        assert r2["bucket"] == "media"
        assert r2["account_id"] == self.ACCOUNT_ID
        assert r2["jurisdiction"] == "eu"
        assert "accountId" not in r2
        creds = r2["credentials"]
        assert creds["access_key_id"] == "AKIAEXAMPLE"
        assert creds["secret_access_key"] == "shhh"
        assert "accessKeyId" not in creds

    def test_serializes_endpoint_form_without_account_id_or_jurisdiction(self) -> None:
        obj = json.loads(serialize(self._endpoint_form()).decode())
        r2 = obj["r2"]
        assert r2["endpoint"] == "https://media.example.com"
        # Unset string scalars are omitted by protojson; unset enums round-trip
        # as the simplified zero-value form (the codec strips the
        # R2_JURISDICTION_ prefix unconditionally).
        assert r2.get("account_id", "") == ""

    def test_round_trips_account_id_form(self) -> None:
        original = self._account_id_form(jurisdiction=origin_pb2.R2_JURISDICTION_FEDRAMP)
        decoded = deserialize(serialize(original), origin_pb2.CreateOriginRequest())
        assert decoded.name == "my-r2"
        assert list(decoded.permissions) == [
            origin_pb2.ORIGIN_PERMISSION_READ,
            origin_pb2.ORIGIN_PERMISSION_WRITE,
        ]
        assert decoded.r2.bucket == "media"
        assert decoded.r2.account_id == self.ACCOUNT_ID
        assert decoded.r2.jurisdiction == origin_pb2.R2_JURISDICTION_FEDRAMP
        assert decoded.r2.credentials.access_key_id == "AKIAEXAMPLE"
        assert decoded.r2.credentials.secret_access_key == "shhh"

    def test_round_trips_endpoint_form_preserving_optional_endpoint(self) -> None:
        decoded = deserialize(serialize(self._endpoint_form()), origin_pb2.CreateOriginRequest())
        assert decoded.r2.endpoint == "https://media.example.com"
        assert decoded.r2.account_id == ""
        assert decoded.r2.jurisdiction == origin_pb2.R2_JURISDICTION_UNSPECIFIED
