#!/bin/bash
cd cp $(dirname $0)
docker build -t xiaokai2022/mdc --no-cache=true ./

function echo_green() {
  echo -e "\033[32m$1\033[0m"
}
echo_green "是否上传到 docker hub ?(y/n)"
read answer
if [ "$answer" == "y" ]; then
  docker push xiaokai2022/mdc
fi