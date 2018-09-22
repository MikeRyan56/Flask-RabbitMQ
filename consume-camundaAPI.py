import pika
import json
import config as cfg
import requests

connection = pika.BlockingConnection(pika.ConnectionParameters(host=cfg.RABBIT_HOST))
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

    id = data['id']
    name = data['name']
    city = data['city']
    company = data['company']
    description = data['description']
    type = data['type']


    url= 'http://localhost:8080/rest/engine/default/process-definition/key/messageStartEvent/start'
    # number = 1234
    payload = {"variables":
        {
            "requestor": {"value": "admin", "type": "String"},
            "name": {"value": name, "type": "String"},
            "city": {"value": city, "type": "String"},
            "company": {"value": company, "type": "String"},
            "description": {"value": description, "type": "String"},
            "type": {"value": type, "type": "String"},
        },
        "businessKey": id
    }
    # headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    r = requests.post(url, json=payload)  # , headers=headers)
    print(r.status_code)


channel.basic_consume(callback, queue=cfg.QUEUE_TOPIC, no_ack=True)
channel.start_consuming()

