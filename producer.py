from kafka import KafkaProducer
import time
import random

producer = KafkaProducer(bootstrap_servers = 'localhost:9092')

while True:
    query = input("ask your question: ")
    producer.send('myfirsttopic', value = query.encode('utf-8'))
    time.sleep(5)