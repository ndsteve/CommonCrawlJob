Common Crawl Data Extraction
============================

.. image:: https://img.shields.io/badge/License-Apache%202.0-blue.svg
   :target: https://opensource.org/licenses/Apache-2.0

.. image:: https://travis-ci.org/qadium-memex/CommonCrawlJob.svg?branch=master
    :target: https://travis-ci.org/qadium-memex/CommonCrawlJob

.. image:: https://badge.fury.io/py/CommonCrawlJob.svg
    :target: https://badge.fury.io/py/CommonCrawlJo



Extract data from common crawl using elastic map reduce

    Note: This project uses Python 2.7.11

CommonCrawlJob is a framework which wraps the ``MRJob`` hadoop library for streaming
analytics over internet scale data.

For more information on using `MRJob`_ framework.

Setup
-----

To develop locally, you will need to install the ``mrjob`` Hadoop
streaming framework library, and the ``boto`` library for accessing amazon cloud
public dataset resources.

Use pip to install these libraries.

.. code:: sh

    $ pip install CommonCrawlJob

Getting Started
---------------

To first get started, we are going to create a Google Analytics extractor. We will go from start to
finish in creating a Common Crawl extractor that uses regular expression capture groups to extract
google analytics tracker id's.

First let's create a file ``GoogleAnalytics.py``.

.. code:: sh

   $ touch GoogleAnalytics.py

Using a text editor, write to this file

.. code:: python

    import re
    from ccjob import CommonCrawl

    class GoogleAnalytics(CommonCrawl):

        def mapper_init(self):
            super(GoogleAnalytics, self).mapper_init()
            self.pattern = re.compile('[\"\']UA-(\d+)-(\d)+[\'\"]', re.UNICODE)


    if __name__ == '__main__':
        GoogleAnalytics.run()

Our ``GoogleAnalytics`` class has is overriding one method ``mapper_init`` which defines a compiled regular expressions
that will be matched over the HTML content.

All common crawl jobs will generally obey this pattern.

Testing Locally
---------------

Run the Google Analytics extractor locally to test your script.

.. code:: sh

    $ python GoogleAnalytics.py -r local <(tail -n 1 data/latest.txt)


Region Configuration
--------------------

For best performance, you should launch the cluster in the same region
as your data. Currently data from `aws-publicdatasets`_ are stored in
``us-east-1``, which is where you want to point your EMR cluster.

Common Crawl Region
-------------------
:S3: US Standard
:EMR: US East (N. Virginia)
:API: ``us-east-1``

Create an Amazon EC2 Key Pair and PEM File
------------------------------------------

Amazon EMR uses an Amazon Elastic Compute Cloud (Amazon EC2) key pair
to ensure that you alone have access to the instances that you launch.

The PEM file associated with this key pair is required to ssh directly to the master node of the cluster.

To create an Amazon EC2 key pair:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
1. Go to the Amazon EC2 console
2. In the Navigation pane, click Key Pairs
3. On the Key Pairs page, click Create Key Pair
4. In the Create Key Pair dialog box, enter a name for your key pair, such as, mykeypair
5. Click Create
6. Save the resulting PEM file in a safe location

Configuring ``mrjob.conf``
--------------------------

Make sure to download an EC2 Key Pair ``pem`` file for your map reduce
job and add it to the ``ec2_key_pair`` and ``ec2_key_pair_file``
variables.

Make sure that the ``PEM`` file has permissions set properly by running

.. code:: sh

    $ chown 600 $MY_PEM_FILE

Download the latest version of python to send to your EMR instances.

.. code:: sh

   $ wget https://www.python.org/ftp/python/2.7.11/Python-2.7.11.tgz

Create a ``mrjob.conf`` file to set up your configuration parameters to match
that of AWS.

There is a default configuration template located at ``mrjob.conf.template`` that you can use



.. code:: yaml

    runners:
      hadoop: # also works for emr runner
        jobconf:
          # "true" must be a string argument, not a boolean! (Issue #323)
          mapreduce.output.fileoutputformat.compress: "true"
          mapreduce.output.fileoutputformat.compress.codec: org.apache.hadoop.io.compress.GzipCodec
      emr:
        aws_region: 'us-east-1' # IMPORTANT: us-east-1 so you dont pay transfer fees
        aws_access_key_id: <Required: aws_access_key_id>
        aws_secret_access_key: <Required: aws_secret_access_key>
        ec2_key_pair: <Required: EC2 Key Pair Name>
        ssh_tunnel: true
        ec2_master_instance_type: 'm3.2xlarge'
        ec2_core_instance_bid_price: '0.2'
        ec2_master_instance_bid_price: '0.2'
        ec2_core_instance_type: 'c3.2xlarge'
        emr_tags:
          name: <Optional: Name Tag>
          project: <Optional: Project Tag>
        emr_api_params:
          VisibleToAllUsers: null
        strict_protocols: true
        num_ec2_instances: <Required: Number of Instances>
        ami_version: '3.11.0'
        s3_tmp_dir: <Required: S3 Temp Bucket>
        interpreter: <Required: Interpreter>
        bootstrap:
          - sudo rm $(which pip-2.7)
          - sudo python2.7 get-pip.py#
          - sudo /usr/local/bin/pip2.7 install --upgrade pip wheel setuptoolps
          - sudo /usr/local/bin/pip2.7 install --upgrade ujson boto
          - sudo /usr/local/bin/pip2.7 install -r requirements.txt#

Run on Amazon Elastic MapReduce
-------------------------------

First copy the ``mrjob.conf.template`` into ``mrjob.conf``

Note: > Make sure to fill out the necessary AWS credentials with your
information

.. code:: sh

    python GoogleAnalytics.py -r emr \
        --conf-path="mrjob.conf" \
        --output-dir='s3://your/output/dir' < $(python -m aws)


.. _MRJob: https://pythonhosted.org/mrjob/

.. _aws-publicdatasets: https://aws.amazon.com/public-data-sets/
