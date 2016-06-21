import re
from ccjob import CommonCrawl

class GoogleAnalytics(CommonCrawl):

    def mapper_init(self):
        super(GoogleAnalytics, self).mapper_init()
        self.pattern = re.compile('[\"\']UA-(\d+)-(\d)+[\'\"]', re.UNICODE)


if __name__ == '__main__':
    GoogleAnalytics.run()
