import pika, json, time

while True:
    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host="rabbitmq", credentials=pika.PlainCredentials("user", "pass"))
        )
        break
    except pika.exceptions.AMQPConnectionError:
        print("[Consumer C] Waiting for RabbitMQ...")
        time.sleep(2)

channel = connection.channel()
channel.queue_declare(queue="invalidTasks")
channel.queue_declare(queue="tasks")

def callback(ch, method, properties, body):
    print(f"[Consumer C] Requeuing: {body}")
    time.sleep(5)
    channel.basic_publish(exchange="", routing_key="tasks", body=body)

channel.basic_consume(queue="invalidTasks", on_message_callback=callback, auto_ack=True)
print('[Consumer C] Waiting for invalid messages...')
channel.start_consuming()
