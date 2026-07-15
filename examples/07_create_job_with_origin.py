"""Create a transcoding job against explicit origins (non-managed apps).

Apps without a server-side managed default origin must supply
``output_origin_id`` (and, if the input isn't a bare URL, ``input_origin_id`` +
``input_path``) — the API rejects ``create()`` calls that omit both
``output_origin_id`` and ``managed=True``.
"""

import os

from transcodely import Transcodely


def main() -> None:
    with Transcodely(api_key=os.environ["TRANSCODELY_API_KEY"]) as client:
        job = client.jobs.create(
            input_origin_id=os.environ["INPUT_ORIGIN_ID"],
            input_path="source-videos/sample-30s.mp4",
            output_origin_id=os.environ["OUTPUT_ORIGIN_ID"],
            output_path_template="{job_id}/{output_id}.{ext}",
            outputs=[
                {
                    "type": "hls",
                    "video": [
                        {"codec": "h264", "resolution": "1080p"},
                        {"codec": "h264", "resolution": "720p"},
                    ],
                }
            ],
        )
        print(f"Created {job.id} in status {job.status}")


if __name__ == "__main__":
    main()
