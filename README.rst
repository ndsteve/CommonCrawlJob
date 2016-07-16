Common Crawl Job Library
========================

.. image:: https://img.shields.io/badge/License-Apache%202.0-blue.svg
   :target: https://opensource.org/licenses/Apache-2.0

.. image:: https://travis-ci.org/qadium-memex/CommonCrawlJob.svg?branch=master
    :target: https://travis-ci.org/qadium-memex/CommonCrawlJob

.. image:: https://badge.fury.io/py/CommonCrawlJob.svg
    :target: https://badge.fury.io/py/CommonCrawlJo

This work is supported by `Qadium Inc`_ as a part of the `DARPA Memex Program`_.

Installation
------------

The easiest way to get started is using pip to install a copy of this library.
This will install the stable latest version hosted on ``PyPI``.

.. code-block:: sh

    $ pip install CommonCrawlJob

Another way is to directly install the code from github to get the bleeding
edge version of the code. If that is the case, you can still use pip by pointing
it to github and specifying the protocol.

.. code-block:: sh

    $ pip install git+https://github.com/qadium-memex/CommonCrawlJob.git

Compatibility
-------------

Unfortunately, this code does not yet compatible with Python 3 and Python/PyPy 2.7
are the only current implementations which are tested against.
Unfortunately the library for encoding ``WARC (Web Archive)`` file formats
will need to undergo a rewrite it is possible to have deterministic IO behavior.

.. _MRJob: https://pythonhosted.org/mrjob/

.. _aws-publicdatasets: https://aws.amazon.com/public-data-sets/


.. _`Qadium Inc`: https://qadium.com
.. _`Darpa Memex Program`: www.darpa.mil/program/memex
