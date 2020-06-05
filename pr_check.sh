#!/bin/bash

set -exv

python3 -m venv .
source bin/activate
bin/pip3 install --upgrade pip
bin/pip3 install .
bin/flake8
