import json
import os
import subprocess

import pyzabbix

class Commander():
    def __init__(self, api_url, login='admin', password='zabbix',
                 datadir='.commander'):
        self.api = pyzabbix.ZabbixAPI(api_url)
        self.api.login(login, password)
        self.datadir = datadir

    def _store_cache(self, file, data):
        f = open(os.path.join(self.datadir, file), 'w')
        f.write("\n".join(data)+"\n")
        f.close()

    def cmd(self, cmd):
        try:
            method = getattr(self, cmd[0])
        except AttributeError:
            return 'E: No such command: %s' % cmd

        try:
            return method(cmd[1:])
        except TypeError:
            return 'E: Wrong usage, try help to get how :)'

    def grouplist(self, *args):
        f = open(os.path.join(self.datadir, '_groups.dat'))
        for group in f.read().split("\n"):
            if group == '':
                continue
            print '  %s' % group
        f.close()
        return 'I: Grouplist finished'

    def p_exec(self, *args):
        group = args[0][0]
        cmd = ' '.join(args[0][1:])

        l = open(os.path.join(self.datadir, group+'.dat'))
        subprocess.call([
            'shmux',
            '-S', 'all',
            '-M', '50',
            '-c', cmd,
            '-'
        ], stdin=l)
        l.close()
        return 'I: Parallel execution ended'

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

        return 'I: Cache reloaded'

    def ssh(self, *args):
        print('I: Starting SSH session')
        subprocess.call(['ssh', args[0][0]])
        return 'I: SSH session ended'
