#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# author mengskysama

import os
import hashlib
import re
import socket
socket.setdefaulttimeout(30)


def md5(_str):
    m2 = hashlib.md5()
    m2.update(_str)
    return m2.hexdigest()


def get_deluge_local_auth():
    xdg_config = os.path.expanduser(os.environ.get("XDG_CONFIG_HOME",
                                                   "~/.config"))
    config_home = os.path.join(xdg_config, "deluge")
    auth_file = os.path.join(config_home, "auth")
    username = password = ""
    with open(auth_file) as fd:
        for line in fd:
            if line.startswith("#"):
                continue
            auth = line.split(":")
            if len(auth) >= 2 and auth[0] == "localclient":
                username, password = auth[0], auth[1]
                break
    return username, password


class InterfaceHelper(object):

    def __init__(self, if_name):
        self._if_name = if_name

    def get_interface_info(self):
        r = os.popen('ifconfig').read()
        r = re.findall('(\S+)([\s\S]+?)\n\n', r)
        for i in r:
            if i[0] == self._if_name:
                return i[1]
        return None

    def get_transfer(self):
        r = self.get_interface_info()
        r = re.findall(':(\S+)\s\(', r)
        return map(lambda x: int(x), r)

    def get_ip(self):
        r = self.get_interface_info()
        return re.findall("inet\saddr:(\d+.\d+.\d+.\d+)", r)[0]
