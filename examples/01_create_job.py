"""Create a transcoding job and print its ID."""

import os

from transcodely import Transcodely


def main() -> None:
    with Transcodely(api_key=os.environ["TRANSCODELY_API_KEY"]) as client:
        job = client.jobs.create(
            input_url="https://download.samplelib.com/mp4/sample-30s.mp4",
            # Write outputs to Transcodely-managed storage. Drop `managed` and set
            # `output_origin_id="ori_..."` to write to your own configured origin.
            managed=True,
            outputs=[
                {
                    "type": "hls",
                    "video": [
                        {"codec": "h264", "resolution": "1080p"},
                        {"codec": "h264", "resolution": "720p"},
                        {"codec": "h264", "resolution": "480p"},
                    ],
                }
            ],
            metadata={"source": "01_create_job.py"},
        )
        print(f"Created {job.id} in status {job.status}")


if __name__ == "__main__":
    main()
