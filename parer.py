"""Main service. Waits for new tasks and executes them"""
import os
import sys
import time
from rq import Queue
from methods.connection import get_redis, await_job


def main():
    """Executes existing tasks and waits for new"""
    # Getting tasks from db
    q = Queue('get_tasks', connection=r)
    job = q.enqueue('get_tasks.get_tasks')
    await_job(job, 5)
    chans_to_parse = job.result
    # parsing channels
    if chans_to_parse != ():
        q = Queue('get_channels', connection=r)
        for chan in chans_to_parse:
            print("+job", chan)
            job = q.enqueue('get_channels.get_channels', chan)
    elif not chans_to_parse:
        print("Retrying to get tasks")
        time.sleep(10)
    else:
        print(chans_to_parse, "Waiting for new tasks")
        time.sleep(60)  # wait for new tasks
    return main()


if __name__ == '__main__':
    r = get_redis()
    time.sleep(10)  # wait till database is fully launched
    main()
