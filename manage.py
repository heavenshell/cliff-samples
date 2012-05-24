#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Cliff sample app
    ~~~~~~~~~~~~~~~~

    Cliff sample app.

    Class Simple, File, Files are ported from CliffDemo apps.

    see also.

    https://github.com/dreamhost/cliff/tree/master/demoapp/cliffdemo

    :copyright: (c) 2012 Shinya Ohyanagi, All rights reserved.
    :license: BSD, see LICENSE for more details.
"""
import os
import sys
import logging
from cliff.app import App
from cliff.commandmanager import CommandManager
from cliff.command import Command
from cliff.show import ShowOne
from cliff.lister import Lister


class Simple(Command):
    "A simple command that prints a message."

    log = logging.getLogger(__name__)

    def run(self, parsed_args):
        self.log.info('sending greeting')
        self.log.debug('debugging')
        self.app.stdout.write('hi!\n')


class File(ShowOne):
    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(File, self).get_parser(prog_name)
        parser.add_argument('filename', nargs='?', default='.')

        return parser

    def get_data(self, parsed_args):
        stat_data = os.stat(parsed_args.filename)
        columns = ('Name',
                   'Size',
                   'UID',
                   'GID',
                   'Modified Time',
                   )
        data = (parsed_args.filename,
                stat_data.st_size,
                stat_data.st_uid,
                stat_data.st_gid,
                stat_data.st_mtime,
                )
        return (columns, data)

class Files(Lister):
    """Show a list of files in the current directory.

    The file name and size are printed by default.
    """

    log = logging.getLogger(__name__)

    def get_data(self, parsed_args):
        return (('Name', 'Size'),
               ((n, os.stat(n).st_size) for n in os.listdir('.')))


class MyCommand(Command):
    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(MyCommand, self).get_parser(prog_name)
        parser.add_argument('arg', nargs='?', default=None)

        return parser

    def run(self, parsed_args):
        self.app.stdout.write(parsed_args.arg + "\n")


class GeneApp(App):
    log = logging.getLogger(__name__)

    def __init__(self):
        command = CommandManager('gene.app')
        super(GeneApp, self).__init__(
            description='sample app',
            version='0.1',
            command_manager=command,
        )
        commands = {
            'simple': Simple,
            'file': File,
            'files': Files,
            'sample': MyCommand
        }
        for k, v in commands.iteritems():
            command.add_command(k, v)


    def initialize_app(self, argv):
        self.log.debug('initialize_app')

    def prepare_to_run_command(self, cmd):
        self.log.debug('prepare_to_run_command %s', cmd.__class__.__name__)

    def clean_up(self, cmd, result, err):
        self.log.debug('clean_up %s', cmd.__class__.__name__)
        if err:
            self.log.debug('got an error: %s', err)


def main(argv=sys.argv[1:]):
    app = GeneApp()
    return app.run(argv)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
