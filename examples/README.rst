Getting Started
====================
It is recommended to utilize the latest version of CommonCrawlJob (directly from Github) rather than from the Pip repository.  

If you've already installed from Pip repository, start by entering:

.. code-block:: sh

   $ pip uninstall CommonCrawlJob

Then, install CommonCrawlJob:

.. code-block:: sh

   $ pip install git+https://github.com/qadium-memex/CommonCrawlJob

Getting Familiar with the Dataset
---------------------------------
Take a glance at the dataset found in ``data/latest.txt``.  You'll find a big list of URL's like so:

::

	common-crawl/crawl-data/CC-MAIN-2016-07/segments/1454701145519.33/warc/CC-MAIN-20160205193905-00000-ip-10-236-182-209.ec2.internal.warc.gz
	common-crawl/crawl-data/CC-MAIN-2016-07/segments/1454701145519.33/warc/CC-MAIN-20160205193905-00001-ip-10-236-182-209.ec2.internal.warc.gz
	common-crawl/crawl-data/CC-MAIN-2016-07/segments/1454701145519.33/warc/CC-MAIN-20160205193905-00002-ip-10-236-182-209.ec2.internal.warc.gz
	common-crawl/crawl-data/CC-MAIN-2016-07/segments/1454701145519.33/warc/CC-MAIN-20160205193905-00003-ip-10-236-182-209.ec2.internal.warc.gz
	common-crawl/crawl-data/CC-MAIN-2016-07/segments/1454701145519.33/warc/CC-MAIN-20160205193905-00004-ip-10-236-182-209.ec2.internal.warc.gz
	common-crawl/crawl-data/CC-MAIN-2016-07/segments/1454701145519.33/warc/CC-MAIN-20160205193905-00005-ip-10-236-182-209.ec2.internal.warc.gz
	common-crawl/crawl-data/CC-MAIN-2016-07/segments/1454701145519.33/warc/CC-MAIN-20160205193905-00006-ip-10-236-182-209.ec2.internal.warc.gz
	common-crawl/crawl-data/CC-MAIN-2016-07/segments/1454701145519.33/warc/CC-MAIN-20160205193905-00007-ip-10-236-182-209.ec2.internal.warc.gz
	common-crawl/crawl-data/CC-MAIN-2016-07/segments/1454701145519.33/warc/CC-MAIN-20160205193905-00008-ip-10-236-182-209.ec2.internal.warc.gz
	common-crawl/crawl-data/CC-MAIN-2016-07/segments/1454701145519.33/warc/CC-MAIN-20160205193905-00009-ip-10-236-182-209.ec2.internal.warc.gz
	common-crawl/crawl-data/CC-MAIN-2016-07/segments/1454701145519.33/warc/CC-MAIN-20160205193905-00010-ip-10-236-182-209.ec2.internal.warc.gz
	common-crawl/crawl-data/CC-MAIN-2016-07/segments/1454701145519.33/warc/CC-MAIN-20160205193905-00011-ip-10-236-182-209.ec2.internal.warc.gz
	common-crawl/crawl-data/CC-MAIN-2016-07/segments/1454701145519.33/warc/CC-MAIN-20160205193905-00012-ip-10-236-182-209.ec2.internal.warc.gz
	...

These are all URL paths of, "chunks" of the total WARC data Common Crawl has collected from around the web (in this case, on its July 2016 crawl).  Each URL is referencing a location on Amazon S3 Public Datasets, where all of the Common Crawl data is hosted for free.  

If you'd like to **see** what the crawl data at a specific URL looks like, add:
``https://aws-publicdatasets.s3.amazonaws.com/`` in front of the URL.  

So, you could end up with something like the URL below, where you can download the data from this chunk and see for yourself: 
``https://aws-publicdatasets.s3.amazonaws.com/common-crawl/crawl-data/CC-MAIN-2016-07/segments/1454701145519.33/warc/CC-MAIN-20160205193905-00000-ip-10-236-182-209.ec2.internal.warc.gz``

