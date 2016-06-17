#!/usr/bin/env bash

sudo rm $(which pip-2.7)
sudo python2.7 get-pip.py#
sudo /usr/local/bin/pip2.7 install --upgrade pip wheel setuptools
sudo /usr/local/bin/pip2.7 install --upgrade ujson boto
sudo /usr/local/bin/pip2.7 install -r requirements.txt#

