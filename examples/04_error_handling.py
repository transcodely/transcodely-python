"""Catch typed errors and respond appropriately."""

import os
import time

from transcodely import (
    AuthenticationError,
    InvalidRequestError,
    NotFoundError,
    RateLimitError,
    Transcodely,
    TranscodelyError,
)


def main() -> None:
    with Transcodely(api_key=os.environ["TRANSCODELY_API_KEY"]) as client:
        try:
            client.jobs.get("job_does_not_exist")
        except NotFoundError as err:
            print("Not found, request id:", err.request_id)
        except AuthenticationError:
            print("Auth failed — check TRANSCODELY_API_KEY")
        except InvalidRequestError as err:
            for v in err.errors:
                print(f"{v.field}: {v.description}")
        except RateLimitError as err:
            time.sleep((err.retry_after_ms or 1000) / 1000)
        except TranscodelyError as err:
            print("Transcodely error:", err.code, err)


if __name__ == "__main__":
    main()