While experimenting locally, it is recommended to limit the number of URL's in the ``data/latest.txt`` file to one or two URL's.  This can allow you to test locally on just 1-2 chunks of the total Common Crawl data, without overloading your own computer.

You can always visit the Common Crawl website to get the full list of WARC paths or regenerate this list after by running:

.. code-block:: sh

	# Generates some_file containing s3 buckets
	# some_file is the same file that you'll find in latest.txt
	python -m aws > some_file.txt

An Example Extractor
====================

Let's build a simple extractor for Google Analytics Trackers.

First let's create a file ``GoogleAnalytics.py``

.. code-block:: sh

   $ touch GoogleAnalytics.py

We will go from start to finish in creating a Common Crawl extractor that uses regular expression capture groups to extract
google analytics tracker id's.

Our ``GoogleAnalytics`` class has is overriding one method ``mapper_init`` which defines a compiled regular expressions
that will be matched over the HTML content.

All common crawl jobs will generally obey this pattern.


Running Locally
---------------

Run the Google Analytics extractor locally to test your script.

.. code-block:: sh

    $ python GoogleAnalytics.py -r local <(tail -n 1 data/latest.txt)

If you're having trouble running the code using the command above, try:

.. code-block:: sh

    $ [sudo] python GoogleAnalytics.py < data/latest.txt

In this command, python is running the code for ``GoogleAnalytics.py``, by downloading Common Crawl data from the list of URL's found on ``data/latest.txt``. You'll notice this outputs the results to your command line.  

In this case, removing the -r local tag will actually try to simulate a Hadoop streaming-ish environment, but can introduce some issues.  It is ok for our purposes though, at the moment.

You can then run the below command to get ``GoogleAnalytics.py`` to save the output to a file:

.. code-block:: sh

    $ [sudo] python GoogleAnalytics.py < data/latest.txt | tail >> output.txt

Sample command line output:

::

	Using configs in /etc/mrjob.conf
	Creating temp directory /tmp/GoogleAnalytics.root.20160726.225707.263660
	Running step 1 of 1...
	reading from STDIN
		Counters: 1
			commoncrawl
			processed_record=12261
		Counters: 1
			commoncrawl
			processed_record=12261
	Streaming final output from /tmp/GoogleAnalytics.root.20160726.225707.263660/output...
	Removing temp directory /tmp/GoogleAnalytics.root.20160726.225707.263660...

Sample output.txt file:

::
	
	"http://ccad.edu.websiteoutlook.com/"	"68038641"
	"http://ccc.edu/pages/file-not-found.aspx?url=/departments/events/menu/Pages/Success-Stories.aspx"	"20438531"
	"http://ccc.edu/pages/file-not-found.aspx?url=/departments/events/menu/Pages/Success-Stories.aspx"	"8735345"
	"http://cccreationsusa.com/?ATCLID=206493962&SPID=93247&DB_OEM_ID=27300"	"7776403"
	"http://ccdl.libraries.claremont.edu/cdm/search/collection/cce/searchterm/\u201cThe/mode/all/order/descri"	"60555116"
	"http://ccdl.libraries.claremont.edu/cdm/search/collection/cce/searchterm/candidates/mode/all/order/descri"	"60555116"
	"http://ccdl.libraries.claremont.edu/cdm/search/collection/lea/searchterm/Celebrating"	"60555116"
	"http://ccdl.libraries.claremont.edu/cdm/search/collection/lea/searchterm/treats"	"60555116"
	"http://ccherb.com/category/vaginal-infections/"	"22470526"
	"http://cctvdirectbuy.com/index.php?main_page=product_info&cPath=77&products_id=1461"	"10097023"

Elastic Map Reduce - Configuration
==================================

You're now ready to run the ``GoogleAnalytics.py`` script on Amazon EMR!

Install Hadoop
--------------
You'll need to have Hadoop installed on your machine in order to interface with Amazon's Elastic MapReduce service.  It is difficult to recommend a specific tutorial for this (depends on your OS/OS version as well as what Hadoop version you want), but existing users have had luck installing Hadoop 2.4.0 on Ubuntu 16.04.  It is recommended to choose a hadoop version that Amazon EMR supports.  

