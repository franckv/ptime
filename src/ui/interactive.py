import shlex
from cmd import Cmd

from command import Command

class Prompt(Cmd):
    def __init__(self):
        Cmd.__init__(self)
        self.prompt='>> '
        self.command = Command()

    def onecmd(self, line):
        cmd, args, line = self.parseline(line) 
        args = shlex.split(args)
        if cmd in self.command.list:
            nargs = int(self.command.list[cmd]['args'])

            if nargs != len(args):
                print('wrong number of arguments (expected %i)' % nargs)
            else:
                self.command.list[cmd]['exec'](self.command, *args)
        else:
            return Cmd.onecmd(self, line)

    def completenames(self, text, *ignored):
        result = Cmd.completenames(self, text, *ignored)

        for cmd in self.command.list:
            if cmd.startswith(text):
                result.append(cmd)

        return result

    def do_EOF(self, args):
        return True

    def do_quit(self, args):
        return True

