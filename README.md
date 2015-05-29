Automatically create localtunnels (http://localtunnel.me) for containers.

### Usage

To run it:

    $ docker run --name proxy -d -p 80:80 -v /var/run/docker.sock:/tmp/docker.sock jwilder/nginx-proxy
    $ docker run --name localtunnel -v /var/run/docker.sock:/tmp/docker.sock -d -t viltrain/localtunnel-docker git://github.com/viltrain/localtunnel-docker.git

Then start any containers you want proxied with an env var `VIRTUAL_HOST=subdomain.local` and an optional subdomain `SUBDOMAIN=mywebapp`

    $ docker run -e "VIRTUAL_HOST=mywebapp.local" -e "SUBDOMAIN=mywebapp" -e "PROVIDER=mywebapp" --name mywebapp -d -t training/webapp

Which will allow you to connect to your container on http://mywebapp.localtunnel.me
