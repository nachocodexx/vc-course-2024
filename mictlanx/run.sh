#!/bin/bash
N=${3:-1}
if [ "$1" -eq "1" ]; then
	echo "Removing peer's data..."
	./create_folders.sh $N
fi 

yml_file=${2:-mictlanx}

echo "Removing existing peer's containers"
docker compose -f ./${yml_file}.yml -p mictlanx down

echo "Deploying peers' containers"
docker compose -f ./${yml_file}.yml -p mictlanx up -d


