import pika, json, time, os

version = os.getenv("MESSAGE_VERSION", "V1.0")

# Retry connection
while True:
    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host="rabbitmq", credentials=pika.PlainCredentials("user", "pass"))
        )
        break
    except pika.exceptions.AMQPConnectionError:
        print("[Producer] Waiting for RabbitMQ...")
        time.sleep(2)

channel = connection.channel()
channel.queue_declare(queue="tasks")

i = 0
while True:
    message = {"id": i, "version": version}
    channel.basic_publish(exchange="", routing_key="tasks", body=json.dumps(message))
    print(f"[Producer] Sent: {message}")
    i += 1
    time.sleep(2)