Although you won't need the entire Hadoop full capabilities, you can navigate to the Hadoop home directory and validate your installation by typing in:

::

	sbin/start-dfs.sh

Afterwards, type ``jps`` into your command window to confirm your fresh Hadoop intall is running, you should get an output like:

::

	6129 JPS
	5484 NameNode
	5811 SecondaryNameNode
	5969 ResourceManager
	6094 NodeManager
	5610 DataNode


You can then terminate your Hadoop instance by entering:

:: 

	sbin/stop-dfs.sh

Note, during this tutorial, you might have to switch over to your hduser account on your operating system to start/stop Hadoop and in another terminal window, actually run the python script to kickstart EMR from your default (hopefully root) user account.

Setup your requirements.txt file:
---------------------------------
Using the existing requirements.txt template in this repo, add the following line, and save the file:

::

	-e git://github.com/qadium-memex/CommonCrawlJob.git#egg=CommonCrawlJob

This line will install the latest version of CommonCrawl Job on EMR as it is preparing the instance and running its, "bootstrap actions".  

Visit the AWS website and access the S3 web panel.  Create a new bucket on Amazon S3 and call it something like:

::
	
	your-name-emr-scripts

Click, "upload" inside of the new bucket you have created and upload your requirements.txt file.  Make sure to set permissions, so that, the "everyone" group can open/view the file.

Configuring your own environment
--------------------------------
For best performance, you should launch the cluster in the same region
as your data. Currently data from ``aws-publicdatasets`` are stored in
``us-east-1``, which is where you want to point your EMR cluster.

NOTE: EMR is a service that costs money, so, always use this service with caution by monitoring your own expenses.  The authors of this tutorial/software are not responsible for any expenses/damages incurred on your AWS account.  Use at your own risk.

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

There is a default configuration template located at ``mrjob.conf.template`` that you can use.  

You can also try a template like this one below:

::

	# A config file template to build off for running in production
	#
	# If you don't have the yaml module installed, you'll have to use JSON instead,
	# which would look something like this:

	runners:
	  emr:
	    # We run on `us-east-1`
	    # This ensure colocation with the CommonCrawl s3 bucket
	    aws_region: 'us-east-1'
	    aws_access_key_id:                                    # enter here
	    aws_secret_access_key:                                # enter here
	    ec2_key_pair:     # enter the name of your key pair file (without extension here) eg. key
	    ec2_key_pair_file: # enter here with .pem extension (eg. key.pem), make sure this key pair file is in the same directory as this file with the appropriate permissions.
	    ssh_tunnel: true
	    ssh_tunnel_is_open: true

	    # Remember to change to a more beefier in production
	    num_ec2_instances: 1
	    ec2_instance_type: 'm1.xlarge'
	    ec2_master_instance_type: 'm1.xlarge'

	    # Getting the right ami_version is important to get right.
	    # https://pythonhosted.org/mrjob/guides/emr-bootstrap-cookbook.html#installing-system-packages
	    ami_version: '3.11.0'
	    python_bin: python2.7
	    interpreter: python2.7

	    # These are functionally optional but realistically are not
	    emr_tags:
	        project: testing_commoncrawl
	        name: testing_commoncrawl

	    bootstrap_action:
	        - s3://elasticmapreduce/bootstrap-actions/install-ganglia

	    upload_files:
	        - GoogleAnalytics.py
	        - requirements.txt

	    bootstrap:
	        # Get the most current versions of packaging libraries
	        - sudo pip-2.7 install ujson setuptools wheel pip
	        - sudo yum install -y git  #this is so you can use the latest version of CommonCrawlJob (instead of the outdated one in the pip repo)
	        - sudo pip-2.7 install --upgrade setuptools
	        - sudo wget   # Paste in the Direct https url for the requirements txt file you uploaded to your s3 bucket (eg. https://s3.amazonaws.com/your-name-emr-scripts/requirements.txt )
        	- sudo pip-2.7 install -r requirements.txt

