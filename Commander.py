import json
import os
import subprocess

import pyzabbix

class Commander():
    _api = None
    commands = [
        'grouplist',
        'hostlist',
        'p_exec',
        'reload',
        'ssh'
    ]
    def __init__(self, api_url='http://localhost', login='admin',
                 password='zabbix',
                 datadir='.commander'):
        self.api_url = api_url
        self.login = login
        self.password = password
        self.datadir = datadir

    @property
    def api(self):
        if self._api:
            return self._api

        self._api = pyzabbix.ZabbixAPI(self.api_url)
        self._api.login(self.login, self.password)

        return self._api


    def _set_title(self, title='cmd.py'):
        print "\033]0;%s\007" % title

    def _read_cache(self, file):
        f = open(os.path.join(self.datadir, file), 'r')
        res = []
        for l in f.read().split("\n"):
            if l != '':
                res.append(l)
        f.close()
        return res

    def _store_cache(self, file, data):
        f = open(os.path.join(self.datadir, file), 'w')
        f.write("\n".join(data)+"\n")
        f.close()

    def cmd(self, cmd):
        try:
            method = getattr(self, cmd[0])
        except AttributeError:
            print 'E: No such command: %s' % cmd
            return

        try:
            method(cmd[1:])
        except TypeError:
            print 'E: Wrong usage, try help to get how :)'
            return

    def grouplist(self, *args):
        grouplist = self._read_cache('_groups.dat')
        for g in grouplist:
            print g

        print 'Total: %s' % len(grouplist)

    def hostlist(self, *args):
        try:
            hostlist = self._read_cache(args[0][0]+'.dat')
        except IndexError:
            hostlist = []
            grouplist = self._read_cache('_groups.dat')
            for group in grouplist:
                for host in self._read_cache(group+'.dat'):
                    hostlist.append(host)

        for h in hostlist:
            print h

        print 'Total: %s' % len(hostlist)

    def p_exec(self, *args):
        group = args[0][0]
        cmd = ' '.join(args[0][1:])

        self._set_title('p_exec %s' % group)

        l = open(os.path.join(self.datadir, group+'.dat'))
        subprocess.call([
            'shmux',
            '-S', 'all',
            '-M', '50',
            '-c', cmd,
            '-'
        ], stdin=l)
        l.close()

    def reload(self, *args):
        groups = self.api.hostgroup.get(output='extend')
        grouplist = []
        for group in groups:
            grouplist.append(group['name'])
            hosts = self.api.host.get(output='extend',
                                         groupids=group['groupid'])
            hostlist = []
            for host in hosts:
                hostlist.append(host['host'])
            self._store_cache(group['name']+'.dat', hostlist)
        self._store_cache('_groups.dat', grouplist)

    def ssh(self, *args):
        subprocess.call(['ssh', args[0][0]])
