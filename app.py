# from flask import Flask
#
# app = Flask(__name__)
#
#
# @app.route('/')
# def hello_world():
#     return 'Hello World!'
#
#
# if __name__ == '__main__':
#     app.run()
from celery import Celery

app = Celery('tasks', broker='amqp://localhost//')

@app.task
def reverse(string):
    return string[::-1]