Although you can include a flag when you are running your job to this configuration file in the same directory as your python script, it is recommended to paste your mrjob.conf file in your `etc` directory along with your key file (with the recommended permissions above).  MrJob (a dependency for CommonCrawlJob) will automatically look into the `etc/` directory first.

Deploy on EMR
=============

Start Hadoop
------------
Switch over to the hadoop account (likely hduser) and navigate to your Hadoop home directory.  Enter the command:

::

	sbin/start-yarn.sh

This setups the resource manager we will need to interface with EMR.

Type in ``jps`` and you should get output like:

::

	9155 NodeManager
	9480 Jps
	9006 ResourceManager


Call EMR
--------
Switch over to another terminal with your default user account and navigate to the directory with the GoogleAnalytics.py file.  Enter the below command:

.. code-block:: sh

    python GoogleAnalytics.py -r emr --output-dir='s3://fresh-bucket-name-here/output' < data/latest.txt

Note: enter a bucket name which currently does not exist on your S3 account.  Make sure to include ``/output`` at the end to avoid getting errors.	

Note: While testing, it is again recommended to only have 1/2 URLs inside of your ``data/latest.txt`` file, otherwise the above command will process over the ENTIRE Common Crawl dataset. 


Sit back as EMR begins processing
---------------------------------
It should take about 5 minutes to crawl over the 1/2 url path chunks you gave in your ``data/latest.txt`` file.  Here's some sample command line output you should see:

