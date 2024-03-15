# Real Time RAG using Kafka pipelines

This project shows how to create a real time kafka pipeline for RAG.

## Project Overview

This project is designed with a producer and consumer setup for real time RAG using kakfa pipelines using Vlite as a numpy vector database.

## How to run

1. ### Install the dependencies

```bash
pip install requirements.txt
```

2. ### Start Zookeeper

```bash
.\bin\windows\zookeeper-server-start.bat .\config\zookeeper.properties
```

3. ### Start Kafka Server

```bash
.\bin\windows\kafka-server-start.bat .\config\server.properties
```

4. ### Create a topic

```bash
.\bin\windows\kafka-topics.bat --create --topic myfirsttopic --bootstrap-server localhost:9092
```

4. ### Start the producer

```bash
python producer.py
```

4. ### Start the consumer

```bash
python consumer.py
```
