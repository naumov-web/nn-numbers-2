#!/bin/bash

echo -e "\e[32mConnecting to python container!"
echo -e "\e[97m"

CONTAINER_ID=`docker ps -qf "name=nn_2_python"`

if [[ -z "$CONTAINER_ID" ]]; then
    echo -e "\e[31mContainer not found in running containers!"
    echo -e "\e[97m"
    exit
fi

docker exec -it $CONTAINER_ID /bin/bash