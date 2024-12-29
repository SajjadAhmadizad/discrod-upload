import os
import json
import pika
import threading
from dotenv import load_dotenv
from discord_manager import send_to_discord

# load_dotenv()

ROUTING_KEY = 'discord.routing.key'
EXCHANGE = 'message_exchange'
QUEUE_NAME = 'discord_queue'

class MessageListener(threading.Thread):
    def __init__(self, function=None, function_parameters=None):
        threading.Thread.__init__(self)

        connection= pika.BlockingConnection(pika.ConnectionParameters(host=os.getenv("QUEUE_HOST")))
        
        self.channel = connection.channel()
        
        self.channel.exchange_declare(exchange=EXCHANGE, exchange_type='direct')

        result = self.channel.queue_declare(queue=QUEUE_NAME, exclusive=True)

        try:
            self.channel.queue_bind(exchange=EXCHANGE, queue=QUEUE_NAME, routing_key=ROUTING_KEY)
            self.channel.basic_consume(queue=QUEUE_NAME, on_message_callback=self.callback)
        except Exception as e:
            print(f"Error in queue listener....\n Error : {str(e)}")

    def callback(self, channel, method, properties, message):
        # print(properties.content_type)
        print(method)
        
        if properties.content_type=="send_to_discord":
            print(message)
            message = json.loads(message)
            send_to_discord(message)
        channel.basic_ack(delivery_tag=method.delivery_tag)

    def run(self):
        print (f'Inside Service:  Created Listener {self.channel}')
        self.channel.start_consuming()

