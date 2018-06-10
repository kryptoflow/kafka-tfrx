from __future__ import division, print_function, absolute_import

import logging
import os
from confluent_kafka import avro, TopicPartition
from confluent_kafka.avro import AvroProducer, AvroConsumer
from confluent_kafka import KafkaError
import confluent_kafka
import uuid
from typing import Iterable


__author__ = "Carlo Mazzaferro"
__copyright__ = "Carlo Mazzaferro"
__license__ = "mit"


_logger = logging.getLogger('root')


class IterateStream(type):

    def __iter__(cls):
        while True:
            msg = cls.consumer.poll()
            if msg is not None:
                if not msg.error():

                    if msg.value() == '':
                        continue
                    else:
                        yield msg.value()

                elif msg.error().code() != KafkaError._PARTITION_EOF:
                    yield msg.error()

    def __next__(self):
        pass


class BaseIterator(metaclass=IterateStream):

    __metaclass__ = IterateStream

    def bind(self, other: Iterable, fn: callable):
        raise NotImplementedError


class KafkaStream(BaseIterator):

    OFFSETS = {'start': confluent_kafka.OFFSET_BEGINNING,
               'end': confluent_kafka.OFFSET_END}

    @classmethod
    def avro_producer(cls, topic='gdax', schemas=None):
        ip = cls.determine_ip()
        return AvroProducer({'bootstrap.servers': ip + ':9092',
                             'schema.registry.url': 'http://' + ip + ':8081'},
                            default_key_schema=cls.schemas(schemas)['keyschema'],
                            default_value_schema=cls.schemas(schemas)[topic])

    @classmethod
    def avro_consumer(cls, topic='gdax', offset='start', group_id=None):
        if not group_id:
            group_id = str(uuid.uuid1()).split('-')[0]
        ip = cls.determine_ip()
        try:
            _offset = cls.OFFSETS[offset]
        except KeyError:
            _offset = offset

        cls.consumer = AvroConsumer(dict({'bootstrap.servers': ip + ':9092',
                                          'schema.registry.url': 'http://' + ip + ':8081'},
                                         **{'group.id': group_id,
                                            'default.topic.config': {'auto.offset.reset': 'beginning',
                                                                     'auto.commit.enable': 'false'}
                                            }))

        cls.consumer.assign([TopicPartition(topic, partition=0, offset=_offset)])

        return cls

    @classmethod
    def schemas(cls, schema_path):
        if not schema_path:
            raise ValueError('Path to schema files must be provided when using avro_producer')
        else:
            return {os.path.basename(topic).split('.avsc')[0]: os.path.join(schema_path, topic) for
                    topic in os.listdir(schema_path)}

    @classmethod
    def determine_ip(cls):
        try:
            return os.environ['KAFKA_SERVER_IP']
        except KeyError:
            return 'localhost'

    def bind(self, other: AvroProducer, fn: callable):
        other.produce()

