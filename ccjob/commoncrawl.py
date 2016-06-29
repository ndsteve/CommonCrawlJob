from __future__ import print_function

from mrjob.job import MRJob
from warc import WARCFile
from six.moves.urllib.request import url2pathname
from s3fs import S3FileSystem

import re

__all__ = [
    'CommonCrawl'
]


class CommonCrawl(MRJob):

    @staticmethod
    def split_headers(head):
        return dict([i.split(':', 1) for i in head.splitlines() if ':' in i])

    def get_payload(self, record):
        output = {}
        payload = record.payload.read()
        head, _, tail = payload.partition('\r\n\r\n')
        output.update(self.split_headers(head))

    def configure_options(self):
        super(CommonCrawl, self).configure_options()
        self.add_passthrough_option(
            '--pattern',
            default='[\"\']UA-(\d+)-(\d)+[\'\"]',
            type=str,
            help='pattern',
        )

    def mapper_init(self):
        self.pattern = re.compile(self.options.pattern)
        self.fs = S3FileSystem(anon=True, use_ssl=False)

    def read_warc(self, key):
        keypath = 's3://aws-publicdatasets/{key}'.format(key=key)
        with self.fs.open(keypath, 'rb') as fp:
            warcfile = WARCFile(fileobj=fp, compress='gzip')
            for record in warcfile.reader:
                if record.type == 'response':
                    yield record

    def mapper(self, key, line):
        for record in self.read_warc(line.strip()):
            payload = self.get_payload(record)
            for value in self.process_record(payload.get('tail', '')):
                yield ((url2pathname(record.url), value), 1)

    def process_record(self, body):
        for match in self.pattern.finditer(body):
            if match:
                yield match.groups()[0]
        self.increment_counter('commoncrawl', 'processed_record', 1)

    def reducer(self, url, values):
        yield (url[0], url[1])

