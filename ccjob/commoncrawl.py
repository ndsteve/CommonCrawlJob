from __future__ import print_function

from mrjob.job import MRJob
from warc import WARCFile
from six.moves.urllib.request import url2pathname
from s3fs import S3FileSystem

import re

from . structures import CaseInsensitiveDict

__all__ = [
    'CommonCrawl'
]

class CommonCrawl(MRJob):
    """
    Baseclass for CommonCrawl MRJob Task.

    Can be inherited from, or used directly by overriding `self.pattern` regular expression
    pattern or through manipulation of the inherited MRJob parent class.

    Usage::

    .. code:: python

        class GoogleAnalytics(CommonCrawl):

            def mapper_init(self):
                super(GoogleAnalytics, self).mapper_init()
                self.pattern = re.compile('[\"\']UA-(\d+)-(\d)+[\'\"]', re.UNICODE)

        if __name__ == '__main__':
            GoogleAnalytics.run()
    """
    fs = S3FileSystem(anon=True)

    def __repr__(self):
        return '<{}: {}>'.format(self.__class__.__name__,self.stdin)

    @staticmethod
    def split_headers(head):
        return CaseInsensitiveDict(
            [
                k.strip() for k in i.split(':', 1)
                ] for i in head.splitlines() if ':' in i
        )

    def get_payload(self, record):
        payload = record.payload.read()
        head, _, tail = payload.partition('\r\n\r\n')
        content_type = self.split_headers(head).get('content-type', '').lower()
        if 'latin-1' or 'iso-8859-1' in content_type:
            tail = tail.decode('latin-1').encode('utf-8')
        try:
            return tail.decode('utf-8')
        except UnicodeDecodeError:
            return unicode()

    def read_warc(self, key):
        keypath = 's3://aws-publicdatasets/{key}'.format(key=key)
        with self.fs.open(keypath, 'rb') as fp:
            warcfile = WARCFile(fileobj=fp, compress='gzip')
            for record in warcfile.reader:
                self.increment_counter('commoncrawl', 'processed_record', 1)
                if record.type == 'response':
                    yield record

    def mapper(self, key, line):
        for record in self.read_warc(line.strip()):
            payload = self.get_payload(record)
            for value in self.process_record(payload):
                yield ((url2pathname(record.url), value), 1)

    def process_record(self, body):
        for match in self.pattern.finditer(body):
            if match:
                yield match.groups()[0]

    def reducer(self, url, values):
        yield (url[0], url[1])

