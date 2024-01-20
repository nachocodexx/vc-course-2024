# Create a network
```sh
docker network create -d bridge vc_course
```
# Demo 0: First container 
```sh
docker build -f ./Dockerfile -t 00-basics .
```
```sh
docker run --name 00-basics-container -e NAME=yourname -d 00-basics
```