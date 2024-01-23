#!/bin/bash
N=${1:-1}

for index in $(seq 0 $N); do
	path="/mictlanx/mictlanx-peer-${index}"
	echo "PATH = ${path}"

	sudo rm -rf "${path}/local"
	sudo mkdir -p "${path}/local"

	sudo rm -rf "${path}/data"
	sudo mkdir -p "${path}/data"

	sudo rm -rf "${path}/log"
	sudo mkdir -p "${path}/log"

	sudo rm -rf "${path}/keys"
	sudo mkdir -p "${path}/keys"
	
	sudo chmod -R 744 "${path}/data"
	sudo chmod -R 744 "${path}/log"
	sudo chmod -R 744 "${path}/local"
	
	sudo chown -R 1001:1002 "${path}"
done

