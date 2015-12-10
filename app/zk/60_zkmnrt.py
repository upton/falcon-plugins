#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
@author: upton
'''
import subprocess
import socket
import json
import time

host = socket.gethostname()
timestamp = int(time.time())

cmd = 'echo mntr | nc 127.0.0.1 2181'
proc = subprocess.Popen([cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
out, err = proc.communicate()
if not err:
    metrics = []
    for line in out.splitlines():
        info = line.split('\t', 1)
        if 'zk_version' != info[0] and 'zk_server_state' != info[0]:
            metric = {}

            metric['metric'] = info[0]
            metric['timestamp'] = timestamp
            metric['endpoint'] = host
            metric['value'] = info[1]
            metric['counterType'] = 'GAUGE'
            metric['step'] = 60
            metric['tags'] = ''
            
            metrics.append(metric)
    
    print json.dumps(metrics)
