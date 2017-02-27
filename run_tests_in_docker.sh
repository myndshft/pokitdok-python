#!/bin/bash

for VERSION in 2.7 3.3 3.4 3.5 3.6
do
  docker run --rm -it -v $PWD:/app/pokitdok python:$VERSION python /app/pokitdok/setup.py develop; APP_ENV=local PYTHONPATH=. nosetests tests/
done