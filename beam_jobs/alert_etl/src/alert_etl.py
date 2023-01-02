import argparse
import json
import logging
import os
import re

import apache_beam as beam
from apache_beam.io import WriteToText
from apache_beam.io.kinesis import ReadDataFromKinesis
from apache_beam.options.pipeline_options import PipelineOptions, SetupOptions

LOGGER = logging.getLogger()
DEBUG_LEVEL = os.environ.get('DEBUG_LEVEL', 'INFO')
LOGGER.setLevel(DEBUG_LEVEL)

AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')

KINESIS_ARN_REGEX = r'arn:aws:kinesis:(?P<region>[^:]+):(?P<account>[^:]+):stream/(?P<stream_name>[^$]+)$'

# Fix for [wrong URN bug](https://github.com/apache/beam/issues/23693) that will be fixed in apache-beam:2.44.0
ReadDataFromKinesis.URN = 'beam:transform:org.apache.beam:kinesis_read_data:v1'


def read_input(input_source: str):
    if not input_source:
        raise ValueError('No input source provided!')
    if input_source.startswith('arn:aws:kinesis'):
        kinesis_arn_match = re.search(KINESIS_ARN_REGEX, input_source)
        aws_region = kinesis_arn_match.group('region')
        stream_name = kinesis_arn_match.group('stream_name')
        res = ReadDataFromKinesis(
            stream_name,
            aws_access_key=AWS_ACCESS_KEY_ID,
            aws_secret_key=AWS_SECRET_ACCESS_KEY,
            region=aws_region,
            max_num_records=10,
            max_read_time=10000,
            initial_position_in_stream='LATEST'
        )
    else:
        raise ValueError('Input source not supported must be Kinesis ARN or S3 ARN/URL')
    return res


def parse_data(entry):
    decoded_data = json.loads(entry.decode('utf8'))
    json_str = json.dumps(decoded_data)
    print(json_str)
    LOGGER.debug(json_str)
    return json_str


def run(argv=None, save_main_session=True):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--input',
        dest='input',
        required=True
    )
    parser.add_argument(
        '--output',
        dest='output',
        required=True
    )
    parser.add_argument(
        '--start_date',
        dest='start_date',
    )
    parser.add_argument(
        '--end_date',
        dest='end_date',
    )
    known_args, pipeline_args = parser.parse_known_args(argv)

    pipeline_options = PipelineOptions(pipeline_args)
    pipeline_options.view_as(SetupOptions).save_main_session = save_main_session

    with beam.Pipeline(options=pipeline_options) as p:
        data = (p | read_input(known_args.input))
        parsed = (data | beam.Map(parse_data))
        persisted = (parsed | WriteToText(known_args.output))


if __name__ == '__main__':
    run()
