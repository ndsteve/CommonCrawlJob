import re

from ccjob import CommonCrawl

class GoogleAnalytics(CommonCrawl):

    def mapper_init(self):
        super(self.__class__, self).mapper_init()
        self.pattern = re.compile('[\"\']UA-(\d+)-(\d)+[\'\"]')


if __name__ == '__main__':
    GoogleAnalytics.run()
