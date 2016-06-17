from __future__ import print_function

import gzip
import boto

from boto.s3.key import Key
from builtins import ( # noqa
    bytes, str, open, super, range,
    zip, round, input, int, pow, object
)

__all__ = [
    'S3Remote',
]


class S3Remote(object):

    def __init__(self):
        self.seg = '/common-crawl/parse-output/valid_segments.txt'
        self.dataset = boto.connect_s3(
                anon=True).get_bucket('aws-publicdatasets')
        self.buckets = self.get_buckets()
        self.valid_segments, _ = self.get_valid_segments(self.seg)

    def __repr__(self):
        return '<{} "{}">'.format(
            self.__class__.__name__,
            self.dataset.name
        )

    def get_valid_segments(self, s3_path):
        kfile = Key(self.dataset, s3_path)
        try:
            kfile.open_read()
        except IOError:
            raise IOError('S3 %s file not found' % s3_path)
        meta = dict(kfile.resp.getheaders())
        data = [i.strip() for i in kfile.read().splitlines()]
        return data, meta

    def get_buckets(self):
        """
        By default get's the latest crawl prefix.

        Example:
        --------
        Get the latest crawl from 2014:

        .. code:: python

            >>> self.get_crawl(crawl_date='2014')

        :param crawl_date: str
            Crawl Date Prefix: EG. 2015-48

        :return: crawl_prefix
        :rtype: str
        """
        crawl_bucket = self.dataset.list('common-crawl/crawl-data/', '/')
        return [
            key.name.encode('utf-8')
            for key in crawl_bucket if 'CC-MAIN' in key.name
        ]

    def select_crawl(self, crawl_date=''):
        """
        Fuzzy match a common crawl crawl prefix from available s3 buckets.
        Always selects the latest crawl date matched.

        :param crawl_date: str
            Crawl date specifier

        :return: Selected crawl date
        :rtype: str

        """
        return max([i for i in self.buckets if crawl_date in i])

    def get_index(self, prefix):
        """
        :param prefix: str
            Prefix to S3 bucket

        :return: Uncompressed warc index
        :rtype: str
        """
        botokey = Key(self.dataset, prefix + 'warc.paths.gz')
        fp = gzip.GzipFile(fileobj=gzip.io.BytesIO(botokey.read()))
        return [i.strip() for i in fp]

    def print_buckets(self):
        """
        Helper function to print out list of available buckets

        :return: Nothing is returned
        :rtype: None
        """
        print('Crawl Date Codes')
        for bucket in self.buckets:
            print(bucket.split('/')[-2].lstrip('CC-MAIN-'))
