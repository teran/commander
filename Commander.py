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
        'ssh',
        'write_configuration'
    ]

    def __init__(self, datadir='.commander'):
        self.datadir = datadir

    def _check_dirs(self):
        if not os.path.exists(self.datadir):
            os.mkdir(self.datadir)

        if not os.path.exists(os.path.join(self.datadir, 'cache')):
            os.mkdir(os.path.join(self.datadir, 'cache'))

    def _set_title(self, title='cmd.py'):
        print "\033]0;%s\007" % title

    def _read_cache(self, file):
        self._check_dirs()

        f = open(os.path.join(self.datadir, 'cache', file), 'r')
        res = []
        for l in f.read().split("\n"):
            if l != '':
                res.append(l)
        f.close()
        return res

    def _update_settings(self, url='http://localhost',
                         login='admin', password='zabbix'):
        self.url = url or self.url
        self.login = login or self.login
        self.password = password or self.password

    def _write_cache(self, file, data):
        self._check_dirs()

        f = open(os.path.join(self.datadir, 'cache', file), 'w')
        f.write("\n".join(data)+"\n")
        f.close()

    @property
    def api(self):
        if self._api:
            return self._api

        self._api = pyzabbix.ZabbixAPI(self.url)
        self._api.login(self.login, self.password)

        return self._api

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
        grouplist = self._read_cache('_groups')
        for g in grouplist:
            print g

        print 'Total: %s' % len(grouplist)

    def hardware(self, *args):
        pass

    def hostlist(self, *args):
        try:
            hostlist = self._read_cache(args[0][0])
        except IndexError:
            hostlist = []
            grouplist = self._read_cache('_groups')
            for group in grouplist:
                for host in self._read_cache(group):
                    hostlist.append(host)

        for h in hostlist:
            print h

        print 'Total: %s' % len(hostlist)

    def p_exec(self, *args):
        group = args[0][0]
        cmd = ' '.join(args[0][1:])

        self._set_title('p_exec %s' % group)

        l = open(os.path.join(self.datadir, 'cache', group))
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
            self._write_cache(group['name'], hostlist)
        self._write_cache('_groups', grouplist)

    def read_configuration(self, *args):
        try:
            fp = open(os.path.join(self.datadir, 'settings.json'), 'r')
            configuration = json.loads(fp.read())
            fp.close()

            for k in configuration.keys():
                setattr(self, k, configuration[k])
        except IOError:
            pass

    def ssh(self, *args):
        subprocess.call(['ssh', args[0][0]])

    def write_configuration(self, *args):
        configuration = {
            'url': self.url,
            'login': self.login,
            'password': self.password
        }

        fp = open(os.path.join(self.datadir, 'settings.json'), 'w')
        fp.write(json.dumps(configuration, indent=4))
        fp.close()
