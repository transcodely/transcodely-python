"""Watch a job to completion."""

import os
import sys

from transcodely import Transcodely
from transcodely.v1 import job_pb2


def main() -> None:
    if len(sys.argv) < 2:
        print("usage: python 02_watch_job.py <job_id>", file=sys.stderr)
        sys.exit(1)
    job_id = sys.argv[1]
    terminal = {
        job_pb2.JOB_STATUS_COMPLETED,
        job_pb2.JOB_STATUS_FAILED,
        job_pb2.JOB_STATUS_CANCELED,
    }
    with Transcodely(api_key=os.environ["TRANSCODELY_API_KEY"]) as client:
        for event in client.jobs.watch(job_id):
            job = event.job
            print(f"[{job.status}] progress={job.progress}%")
            if job.status in terminal:
                print("terminal:", job_pb2.JobStatus.Name(job.status))
                break


if __name__ == "__main__":
    main()
