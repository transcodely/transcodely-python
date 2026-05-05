"""HTTP header helpers — user-agent, idempotency keys, structured client metadata."""

from __future__ import annotations

import json
import platform
import sys
import uuid

from ..version import SDK_VERSION


def user_agent() -> str:
    return f"Transcodely/{SDK_VERSION} python/{sys.version_info.major}.{sys.version_info.minor}"


def client_user_agent_json() -> str:
    return json.dumps(
        {
            "lang": "python",
            "lang_version": platform.python_version(),
            "platform": f"{platform.system()} {platform.release()} {platform.machine()}",
            "publisher": "transcodely",
            "version": SDK_VERSION,
        },
        separators=(",", ":"),
    )


def new_idempotency_key() -> str:
    return str(uuid.uuid4())
