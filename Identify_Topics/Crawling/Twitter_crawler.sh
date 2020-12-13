#!/bin/bash
# sed -i 's/\r//g' Twitter_crawler.sh

for ((i=0; i>=0; i++))
do
  echo ${i}
  {
    python Twitter_crawler.py
    python utils.py
    echo "finish"
  } &
  sleep 15m
done