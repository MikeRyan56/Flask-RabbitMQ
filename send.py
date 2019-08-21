import pika
import json
import config as cfg
import silly
from random import randint, SystemRandom
import datetime

time_start = datetime.datetime.now()
count_id = 0

for x in range(0, 1000):
    # credentials = pika.PlainCredentials(username=cfg.USER, password=cfg.USER)
    # parameters = pika.ConnectionParameters(host=cfg.RABBIT_HOST, port=cfg.PORT, '/', credentials)
    credentials = pika.PlainCredentials(username='guest', password='guest')
    parameters = pika.ConnectionParameters("localhost",32783, '/', credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    channel.queue_declare(queue=cfg.QUEUE_TOPIC)

    count_id += 1
    messType = ["100", "101", "102", "103", "200", "201", "202"]
    sr = SystemRandom()
    srType = sr.choice(messType)
    name = silly.thing()
    city = silly.city()
    company = silly.company()
    description = silly.sentence()
    data = {
        "id": count_id,
        "name": name,
        "city": city,
        "company": company,
        "description": description,
        "type": srType
    }
    message = json.dumps(data)
    channel.basic_publish(exchange='', routing_key=cfg.QUEUE_TOPIC, body=message)
    print(message)
    connection.close()

time_end = datetime.datetime.now()
print(time_end - time_start)