#!/usr/bin/env python

import readline
import os
import sys
import time

import Commander

if __name__ == '__main__':
    api_url = os.environ.get('ZABBIX_API_URL', 'http://localhost')
    c = Commander.Commander(api_url=api_url)
    c.reload()
    try:
        while True:
            cmd = raw_input('cmd> ').strip()
            if cmd == '':
                continue
            print c.cmd(cmd=cmd.split(' '))
    except EOFError:
        print "\nBye!"
        pass