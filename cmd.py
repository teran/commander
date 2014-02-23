#!/usr/bin/env python

from optparse import OptionParser
import os
import readline

import Commander
import Terminal

if __name__ == '__main__':
    parser = OptionParser()

    parser.add_option('-u', '--url', type='string', action='store',
                      dest='url', help='Zabbix URL')
    parser.add_option('-l', '--login', type='string', action='store',
                      dest='login', help='Zabbix user to login with')
    parser.add_option('-p', '--password', type='string', action='store',
                      dest='password', help='Zabbix password')

    parser.add_option('-w', '--write-configuration', action='store_true',
                      default=False,
                      dest='write', help='Write given parameters as default '
                                         'configuration')

    parser.add_option('-c', '--use-cache', action='store_true',
                      default=False, dest='cache',
                      help='Do not reload cache and use the previously '
                           'stored one')

    parser.add_option('-d', '--enable-logging', action='store_true',
                      default=False, dest='logging',
                      help='Enable logging(log store in cache directory)')

    (options, args) = parser.parse_args()

    api_url = os.environ.get('ZABBIX_API_URL', 'http://localhost')

    c = Commander.Commander()

    c.read_configuration()
    c._update_settings(
        url=options.url or os.environ.get(
            'ZABBIX_API_URL', None),
        login=options.login or os.environ.get('ZABBIX_LOGIN', None),
        password=options.password or os.environ.get(
            'ZABBIX_PASSWORD', None)
    )

    if not options.cache:
        c.reload()
    if options.write:
        c.write_configuration()

    c._set_title()

    try:
        while True:
            comp = Terminal.Completer()

            readline.set_history_length(500)
            try:
                readline.read_history_file(
                    os.path.join(c.datadir, 'history'))
            except IOError:
                pass
            readline.set_completer_delims(' \t\n;')
            readline.parse_and_bind('tab: complete')
            readline.set_completer(comp.complete)

            cmd = raw_input('cmd> ').strip()
            if cmd == '':
                continue

            c.cmd(cmd=cmd.split(' '))

            readline.write_history_file(
                os.path.join(c.datadir, 'history'))
    except EOFError:
        print "\nBye!"
