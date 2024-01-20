# Demo 5: Docker swarm 
In this tutorial you'll see the most used commands in ```Docker Swarm```:

## Nodes
### 1. List nodes
```bash
docker node ls
```
### 2. Inspect a node
```bash
docker node inspect <NODE_ID>
```
## Services
### 1. List services
```bash
docker service ls
```
### 2. Inspect a service
```bash
docker service inspect <SERVICE_ID>
```
### 3. Remove service
```bash
docker service rm <SERVICE_ID>
```
## Stack
### 1. Deploy a stack
```bash
docker stack deploy -c <YAML_FILE_PATH> <STACK_NAME>
```
### 2. List stacks
```bash
docker stack ls
```
### 3. Inspect stack
```bash
docker stack ps <STACK_NAME>
```
### 4. List services of the stack
```bash
docker stack services <STACK_NAME>
```
### 5. Remove a stack
```bash
docker stack rm <STACK_NAME>
```