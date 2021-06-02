"""Main service. Waits for new tasks and executes them"""
import os
import sys
import time
from rq import Queue
from methods.connection import get_redis


def await_job(job, t=60):
    """Waits for job to be done"""
    for i in range(t):
        if job.result is None:
            time.sleep(1)
        else:
            pass


def enqueue_video(video):
    """Enqueues video to parse"""
    # SELECT * FROM CHANNELS WHERE ID = CHAN.ID
    q = Queue('get_videos', connection=r)
    job = q.enqueue('get_videos.get_videos', video['id'])
    await_job(job)
    vid_type = "upd" if len(job.result) == 1 else "new"

    q = Queue('parse_video', connection=r)
    job = q.enqueue('parse_video.parse_video')
    await_job(job)
    data = job.result

    if vid_type == "new":
        q = Queue('write_videos', connection=r)
        job = q.enqueue('write_videos.write_videos', [data])
    else:
        # MB ZROBITI CHEREZ DICTIONARY? TYPU JSON
        q = Queue('update_videos', connection=r)
        job = q.enqueue('update_videos.update_videos', [data])


def enqueue_channel(chan):
    """Enqueues channel to parse"""
    q = Queue('get_channels', connection=r)
    job = q.enqueue('get_channels.get_channels',
                    "WHERE", "id", chan[1])
    await_job(job)
    chan_type = "upd" if job.result != () else "new"
    #  not implemented yet
    q = Queue('parse_channel', connection=r)
    job = q.enqueue('parse_channel.parse_channel', chan[1])
    await_job(job)
    videos = job.result['videos']
    data = job.result['data']
    if chan_type == "new":
        q = Queue('write_channels', connection=r)
        job = q.enqueue('write_channels.write_channels', [data])
    else:
        # MB ZROBITI CHEREZ DICTIONARY? TYPU JSON
        q = Queue('update_channels', connection=r)
        job = q.enqueue('update_channels.update_channels', [data])

    for video in videos:
        enqueue_video(video)
    # remove from tasks
    q = Queue('delete_task', connection=r)
    job = q.enqueue('delete_task.delete_task', chan[0])


def main():
    """Executes existing tasks and waits for new"""
    q = Queue('get_tasks', connection=r)
    # Getting tasks from db
    job = q.enqueue('get_tasks.get_tasks')
    for i in range(5):
        if job.result is None:
            time.sleep(1)
        else:
            break
    chans_to_parse = job.result
    # parsing channels
    if chans_to_parse is not None:
        for chan in chans_to_parse:
            enqueue_channel(chan)
    else:
        time.sleep(30)  # wait for new tasks


if __name__ == '__main__':
    r = get_redis()
    time.sleep(10)  # wait till database is fully launched
    main()
