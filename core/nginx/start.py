#!/usr/bin/python

import os
import subprocess

# Check if a stale pid file exists
if os.path.exists("/var/log/nginx.pid"):
    os.remove("/var/log/nginx.pid")

# Actual startup script
if not os.path.exists("/certs/dhparam.pem") and os.environ["TLS_FLAVOR"] != "notls":
    os.system("openssl dhparam -out /certs/dhparam.pem 4096")

if os.environ["TLS_FLAVOR"] == "letsencrypt":
    subprocess.Popen(["/letsencrypt.py"])

subprocess.call(["/config.py"])
os.execv("/usr/sbin/nginx", ["nginx", "-g", "daemon off;"])
