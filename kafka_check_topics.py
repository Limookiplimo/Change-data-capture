from confluent_kafka.admin import AdminClient

bootstrap_servers = 'docker_kafka_service_ip_address:9092'
conf = {
    'bootstrap.servers': bootstrap_servers,
}
admin_client = AdminClient(conf)
topics = admin_client.list_topics().topics

try:
    print("List of topics:", topics)
except KeyboardInterrupt:
    pass