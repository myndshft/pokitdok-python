#!/bin/bash

for VERSION in 2.7
do
  docker run --rm -it -v $PWD:/app/pokitdok python:$VERSION python /app/pokitdok/setup.py develop; APP_ENV=local PYTHONPATH=. nosetests tests/
done