from mrjob.job import MRJob
from warc import WARCFile
from six.moves.urllib.request import url2pathname
from s3fs import S3FileSystem
import re

__all__ = ['CommonCrawl']


class CommonCrawl(MRJob):

    def configure_options(self):
        super(CommonCrawl, self).configure_options()
        self.add_passthrough_option(
            '--pattern',
            default='[\"\']UA-(\d+)-(\d)+[\'\"]',
            type=str,
            help='pattern',
        )

    def mapper_init(self):
        self.pattern = re.compile(self.options.pattern, re.UNICODE)
        self.fs = S3FileSystem(anon=True, use_ssl=False)

    def read_warc(self, key):
        with self.fs.open('/'.join(['aws-publicdatasets', key]), 'rb') as fp:
            warcfile = WARCFile(fileobj=fp, compress='gzip')
            for record in warcfile.reader:
                if record.type == 'response':
                    yield record

    def mapper(self, key, line):
        for record in self.read_warc(line.strip()):
            payload = record.payload.read()
            head, _, tail = payload.partition('\r\n\r\n')
            for value in self.process(tail):
                yield ((url2pathname(record.url), value), 1)

    def process(self, body):
        for match in self.pattern.finditer(body):
            if match:
                yield match.groups()[0]
        self.increment_counter('commoncrawl', 'processed_document', 1)

    def reducer(self, url, values):
        yield (url[0], url[1])


