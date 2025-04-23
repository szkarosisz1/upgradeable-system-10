import pika, json, datetime, time

while True:
    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host="rabbitmq", credentials=pika.PlainCredentials("user", "pass"))
        )
        break
    except pika.exceptions.AMQPConnectionError:
        print("[Consumer B] Waiting for RabbitMQ...")
        time.sleep(2)

channel = connection.channel()
channel.queue_declare(queue="tasks", durable=True)
channel.queue_declare(queue="finishedTasks", durable=True)
channel.queue_declare(queue="invalidTasks", durable=True)

def callback(ch, method, properties, body):
    msg = json.loads(body)
    version = msg.get("version")
    if version == "V1.0" or version == "V2.0":
        msg["processed_at"] = str(datetime.datetime.now())
        channel.basic_publish(
            exchange="",
            routing_key="finishedTasks",
            body=json.dumps(msg),
            properties=pika.BasicProperties(delivery_mode=2)
        )
        print(f"[Consumer B] Processed: {msg}")
    else:
        channel.basic_publish(
            exchange="",
            routing_key="invalidTasks",
            body=body,
            properties=pika.BasicProperties(delivery_mode=2)
        )
        print(f"[Consumer B] Invalid version: {version} → sent to invalidTasks")

channel.basic_consume(queue="tasks", on_message_callback=callback, auto_ack=True)
print('[Consumer B] Waiting for messages...')
channel.start_consuming()
