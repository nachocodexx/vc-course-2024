# Cheatsheet: Container

## 1. Running a container
```
docker run [OPTIONS] IMAGE [COMMANDS] [ARG...]
```
Example: Run a container in detached mode and map ports
```
docker run -d -p 80:80 nginx
```
## 2. Listing containers
- **Command**: 
```bash
docker ps and docker ps -a
```
- **Description**: Lists all running containers. Use -a to list all containers, including stopped ones.

## 3. Sotpping a container
  - **Command**
```bash
docker stop [CONTAINER ID or NAME
```
  - **Description**: Stops a running container. Replace [CONTAINER ID or NAME] with the container's ID or name.

## 4. Starting a container
  - **Command**
```bash
docker start [CONTAINER ID or NAME]
```
  - **Description**: Starts a stopped container.

## 5. Removing a container
  - **Command**
```bash
docker rm [CONTAINER ID or NAME]
```
  - **Description**: Removes a stopped container.

## 6. Executing Commands Inside a ContainerSotpping a container
  - **Command**
```bash
docker exec [OPTIONS] [CONTAINER ID or NAME] COMMAND [ARG...]
```
  - **Description**: Executes a command inside a running container. Useful for interactive debugging or configuration.
  - **Example**:
```bash
docker exec -it [CONTAINER ID or NAME] bash
```

## 7. Viewing Container LogsSotpping a container
  - **Command**
```bash
docker logs [CONTAINER ID or NAME]
```
  - **Description**: Displays the logs from a container. Useful for troubleshooting and monitoring the container's operation.