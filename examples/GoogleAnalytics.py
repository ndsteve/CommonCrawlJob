import re
from io import BytesIO

from ccjob import CommonCrawl

class GoogleAnalytics(CommonCrawl):

    def mapper_init(self):
        self.pattern = re.compile('[\"\']UA-(\d+)-(\d)+[\'\"]')


if __name__ == '__main__':
    key = '/'.join([
        'common-crawl',
        'crawl-data',
        'CC-MAIN-2016-07',
        'segments',
        '1454702039825.90',
        'warc',
        'CC-MAIN-20160205195359-00348-ip-10-236-182-209.ec2.internal.warc.gz',
    ])
    stdin = BytesIO(bytes(key))
    mr_job = GoogleAnalytics(args=['--no-conf', '-'])
    output = mr_job.run()

    print(output)
