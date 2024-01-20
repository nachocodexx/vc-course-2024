# Create a network
```sh
docker network create -d bridge vc_course
```
# Demo 01: HTTP server
```sh
docker build -f ./Dockerfile_server -t 01-http_server .
```

```sh
 docker run --name 01-http_server_container -e PORT=5000 -v /source/html:/source/html -v ./data:/data -p 5000:5000 -d 01-http_server
```

# Demo 0.2: Web Server (Compose)

```sh
docker compose up --build 
```