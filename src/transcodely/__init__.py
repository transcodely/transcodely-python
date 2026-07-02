"""Official Python SDK for the Transcodely video transcoding API.

Quick start:

.. code-block:: python

    import os
    from transcodely import Transcodely

    with Transcodely(api_key=os.environ["TRANSCODELY_API_KEY"]) as client:
        job = client.jobs.create(
            input_url="https://example.com/source.mp4",
            outputs=[{
                "type": "hls",
                "video": [
                    {"codec": "h264", "resolution": "1080p"},
                    {"codec": "h264", "resolution": "720p"},
                ],
            }],
        )
        print(job.id)

        for event in client.jobs.watch(job.id):
            print(event.job.status, event.job.progress)

Headline message and enum classes are re-exported here for ergonomics. Every
public proto class is reachable via :mod:`transcodely.types`. Generated
modules also remain available at ``transcodely.v1.{name}_pb2`` for power users.
"""

from .client import Transcodely
from .errors import (
    APIConnectionError,
    APIError,
    AuthenticationError,
    ConflictError,
    FieldViolation,
    InvalidRequestError,
    NotFoundError,
    PermissionError,
    PreconditionError,
    RateLimitError,
    TranscodelyError,
)
from .pagination import Page, PageContents
from .version import API_VERSION, DEFAULT_BASE_URL, SDK_VERSION

# Headline message classes — most callers reach for these. Everything else lives
# in :mod:`transcodely.types`.
from .types import (
    APIKey,
    App,
    AudioTrackConfig,
    AutoABRConfig,
    ContentAwareConfig,
    DASHConfig,
    DRMConfig,
    HDRConfig,
    HLSConfig,
    Job,
    JobOutput,
    JobPriority,
    JobStatus,
    Membership,
    Organization,
    Origin,
    OutputFormat,
    OutputSpec,
    OutputStatus,
    Preset,
    PresetVariant,
    Resolution,
    StreamingConfig,
    SubtitleTrack,
    ThumbnailResult,
    ThumbnailSpec,
    User,
    UserWithOrganizations,
    Video,
    VideoCodec,
    VideoRendition,
    VideoVariant,
    WatchEventType,
    WatchJobResponse,
    WatchVideoResponse,
)

__all__ = [
    "API_VERSION",
    "APIConnectionError",
    "APIError",
    "APIKey",
    "App",
    "AudioTrackConfig",
    "AuthenticationError",
    "AutoABRConfig",
    "ConflictError",
    "ContentAwareConfig",
    "DASHConfig",
    "DEFAULT_BASE_URL",
    "DRMConfig",
    "FieldViolation",
    "HDRConfig",
    "HLSConfig",
    "InvalidRequestError",
    "Job",
    "JobOutput",
    "JobPriority",
    "JobStatus",
    "Membership",
    "NotFoundError",
    "Organization",
    "Origin",
    "OutputFormat",
    "OutputSpec",
    "OutputStatus",
    "Page",
    "PageContents",
    "PermissionError",
    "PreconditionError",
    "Preset",
    "PresetVariant",
    "RateLimitError",
    "Resolution",
    "SDK_VERSION",
    "StreamingConfig",
    "SubtitleTrack",
    "ThumbnailResult",
    "ThumbnailSpec",
    "Transcodely",
    "TranscodelyError",
    "User",
    "UserWithOrganizations",
    "Video",
    "VideoCodec",
    "VideoRendition",
    "VideoVariant",
    "WatchEventType",
    "WatchJobResponse",
    "WatchVideoResponse",
]
