from kafka_tfrx.stream import KafkaStream


stream = KafkaStream.avro_consumer('gdax', offset='end')

if __name__ == '__main__':
    for message in stream:
        print(message)


