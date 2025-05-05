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
channel.queue_declare(queue="invalidTasks", durable=True)
channel.queue_declare(queue="tasks", durable=True)

def callback(ch, method, properties, body):
    try:
        msg = json.loads(body)
        print(f"[Consumer C] Requeuing message: {msg}")
    except json.JSONDecodeError:
        print(f"[Consumer C] Received non-JSON message: {body}")
    time.sleep(5)
    try:
        channel.basic_publish(
            exchange="",
            routing_key="tasks",
            body=body,
            properties=pika.BasicProperties(delivery_mode=2)
        )
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        print(f"[Consumer C] Failed to requeue message: {e}")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)

channel.basic_consume(queue="invalidTasks", on_message_callback=callback, auto_ack=False)
print('[Consumer C] Waiting for invalid messages...')
channel.start_consuming()