# Debezium Integration with PostgreSQL as Change Data Capture (CDC)
This project demonstrates the integration of Debezium as a Change Data Capture (CDC) tool with PostgreSQL. Debezium captures changes in the database and publishes them to Apache Kafka, allowing real-time consumption of database changes.

## Prerequisites
- Docker
- Docker Compose
- Python 3.x
- Python libraries and packages (`requirements.txt`)

## Setup
1. Start Docker Services:
Run the following command to start PostgreSQL, Zookeeper, Kafka, Debezium, and Schema Registry services:
`docker compose up -d`
2. Configure Debezium Connector:
Edit the `postgresql_connector.py` file to include the correct PostgreSQL service IP address in the connector_config dictionary.

3. Create Debezium Connector:
Run the following command to create the Debezium connector:
`python postgresql_connector.py`
3. Generate and Load Sample Data
Execute the following command to generate and load sample data into the PostgreSQL database:
 `python python_job.py`
4. Check Kafka Topics
Run the following command to check the Kafka topics:
`python kafka_check_topics.py`
5. Consume Changes from Kafka
Run the following command to consume changes from the Kafka topic postgres.public.transactions:
`python kafka_read_topics.py`
6. Cleanup
Run the following command to stop the Docker services:
`docker-compose down`

## Important Notes
- Ensure the postgresql database write-ahead log (WAL) level value is set to `logical`.
- Ensure the required Python libraries are installed. You can install them using:`pip install -r requirements.txt`.
- Adjust the connection parameters in the Python scripts (postgresql_connector.py, python_job.py, kafka_read_topics.py) according to your PostgreSQL and Kafka configurations.
- For more information on Debezium and its configuration options, refer to the [Debezium Documentation](https://debezium.io/documentation/reference/2.5/connectors/postgresql.html).

Feel free to customize the project according to your requirements and explore the real-time change data capture capabilities provided by Debezium.