# Cheatsheet: Networks
## 1. List the networks
```bash
docker network ls
```
## 2. Create a network (bridge)
```bash
docker network create -d bridge <NETWORK_NAME>
```
## 3. Inspect a network
```bash
docker network inspect <NETWORK_NAME>
```