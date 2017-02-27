#!/bin/bash

for VERSION in 2.7 3.3
do
    PYTHON_VERSION=$VERSION docker-compose build
done