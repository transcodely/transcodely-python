"""Create an S3-compatible origin (Hetzner Object Storage) and print its ID."""

import os

from transcodely import Transcodely


def main() -> None:
    with Transcodely(api_key=os.environ["TRANSCODELY_API_KEY"]) as client:
        # Any S3-compatible store (Hetzner Object Storage, Wasabi, DigitalOcean
        # Spaces, MinIO, Backblaze B2) uses the "s3" provider plus an explicit
        # endpoint. Transcodely switches to path-style addressing automatically;
        # the region is still required because the AWS SDK uses it to sign
        # requests. For Hetzner the region is the location code (fsn1/nbg1/hel1).
        origin = client.origins.create(
            name="Hetzner Object Storage",
            permissions=["read", "write"],
            s3={
                "bucket": os.environ.get("S3_BUCKET", "media"),
                "region": "fsn1",
                "endpoint": "https://fsn1.your-objectstorage.com",
                "credentials": {
                    "access_key_id": os.environ["S3_ACCESS_KEY_ID"],
                    "secret_access_key": os.environ["S3_SECRET_ACCESS_KEY"],
                },
            },
        )
        print(f"Created {origin.id} for bucket {origin.s3.bucket}")


if __name__ == "__main__":
    main()
