#!/usr/bin/python3

### import modules
import os

### install software
cmd = "apt -y install python3-colorama python3-netifaces openssh-server rsyslog firewalld rtpengine kamailio kamailio-json-modules kamailio-geoip-modules \
kamailio-geoip2-modules kamailio-memcached-modules kamailio-utils-modules kamailio-tls-modules kamailio-systemd-modules kamailio-cpl-modules kamailio-extra-modules"
os.system(cmd)

### copy configuration files
os.system('cp -f dispatcher.list /etc/kamailio/')
os.system('cp -rf firewalld /etc/')
os.system('cp -f kamailio.cfg /etc/kamailio/')
os.system('cp -f kamailio-local.cfg /etc/kamailio/')
os.system('cp -f rsyslog.conf /etc/')
os.system('systemctl restart rsyslog')
os.system('cp -f rtpengine.conf /etc/rtpengine/')

### printout
print("Installation completed! Next, run setup.py ;)\n")
