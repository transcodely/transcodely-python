"""Iterate every job using auto-pagination."""

import os

from transcodely import Transcodely


def main() -> None:
    with Transcodely(api_key=os.environ["TRANSCODELY_API_KEY"]) as client:
        seen = 0
        for job in client.jobs.list(limit=50).auto_paging_iter():
            seen += 1
            print(f"{seen}. {job.id} {job.status}")
            if seen >= 200:
                break
        print(f"\nTotal seen: {seen}")


if __name__ == "__main__":
    main()
