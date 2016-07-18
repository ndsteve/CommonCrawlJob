.. example

An Example Extractor
====================

Let's build a simple extractor for Google Analytics Trackers.

First let's create a file ``GoogleAnalytics.py``

.. code-block:: sh

   $ touch GoogleAnalytics.py

We will go from start to finish in creating a Common Crawl extractor that uses regular expression capture groups to extract
google analytics tracker id's.

.. literalinclude:: GoogleAnalytics.py
   :language: python

Our ``GoogleAnalytics`` class has is overriding one method ``mapper_init`` which defines a compiled regular expressions
that will be matched over the HTML content.

All common crawl jobs will generally obey this pattern.

Running Locally
---------------

Run the Google Analytics extractor locally to test your script.

.. code-block:: sh

    $ python GoogleAnalytics.py -r local <(tail -n 1 data/latest.txt)

Configuration
=============

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
---------------------------------

.. image:: /static/img/EC2KeyPair.png
   :alt: EC2 Key Pair
   :align: center

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

.. code-block:: sh

    $ chown 600 $MY_PEM_FILE

Download the latest version of python to send to your EMR instances.

.. code-block:: sh

   $ wget https://www.python.org/ftp/python/2.7.11/Python-2.7.11.tgz

Create a ``mrjob.conf`` file to set up your configuration parameters to match
that of AWS.

There is a default configuration template located at ``mrjob.conf.template`` that you can use

.. literalinclude:: mrjob.conf.template
   :language: yaml

Deploy on EMR
=============

First copy the ``mrjob.conf.template`` into ``mrjob.conf``

Note: > Make sure to fill out the necessary AWS credentials with your
information

.. code-block:: sh

    python GoogleAnalytics.py -r emr \
        --conf-path="mrjob.conf" \
        --output-dir='s3://your/output/dir' < $(python -m aws)

.. _aws-publicdatasets: https://aws.amazon.com/public-data-sets/
