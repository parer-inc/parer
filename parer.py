"""Main service. Waits for new tasks and executes them"""
import time
from rq import Queue
from methods.connection import get_redis, await_job


def main(first=True):
    """Executes existing tasks and waits for new"""
    if first:
        result = False
        for i in range(60):
            q = Queue('get_tables', connection=r)
            main.job = q.enqueue('get_tables.get_tables')
            await_job(main.job, 5)
            result = main.job.result
            if result:
                break
            time.sleep(1)
        j = ""
        for table in result:
            table = table[0]
            if "_tmp" in table:
                q = Queue('delete_tmp_table', connection=r)
                j = q.enqueue(
                    'delete_tmp_table.delete_tmp_table', table)
                await_job(j, 5)
        q = Queue('delete_task', connection=r)
        main.job = q.enqueue('delete_task.delete_task', "ALL")
        await_job(main.job, 5)
        q = Queue('write_tasks', connection=r)
        main.job = q.enqueue('write_tasks.write_tasks', [
                             'UCngjw6cGfzm6bUIDuhGMntg', 'UCXuqSBlHAE6Xw-yeJA0Tunw'])
        await_job(main.job, 5)
    if first or main.job.result is not None:
        q = Queue('get_tasks', connection=r)
        main.job = q.enqueue('get_tasks.get_tasks')
        await_job(main.job, 5)
        chans_to_parse = main.job.result
        # enqueue_channel
        if chans_to_parse != () and chans_to_parse:
            q = Queue('enqueue_channel', connection=r)
            # time.sleep(9999999)
            for chan in chans_to_parse:
                print("+job", chan)
                main.job = q.enqueue('enqueue_channel.enqueue_channel', chan)
                # time.sleep(50000) # for test
            time.sleep(50)
        elif not chans_to_parse:
            print("Retrying to get tasks")
            time.sleep(10)
        else:
            print(chans_to_parse, "Waiting for new tasks")
            time.sleep(60)  # wait for new tasks
    else:
        print("Watiting for jobs to complete")
        time.sleep(10)
    return main(False)


if __name__ == '__main__':
    r = get_redis()
    main()
