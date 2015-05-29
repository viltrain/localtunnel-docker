tunnels: python -u /app/service.py
dockergen: docker-gen -watch -only-exposed -notify "/bin/bash /app/reload.sh" /app/hosts.tmpl /tmp/hosts.json
