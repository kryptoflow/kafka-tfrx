from kafka_tfrx.stream import KafkaStream

"""
Run python examples/simple_produce.py first to get an output here
Assumes kafka and schema registry are running according to the following
configuration: https://github.com/carlomazzaferro/kryptoflow/blob/master/docker-compose.yml
"""

if __name__ == '__main__':
    cons = KafkaStream.avro_consumer(topic='gdax', ip='127.0.0.1')
    for c in cons:
        print(c)
