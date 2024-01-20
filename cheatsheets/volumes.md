# Cheatsheet: Volumes
The basic commands to manage volumes that are the perferred mechanism for persisting data generated by and used by Docker containers.

## 1. List all avaiable volumes
```bash
docker volume ls 
```
## 2. Create a volume (default config)
```bash
docker volume create <VOLUME_NAME>
```
## 3. Inspect a volume:
```bash
docker volume inspect <VOLUME_NAME>
```
```console
[
    {
        "CreatedAt": "2023-09-11T07:19:02Z",
        "Driver": "local",
        "Labels": null,
        "Mountpoint": "/var/lib/docker/volumes/mictlanx/_data",
        "Name": "mictlanx",
        "Options": null,
        "Scope": "local"
    }
]
```
## 4. Delete a volume
```bash
docker volume rm <VOLUME_NAME>
```