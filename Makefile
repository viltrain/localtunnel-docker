ID := $(shell docker inspect -f   "{{.Id}}"  localtunnel)

build: ; docker stop localtunnel && docker rm localtunnel && docker build -t localtunnel . && docker run --name localtunnel -v /var/run/docker.sock:/tmp/docker.sock -d localtunnel
  
run: ; docker exec -it localtunnel /bin/bash
  
logs: ; docker logs localtunnel 


copy: ; sudo cp * '/var/lib/docker/aufs/mnt/$(ID)/app/' && docker exec -it localtunnel docker-gen -only-exposed /app/hosts.tmpl /tmp/hosts.json && docker exec -it localtunnel python /app/service.py
