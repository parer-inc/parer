"""Main service. Waits for new tasks and executes them"""
import os
import sys
import time
import json
import requests
from redis import Redis
from rq import Worker, Queue, Connection

def get_redis():
    """Returns redis connection"""
    try:
        redis = Redis(host='redis', port=6379)
    except Redis.DoesNotExist as error:
        print(error)
        sys.exit("Error: Faild connecting to redis")
    return redis

def main():
    """Executes existing tasks and waits for new"""
    r = get_redis()
    q = Queue('get_tasks',connection=r)
    job = q.enqueue('get_tasks.get_tasks')
    for i in range(5):
        if job.result == None:
            time.sleep(1)
        else:
            break
    print(job.result)

if __name__ == '__main__':
    time.sleep(10) # wait till database is fully launched
    main()
