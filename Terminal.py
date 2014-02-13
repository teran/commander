import os
import re
import readline

import Commander


class Completer(object):
    def __init__(self):
        self.RE_SPACE = re.compile('.*\s+$', re.M)
        self.c = Commander.Commander()
        self.COMMANDS = self.c.commands

    def complete_hostlist(self, args):
        groups = self.c._read_cache('_groups.dat')
        if args[0] == '':
            return groups

        res = []
        for group in groups:
            if group.startswith(args[0]):
                res.append(group)

        return res

    def complete_p_exec(self, args):
        return self.complete_hostlist(args)

    def complete_ssh(self, args):
        res = []
        grouplist = self.c._read_cache('_groups.dat')
        for group in grouplist:
            for host in self.c._read_cache(group + '.dat'):
                if host.startswith(args[0]):
                    res.append(host)

        return res

    def complete(self, text, state):
        buffer = readline.get_line_buffer()
        line = readline.get_line_buffer().split()
        if not line:
            return [c + ' ' for c in self.COMMANDS][state]
        if self.RE_SPACE.match(buffer):
            line.append('')
        cmd = line[0].strip()
        if cmd in self.COMMANDS:
            impl = getattr(self, 'complete_%s' % cmd)
            args = line[1:]
            if args:
                return (impl(args) + [None])[state]
            return [cmd + ' '][state]
        results = [c + ' ' for c in self.COMMANDS if c.startswith(cmd)] + [
            None]
        return results[state]
