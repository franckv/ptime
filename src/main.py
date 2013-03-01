#!/usr/bin/env python2

import os, sys
from optparse import OptionParser
import logging

import config
from command import Command

if __name__ == '__main__':
    logging.basicConfig(
        level = logging.DEBUG,
        format="[%(levelname)-8s] %(asctime)s %(module)s:%(lineno)d %(message)s",
        datefmt="%H:%M:%S",
        filename = config.log_file,
        filemode = 'w'
    )

    logging.debug('Start')

    usage = 'Usage: %prog COMMAND [ARGS]'
    parser = OptionParser(usage)
    parser.add_option('--ui', dest='ui', default='console', help='interface: curses, gtk or console (default)')
    parser.add_option('-i', action='store_const', const='interactive', dest='ui', help='interactive mode')
    parser.add_option('-k', action='store_const', const='kivy', dest='ui', help='kivy ui')

    (options, args) = parser.parse_args()

    if options.ui == 'curses':
        ui.ncurses.run()
    elif options.ui == 'gtk':
        ui.gtkui.run()
    elif options.ui == 'kivy':
        from ui.kivyui import PTimeApp
        PTimeApp().run()
    elif options.ui == 'interactive':
        print('interactive mode')
        from ui.interactive import Prompt
        Prompt().cmdloop()
    else:
        if len(args) == 0:
            parser.error('missing command')

        cmd = args[0]
        command = Command()

        if not cmd in command.list:
            parser.error('invalid command')
        else:
            nargs = int(command.list[cmd]['args'])

            if nargs != len(args) - 1:
                parser.error('wrong number of arguments (expected %i)' % nargs)
            else:
                command.list[cmd]['exec'](command, *args[1:])

        command.close()

    logging.debug('Stop')
