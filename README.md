# Virtualization demos

In this readme file you'll see the commands to run the demos.

The folder structure:  

```bash
.
├── 00-basics
│   ├── Dockerfile
│   ├── README.md
│   ├── __pycache__
│   ├── requirements.txt
│   └── src
├── 01-http_server
│   ├── Dockerfile_server
│   ├── README.md
│   ├── data
│   ├── docker-compose.yml
│   ├── requirements.txt
│   └── src
├── 02-xolo_QR_generator
│   ├── Dockerfile
│   ├── README.md
│   ├── config
│   ├── docker-compose.yml
│   ├── requirements.txt
│   └── src
├── 03-xolo_consumer
│   ├── Dockerfile
│   ├── README.md
│   ├── config
│   ├── docker-compose.yml
│   ├── requirements.txt
│   └── src
├── 04-swarm-basics
│   └── README.md
├── 05-mictlanx-summoner
│   ├── Dockerfile-consumer
│   ├── Dockerfile-encrypt
│   ├── Dockerfile-producer
│   ├── README.md
│   ├── requirements.txt
│   └── src
├── README.md
├── cheatsheets
│   ├── containers.md
│   ├── networks.md
│   └── volumes.md
```
## Prerequisites
You must create a Docker network using the following command:
```bash
docker network create -d bridge <NETWORK_NAME> --subnet=10.0.0.1/25
```

## 1. Install
The only thing you need for this course is Docker, the instructions depends mainly of your operating system, so it is better that you go to the official web page of the virtual container platform Docker: https://docs.docker.com/engine/install/

Also I recommend installing the following http client:
https://httpie.io/desktop

## 2. Download / Clone
To get the project you need to download this repo or clone it, if you select to clone then:
```bash
git clone git@gitghub.com:nachocodexx/vc-course-demos
```



## 3. Hands-On

### Demo 0: Introduction to docker containers (Hello world)
This demo show you how to create an basic python image and a basic web server using Flask then deploy all the services using docker compose.

All the commands are relative to the /00-basics folder, please ensure that you are in that folder, if you dont then:
```bash
cd <PATH>/demo0  
```
The ```<PATH>``` is the path where you saved this repo if you dont have the repo please go to the section 2. Download / Clone

Now you are ready to continue this demo is a simple qr generator to share whatever you want using a qr code.

### Demo 1: First virtual container (Web server)
All the commands are relative to the /01-http_server folder, please ensure that you are in that folder, if you dont then:
```bash
cd <PATH>/demo1  
```
The ```<PATH>``` is the path where you saved this repo if you dont have the repo please go to the section 2. Download / Clone

### Demo 2: Xolo QR Generator
### Demo 3: Xolo Consumer
### Demo 4: MictlanX Summoner