kafka-tfrx
==========


[![Build Status](https://travis-ci.org/kryptoflow/kafka-tfrx.svg?branch=master)](https://travis-ci.org/kryptoflow/kafka-tfrx)

Simple, idiomatic python API to interface Kafka topics with [RxPY](https://github.com/ReactiveX/RxPY)

## Description

The goal of this library is mostly to enable reactive access to Kafka topics. It builds on top of Confluent Kafka's 
python [client](https://github.com/confluentinc/confluent-kafka-python), and allows building observable streams from
any Kafka topic.

The main motivation for this library is using it with [online learning](https://en.wikipedia.org/wiki/Online_machine_learning), 
but it is by no means limited to that. In a way, it provides a subset of the functionality that Kafka-Streams offers,
which currently does not have a stable python implementation. 


## Usage

See `examples/`


## Tests

Run `tox` from top level dir

## Note

This project has been set up using PyScaffold 3.0.3. For details and
usage information on PyScaffold see <http://pyscaffold.org/>.
