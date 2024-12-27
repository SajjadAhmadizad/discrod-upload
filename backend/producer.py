import os
import json
import pika
from dotenv import load_dotenv

load_dotenv()

ROUTING_KEY = 'discord.routing.key'
EXCHANGE = 'message_exchange'
QUEUE_NAME = 'discord_queue'

class MessageProducer:
    def __init__(self):        
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=os.getenv("QUEUE_HOST"), heartbeat=600, blocked_connection_timeout=300)
            )
        self.channel = self.connection.channel()

    def publish(self,method, message:dict, routing_key):
        print(f'Im Sending to RabbitMQ: channel number : {self.channel.channel_number}')
        properties = pika.BasicProperties(method)
        print(self.channel.queue_declare(QUEUE_NAME))
        # self.channel.basic_publish(
        #     exchange=EXCHANGE, routing_key=ROUTING_KEY, body=json.dumps(message), 
        #     properties=properties
        # )

        print(properties)

        self.channel.basic_publish(
            exchange=EXCHANGE, body=json.dumps(message), routing_key=routing_key,
            properties=properties
        )