#!/bin/bash

for VERSION in 2.7
do
    PYTHON_VERSION=$VERSION docker-compose build
done