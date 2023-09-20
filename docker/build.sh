#!/bin/bash
cd $(dirname $0)
docker build -t xiaokai2022/mdc --no-cache=true ./