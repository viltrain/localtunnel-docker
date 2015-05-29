#!/usr/bin/env python

import os
import sys
import glob
import signal
import json
import re
import shlex
from subprocess import Popen, PIPE

sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)

import logging
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger('localtunnel')


RUNNING = True
TUNNELS = {}

def cleanup_tunnels():
  for name, info in TUNNELS.items():
    process, url = info
    print 'killing tunnel', name
    process.kill()

import atexit
atexit.register(cleanup_tunnels)

def handler_ctrlz(signum, frame):
  print 'Ctrl+Z pressed'
  global RUNNING
  RUNNING = False
  signal.alarm(1)
signal.signal(signal.SIGTSTP, handler_ctrlz)


def signal_handler(signal, frame):
  global TUNNELS
  hosts = read_hosts()
  ensure_hosts(hosts.keys())
  names = []
  logger.info('reloading hosts')
  for vhost, containers in hosts.items():
    for container in containers:
      name = (container['subdomain'], vhost)
      if name not in TUNNELS:
        logger.info('Adding tunnel %s', name)
        TUNNELS[name] = start_tunnel(container['subdomain'], vhost)
      names.append(name)
  for name in TUNNELS.keys():
    if name not in names:
      logger.info('Removing tunnel %s', name)
      p, url = TUNNELS[name]
      p.kill()
      del TUNNELS[name]
signal.signal(signal.SIGINT, signal_handler)


def handler(signum, frame):
  global TUNNELS
  tunnels = [(name,info[1]) for name, info in TUNNELS.items()]
  logger.info('Checking tunnels: %s', tunnels)
  for name, info in TUNNELS.items():
    process, url = info
    if process.poll() is not None:
      logger.warn('Tunnel %s has terminated, restarting...', name)
      TUNNELS[name] = start_tunnel(name[0], name[1])
signal.signal(signal.SIGALRM, handler)


def read_hosts():
  def clean_json(string):
    string = re.sub(",[ \t\r\n]+}", "}", string)
    string = re.sub(",[ \t\r\n]+\]", "]", string)

    return string
  try:
    with open('/tmp/hosts.json', 'rb') as f:
      data = clean_json(f.read())
      return json.loads(data)
  except Exception as e:
    print 'Warning', e
    return {}


def start_tunnel(vname, vhost):
  logger.info('Starting tunnel subdomain:%s local-host:%s', vname, vhost)
  if '<no value>' == vname:
    p = Popen(shlex.split('lt --local-host {1} --port 80'.format(vname, vhost)), stdout=PIPE)
  else:
    p = Popen(shlex.split('lt --subdomain {0} --local-host {1} --port 80'.format(vname, vhost)), stdout=PIPE)
  line = p.stdout.readline()
  line = line.split(':', 1)[1].replace('\n', '').strip()
  logger.info('{0} for {1} {2}'.format(line, vname, vhost))
  return p, line


def ensure_hosts(hosts):
  host_ip = '172.17.42.1' #TODO: use netstat -nr | grep '^0\.0\.0\.0' | awk '{print $2}'
  with open('/etc/hosts', 'r+b') as f:
    data = f.read()
    data = data.split('####\n')[0]
    data += '####\n'
    for host in hosts:
      data += '{0} {1}\n'.format(host_ip, host)
    f.seek(0)
    f.write(data)
    f.close()
    
if __name__ == '__main__':
  logger.debug('Starting tunnel service')
  
  signal_handler(None, None)
  
  while RUNNING:
    signal.alarm(20)
    sys.stdout.flush()
    signal.pause()

