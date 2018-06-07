#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import pytest
from kafka_tfrx.stream import KafkaStream
from confluent_kafka.avro import AvroProducer, AvroConsumer
import collections


__author__ = "Carlo Mazzaferro"
__copyright__ = "Carlo Mazzaferro"
__license__ = "mit"


@pytest.fixture
def schema_files_dir():
    return'tests/sample_schemas'


def test_get_schema_files(schema_files_dir):
    fs = KafkaStream.schemas(schema_files_dir)
    assert isinstance(fs, dict)
    for key, val in fs.items():
        assert val.endswith('.avsc')
        assert key in ['twitter', 'keyschema', 'reddit', 'gdax']

    with pytest.raises(ValueError):
        KafkaStream.schemas(None)


def test_setup_avro_producer():
    p = KafkaStream.avro_producer('gdax', schemas='tests/sample_schemas')
    assert isinstance(p, AvroProducer)
    with pytest.raises(ValueError):
        KafkaStream.avro_producer('gdax', schemas=None)


def test_setup_avro_consumer():
    c = KafkaStream.avro_consumer('gdax', offset='start', group_id=None)
    assert isinstance(c, KafkaStream.__class__)
    assert isinstance(c, collections.Iterable)


def test_setup_avro_consumer_end():
    e = KafkaStream.avro_consumer('gdax', offset='end', group_id=None)
    assert isinstance(e, KafkaStream.__class__)
    assert isinstance(e, collections.Iterable)


def test_setup_avro_consumer_int():
    e = KafkaStream.avro_consumer('gdax', offset=10000, group_id=None)
    assert isinstance(e, KafkaStream.__class__)
    assert isinstance(e, collections.Iterable)


