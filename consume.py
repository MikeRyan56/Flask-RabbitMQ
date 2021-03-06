import pika
import json
import config as cfg
import requests

connection = pika.BlockingConnection(pika.ConnectionParameters(host=cfg.RABBIT_HOST,port=cfg.PORT))
channel = connection.channel()

channel.queue_declare(queue=cfg.QUEUE_TOPIC)

print(' [*] Waiting for messages. To exit press CTRL+C')


def callback(ch, method, properties, body):
    print("Method: {}".format(method))
    print("Properties: {}".format(properties))

    data = json.loads(body)
    print("ID: {}".format(data['id']))
    print("Name: {}".format(data['name']))
    print('Description: {}'.format(data['description']))
    print("city: {}".format(data['city']))
    print("company: {}".format(data['company']))
    print("type: {}".format(data['type']))



channel.basic_consume(callback, queue=cfg.QUEUE_TOPIC, no_ack=True)
channel.start_consuming()

