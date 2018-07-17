from kafka_tfrx.stream import KafkaStream

"""
Assumes kafka and schema registry are running according to the following
configuration: https://github.com/carlomazzaferro/kryptoflow/blob/master/docker-compose.yml
"""

if __name__ == '__main__':
    msg = {"price":  100.0,
           "volume_24h": 10000.1,
           "spread": 0,
           "ts": "1235467",
           "side": "buy"}

    p = KafkaStream.avro_producer('gdax', schemas='examples/schemas', ip='127.0.0.1')

    for i in range(100):
        p.produce(topic='gdax', value=msg)
    p.flush()