::

	python GoogleAnalytics.py -r emr --output-dir='s3://fresh-common-crawl-bucket/output' < data/latest.txt
	Using configs in /etc/mrjob.conf
	Unexpected option bootstrap_action from /etc/mrjob.conf
	Auto-created temp S3 bucket mrjob-6e2b70841572fdca
	Using s3://mrjob-6e2b70841572fdca/tmp/ as our temp dir on S3
	Creating temp directory /tmp/GoogleAnalytics.hduser.20160727.002907.104465
	reading from STDIN
	Copying local files to s3://mrjob-6e2b70841572fdca/tmp/GoogleAnalytics.hduser.20160727.002907.104465/files/...
	Setting EMR tags: project=testing_commoncrawl, name=testing_commoncrawl
	Created new cluster j-2YB8E42RAAWBK
	Setting EMR tags: project=testing_commoncrawl, name=testing_commoncrawl
	Waiting for step 1 of 1 (s-19YMWDXCJ7FBI) to complete...
	  PENDING (cluster is STARTING)
	  PENDING (cluster is STARTING)
	  PENDING (cluster is STARTING)
	  PENDING (cluster is STARTING)
	  PENDING (cluster is STARTING)
	  PENDING (cluster is BOOTSTRAPPING: Running bootstrap actions)
	  PENDING (cluster is BOOTSTRAPPING: Running bootstrap actions)
	  PENDING (cluster is BOOTSTRAPPING: Running bootstrap actions)
	  PENDING (cluster is BOOTSTRAPPING: Running bootstrap actions)
	  Opening ssh tunnel to resource manager...
	  Connect to resource manager at: http://MY-COMPUTER:40329/cluster
	  RUNNING for 8.8s
	  RUNNING for 41.2s
	  RUNNING for 72.6s
	  RUNNING for 103.4s
	  RUNNING for 136.2s
	  COMPLETED
	Attempting to fetch counters from logs...
	Looking for step log in /mnt/var/log/hadoop/steps/s-19YMWDXCJ7FBI on ec2-54-197-3-188.compute-1.amazonaws.com...
	  Parsing step log: ssh://ec2-54-197-3-188.compute-1.amazonaws.com/mnt/var/log/hadoop/steps/s-19YMWDXCJ7FBI/syslog
	Counters: 55
		File Input Format Counters 
			Bytes Read=1278
		File Output Format Counters 
			Bytes Written=264517
		File System Counters
			FILE: Number of bytes read=176255
			FILE: Number of bytes written=2775884
			FILE: Number of large read operations=0
			FILE: Number of read operations=0
			FILE: Number of write operations=0
			HDFS: Number of bytes read=2538
			HDFS: Number of bytes written=0
			HDFS: Number of large read operations=0
			HDFS: Number of read operations=18
			HDFS: Number of write operations=0
			S3: Number of bytes read=1278
			S3: Number of bytes written=264517
			S3: Number of large read operations=0
			S3: Number of read operations=0
			S3: Number of write operations=0
		GoogleAnalytics
			match=4087
		Job Counters 
			Data-local map tasks=18
			Launched map tasks=18
			Launched reduce tasks=5
			Total megabyte-seconds taken by all map tasks=680242176
			Total megabyte-seconds taken by all reduce tasks=203059200
			Total time spent by all map tasks (ms)=885732
			Total time spent by all maps in occupied slots (ms)=2657196
			Total time spent by all reduce tasks (ms)=99150
			Total time spent by all reduces in occupied slots (ms)=793200
			Total vcore-seconds taken by all map tasks=885732
			Total vcore-seconds taken by all reduce tasks=99150
		Map-Reduce Framework
			CPU time spent (ms)=51840
			Combine input records=0
			Combine output records=0
			Failed Shuffles=0
			GC time elapsed (ms)=8965
			Input split bytes=2538
			Map input records=1
			Map output bytes=317181
			Map output materialized bytes=177595
			Map output records=3079
			Merged Map outputs=90
			Physical memory (bytes) snapshot=9866244096
			Reduce input groups=2656
			Reduce input records=3079
			Reduce output records=2656
			Reduce shuffle bytes=177595
			Shuffled Maps =90
			Spilled Records=6158
			Total committed heap usage (bytes)=10636230656
			Virtual memory (bytes) snapshot=34872307712
		Shuffle Errors
			BAD_ID=0
			CONNECTION=0
			IO_ERROR=0
			WRONG_LENGTH=0
			WRONG_MAP=0
			WRONG_REDUCE=0
	Streaming final output from s3://fresh-common-crawl-bucket/output/...
	"http:\/\/1012lounge.com\/"	"3479925"
	"http:\/\/102theriver.iheart.com\/articles"	"45084235"
	"http:\/\/1065ctq.iheart.com\/articles\/national-news-104668\/new-electronic-license-plates-could-be-11383289\/"	"45084235"
	"http:\/\/12160.info\/group\/gunsandtactics\/forum\/topic\/show?id=2649739:Topic:1105218&xg_source=msg"	"2024191"
	"http:\/\/1350kman.com\/settlement-reached-in-salina-contamination-cleanup\/"	"47189603"
	"http:\/\/2670.antiquesnavigator.com\/index.php?main_page=product_info&cPath=124&products_id=4628"	"212281"
	"http:\/\/303magazine.com\/2012\/10\/undead-mans-party-casselmans-hosts-zombie-crawl-aftermath-featuring-celldweller\/"	"19049911"
	"http:\/\/511.ky.gov\/kylb\/roadreports\/event.jsf?sitKey=kycars4-10068&view=state&text=l&textOnly=false&current=true"	"16329038"
	"http:\/\/610wtvn.iheart.com\/articles\/entertainment-news-104658\/fun-to-perform-with-queen-at-11672188\/"	"45084235"
	"http:\/\/7warez.mihanblog.com\/post\/tag\/\u062f\u0627\u0646\u0644\u0648\u062f+KMPlayer+3"	"153829"
	"http:\/\/949thebull.iheart.com\/onair\/caffeinated-radio-jason-pullman-kristen-gates-30022\/celeb-perk-11513-11797938\/"	"45084235"
	"http:\/\/965tic.cbslocal.com\/2011\/05\/05\/cinco-de-mayo-top-10-tasty-mexican-inspired-cocktails-for-your-feista-3\/3\/"	"19997300"
	"http:\/\/987ampradio.cbslocal.com\/2011\/02\/13\/cee-lo-green-gwyneth\/"	"20574553"
	"http:\/\/987ampradio.cbslocal.com\/tag\/going-out\/"	"20574553"
	"http:\/\/99mpg.com\/workshops\/understandingdiagn\/firststart\/"	"43148446"
	"http:\/\/9to5mac.com\/2012\/11\/22\/black-friday-week-daily-deal-roundup-thanksgiving-edition\/?utm_source=feedburner&utm_medium=feed&utm_campaign=Feed:+9To5Mac-MacAllDay+(9+to+5+Mac+-+Apple+Intelligence)"	"1493547"
	"http:\/\/JMART8@luc.edu\/neuroscience\/index.shtml"	"5482792"
	"http:\/\/abcnews.go.com\/WNT\/video\/instant-index-skydiver-takes-cue-mary-poppins-latest-18643837"	"225447"
	...

	Removing s3 temp directory s3://mrjob-6e2b70841572fdca/tmp/GoogleAnalytics.hduser.20160727.002907.104465/...
	Removing temp directory /tmp/GoogleAnalytics.hduser.20160727.002907.104465...
	Removing log files in s3://mrjob-6e2b70841572fdca/tmp/logs/j-2YB8E42RAAWBK/...
	Terminating cluster: j-2YB8E42RAAWBK

