from confluent_kafka import Consumer, KafkaError

bootstrap_servers = 'localhost:29092'
topic = 'postgres.public.transactions'
conf = {
    'bootstrap.servers': bootstrap_servers,
    'group.id': 'trans-group',
    'auto.offset.reset': 'earliest' 
}

consumer = Consumer(conf)
consumer.subscribe([topic])

try:
    while True:
        msg = consumer.poll(1.0)

        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                continue
            else:
                print(msg.error())
                break
        print('Received message: {}'.format(msg.value().decode('utf-8')))

except KeyboardInterrupt:
    pass
finally:
    consumer.close()
