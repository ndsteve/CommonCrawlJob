from __future__ import print_function

import sys

from argparse import ArgumentParser

from . aws import select_crawl, get_index, print_buckets


def command_line():

    prog = 'crawl_index'
    description = 'Helper tool to run MapReduce jobs over Common Crawl'

    crawl_list = ArgumentParser(add_help=False)
    crawl_list.add_argument(
        '-l', '--list',
        action='store_true',
        help='Enumerate all possible crawl dates',
    )

    # Preparse Date Codes
    crawl, _ = crawl_list.parse_known_args()
    if crawl.list:
        print_buckets()
        exit(0)

    parser = ArgumentParser(
        parents=[crawl_list],
        prog=prog,
        description=description,
    )
    parser.add_argument(
        '-v', '--version',
        action='version',
        version="%s v0.1.0" % prog
    )
    parser.add_argument(
        '-d', '--date',
        nargs='?',
        default='latest',
        help='Specify crawl date',
        metavar='d',
    )
    parser.add_argument(
        '-f', '--file',
        nargs='?',
        metavar='f',
        default=None,
        help='Output to a file'
    )
    return parser.parse_args()


def main():
    args = command_line()
    crawl = select_crawl() if args.date == 'latest' else select_crawl(args.date)
    print(
        get_index(crawl),
        file=(open(args.file, 'wt') if args.file else sys.stdout),
        end='',
    )

if __name__ == '__main__':
    sys.exit(main())
