# Demo 4: Deploying multiple containers using a Compose
Build the qr generator app:
```bash
docker build -f ./Dockerfile -t 02_xolo_qr_generator .
```
In this demo we use a YAML file that describe a container, to execute the containers using compose please type the following commands:
```bash
docker compose -f ./docker-compose.yml up # use the flag -d to run the compose in detached mode
```

to stop and remove the containers Press Cntrl + C or if you run the compose in detached mode u can use the following command:
```bash
docker compose -f ./docker-compose.yml down
```
