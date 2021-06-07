"""Main service. Waits for new tasks and executes them"""
import os
import sys
import time
from rq import Queue
from methods.connection import get_redis, await_job


def enqueue_video(video):
    """Enqueues video to parse"""
    # SELECT * FROM CHANNELS WHERE ID = CHAN.ID
    q = Queue('get_videos', connection=r)
    job = q.enqueue('get_videos.get_videos', video['id'])
    await_job(job)
    vid_type = "upd" if len(job.result) == 1 else "new"

    q = Queue('parse_video', connection=r)
    job = q.enqueue('parse_video.parse_video', "UCXuqSBlHAE6Xw-yeJA0Tunw")
    await_job(job, 1800)
    data = job.result
    if data is not None:
        if vid_type == "new":
            q = Queue('write_videos', connection=r)
            job = q.enqueue('write_videos.write_videos', [data])
        else:
            q = Queue('update_videos', connection=r)
            job = q.enqueue('update_videos.update_videos', [data])


def enqueue_channel(chan):
    """Enqueues channel to parse"""

    q = Queue('get_channels', connection=r)
    job = q.enqueue('get_channels.get_channels',
                    "WHERE", "id", chan[1])
    await_job(job)
    chan_type = "upd" if job.result != () else "new"

    q = Queue('parse_channel', connection=r, default_timeout=18000)
    job = q.enqueue('parse_channel.parse_channel', chan[1])
    await_job(job, 18000)
    data = job.result
    if data is not None:
        if chan_type == "new":
            q = Queue('write_channels', connection=r)
            job = q.enqueue('write_channels.write_channels', data)
        else:
            # MB ZROBITI CHEREZ DICTIONARY? TYPU JSON
            q = Queue('update_channels', connection=r)
            job = q.enqueue('update_channels.update_channels', data)
    else:
        pass # LOG
    q = Queue('delete_task', connection=r)
    job = q.enqueue('delete_task.delete_task', chan[0])
#    select from agaga
    #for video in videos:
    #    enqueue_video(video)
    # remove from tasks
    q = Queue('delete_tmp_table', connection=r)
    job = q.enqueue('delete_tmp_table.delete_tmp_table', chan[1]+"_tmp")


def main():
    """Executes existing tasks and waits for new"""
    q = Queue('get_tasks', connection=r)
    # Getting tasks from db
    job = q.enqueue('get_tasks.get_tasks')
    await_job(job, 5)
    chans_to_parse = job.result
    # parsing channels
    if chans_to_parse != ():
        for chan in chans_to_parse:
            print("+job", chan)
            enqueue_channel(chan)  # will be implemented as a serivce later
            time.sleep(5)
    else:
        print(chans_to_parse, "Waiting for new tasks")
        time.sleep(60)  # wait for new tasks


if __name__ == '__main__':
    r = get_redis()
    time.sleep(10)  # wait till database is fully launched
    main()