Navigate to the bucket name you created when entering the command and you should see your results output inside of the bucket.  EMR has already split the output results into multiple files.

Here's a sample of some output inside of the ``part-00000.gz`` file:

::

	"http:\/\/1012lounge.com\/"	"3479925"
	"http:\/\/102theriver.iheart.com\/articles"	"45084235"
	"http:\/\/1065ctq.iheart.com\/articles\/national-news-104668\/new-electronic-license-plates-could-be-11383289\/"	"45084235"
	"http:\/\/12160.info\/group\/gunsandtactics\/forum\/topic\/show?id=2649739:Topic:1105218&xg_source=msg"	"2024191"
	"http:\/\/1350kman.com\/settlement-reached-in-salina-contamination-cleanup\/"	"47189603"
	"http:\/\/2670.antiquesnavigator.com\/index.php?main_page=product_info&cPath=124&products_id=4628"	"212281"
	"http:\/\/303magazine.com\/2012\/10\/undead-mans-party-casselmans-hosts-zombie-crawl-aftermath-featuring-celldweller\/"	"19049911"
	"http:\/\/511.ky.gov\/kylb\/roadreports\/event.jsf?sitKey=kycars4-10068&view=state&text=l&textOnly=false&current=true"	"16329038"
	"http:\/\/610wtvn.iheart.com\/articles\/entertainment-news-104658\/fun-to-perform-with-queen-at-11672188\/"	"45084235"
	"http:\/\/7warez.mihanblog.com\/post\/tag\/\u062f\u0627\u0646\u0644\u0648\u062f+KMPlayer+3"	"153829"
	"http:\/\/949thebull.iheart.com\/onair\/caffeinated-radio-jason-pullman-kristen-gates-30022\/celeb-perk-11513-11797938\/"	"45084235"
	"http:\/\/965tic.cbslocal.com\/2011\/05\/05\/cinco-de-mayo-top-10-tasty-mexican-inspired-cocktails-for-your-feista-3\/3\/"	"19997300"
	"http:\/\/987ampradio.cbslocal.com\/2011\/02\/13\/cee-lo-green-gwyneth\/"	"20574553"
	"http:\/\/987ampradio.cbslocal.com\/tag\/going-out\/"	"20574553"
	"http:\/\/99mpg.com\/workshops\/understandingdiagn\/firststart\/"	"43148446"
	...

Now that EMR is terminated, navigate back to your hadoop home directory and enter the below line to terminate the resource manager:

::

	sbin/stop-yarn.sh

You have now successfully ran your first EMR job over part of the Common Crawl Archive!

Next Steps
----------
When ready, run the above command over every URL inside of the original ``data/latest.txt`` file.   This will run ``GoogleAnalytics.py`` over the ENTIRE Common Crawl July 2016 archive.  

Proceed with caution as this is a bigger EMR job and could be costly ... continue at your own risk ;)  Best of luck!!
