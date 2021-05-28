"""Main service. Waits for new tasks and executes them"""
import os
import sys
import time
import json
import MySQLdb
import requests
from flask import Flask, request, Response
from redis import Redis
from rq import Worker, Queue, Connection
from api import api

app = Flask(__name__)
app.register_blueprint(api, url_prefix='/api')
@app.route('/')
def hello_world():
    return 'Parer INC-_-_-_-_-_-_'

def get_redis():
    """Returns redis connection"""
    try:
        redis = Redis(host='redis', port=6379)
    except Redis.DoesNotExist as error:
        print(error)
        sys.exit("Error: Faild connecting to redis")
    return redis
def get_cursor():
    """Returns database cursor"""
    try:
        mydb = MySQLdb.connect(
            host="database",
            password=os.environ['MYSQL_ROOT_PASS'],
            database='youpar'
        )
    except MySQLdb.Error as error:
        print(error)
        sys.exit("Error: Failed connecting to database")
    return mydb.cursor()


def main():
    """Executes existing tasks and waits for new"""
    redis, cursor = get_redis(), get_cursor()

if __name__ == '__main__':
    time.sleep(30) # wait till database is fully launched
    main()
