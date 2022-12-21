import argparse

import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions, SetupOptions

def run(argv=None, save_main_session=True):
  parser = argparse.ArgumentParser()
  parser.add_argument(
    '--name',
    default='World',
    dest='name'
  )

  known_args, pipeline_args = parser.parse_known_args(argv)

  pipeline_options = PipelineOptions(pipeline_args)
  pipeline_options.view_as(SetupOptions).save_main_session = save_main_session

  with beam.Pipeline(options=pipeline_options) as p:
    output = (
      p | 'read data' >> beam.Create(['Hello %s' % known_args.name])
        | 'output data' >> beam.Map(print)
    )

if __name__ == '__main__':
  run()
