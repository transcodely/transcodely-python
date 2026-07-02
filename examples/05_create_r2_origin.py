"""Create a Cloudflare R2 origin and print its ID."""

import os

from transcodely import Transcodely


def main() -> None:
    with Transcodely(api_key=os.environ["TRANSCODELY_API_KEY"]) as client:
        origin = client.origins.create(
            name="My R2 Origin",
            permissions=["read", "write"],
            r2={
                "bucket": os.environ.get("R2_BUCKET", "media"),
                "account_id": os.environ["R2_ACCOUNT_ID"],
                "jurisdiction": "default",  # or "eu", "fedramp"
                "credentials": {
                    "access_key_id": os.environ["R2_ACCESS_KEY_ID"],
                    "secret_access_key": os.environ["R2_SECRET_ACCESS_KEY"],
                },
            },
        )
        print(f"Created {origin.id} for bucket {origin.r2.bucket}")

        # Alternative: an explicit endpoint URL (custom domain bound to the bucket, or
        # a jurisdiction not yet enumerated in R2Jurisdiction). Provide either
        # account_id or endpoint — never both.
        #
        # client.origins.create(
        #     name="My R2 Origin (custom endpoint)",
        #     permissions=["read", "write"],
        #     r2={
        #         "bucket": "media",
        #         "endpoint": "https://media.example.com",
        #         "credentials": {
        #             "access_key_id": os.environ["R2_ACCESS_KEY_ID"],
        #             "secret_access_key": os.environ["R2_SECRET_ACCESS_KEY"],
        #         },
        #     },
        # )


if __name__ == "__main__":
    main()
