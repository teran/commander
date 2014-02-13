#!/usr/bin/env python

import os
import readline

import Commander
import Terminal

if __name__ == '__main__':
    api_url = os.environ.get('ZABBIX_API_URL', 'http://localhost')
    c = Commander.Commander(api_url=api_url)
    c.reload()
    c._set_title()
    try:
        while True:
            comp = Terminal.Completer()
            readline.set_history_length(500)
            readline.read_history_file(
                os.path.join(c.datadir, '_history.dat'))
            readline.set_completer_delims(' \t\n;')
            readline.parse_and_bind('tab: complete')
            readline.set_completer(comp.complete)
            cmd = raw_input('cmd> ').strip()
            if cmd == '':
                continue
            c.cmd(cmd=cmd.split(' '))
            readline.write_history_file(
                os.path.join(c.datadir, '_history.dat'))
    except EOFError:
        print "\nBye!"
