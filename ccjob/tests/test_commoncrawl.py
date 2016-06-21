# -*- coding: utf-8 -*-

from unittest import TestCase
from io import BytesIO

from s3fs import S3FileSystem
from ccjob import CommonCrawl

import logging

logger = logging.getLogger(__name__)

class CommonCrawlTest(TestCase):

    def setUp(self):
        self.s3 = S3FileSystem(anon=True, use_ssl=False)
        self.key = '/'.join([
            'common-crawl',
            'crawl-data',
            'CC-MAIN-2016-07',
            'segments',
            '1454702039825.90',
            'warc',
            'CC-MAIN-20160205195359-00348-ip-10-236-182-209.ec2.internal.warc.gz'
        ])
        self.s3_url = 's3://aws-publicdatasets/' + self.key

    def test_key_exists(self):
        self.assertTrue(self.s3.exists(self.s3_url))

    def test_run(self):
        stdin = BytesIO(bytes(self.key))
        mr_job = CommonCrawl(['--no-conf', '-'])
        mr_job.sandbox(stdin=stdin)
        with mr_job.make_runner() as runner:
            runner.run()
            for line in runner.stream_output():
                key, value = mr_job.parse_output_line(line)
                self.assertTrue(value.isdigit())
