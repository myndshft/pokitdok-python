#!/bin/bash

for VERSION in 2.7 3.2 3.3 3.4 3.5
do
  docker run --rm -it \
  --env-file ./env.list \
  -v $PWD:/app/pokitdok python:$VERSION \
  /bin/sh /app/pokitdok/setup_and_test.sh
done

docker run --rm -it \
--env-file ./env.list \
-v $PWD:/app/pokitdok pypy:2-5.6.0 \
/bin/sh /app/pokitdok/setup_and_test.sh