#!/usr/bin/python2
# -*- coding: utf-8 -*-
from oyoyo.client import IRCClient, IRCApp
from oyoyo.cmdhandler import DefaultCommandHandler
from oyoyo import helpers
import ConfigParser
import logging
import socket
import time
import re
import os
import commands
import sys, traceback

config = ConfigParser.ConfigParser()
config.read(os.path.join(os.path.dirname(os.path.realpath(__file__)),'settings.ini'))

logging.basicConfig(level=logging.DEBUG)

is_command_pattern = re.compile('\![a-zA-Z0-9]+')

class IRCHandler(DefaultCommandHandler):
    def endofmotd(self, server, target, text):
        for channel in config.get('irc', 'channels').split(','):
            helpers.join(self.client, channel)

    def nicknameinuse(self, server, wtf, nick, reason):
        helpers.nick(self.client, nick+'_')

    def privmsg(self, sender, chan, msg):
        if msg[0] == '!':
            s = msg.split(' ')
            if is_command_pattern.match(s[0]):
                command = s[0][1:]
                arguments = s[1:]
                nick = sender.split('!')[0]

                if hasattr(commands, command) and callable(getattr(commands, command)):
                    try:
                        response = getattr(commands, command)(nick, chan, arguments, sender, config, self)
                    except:
                        exc_type, exc_value, exc_traceback = sys.exc_info()
                        traceback.print_exception(exc_type, exc_value, exc_traceback, limit=2, file=sys.stdout)
                        response = 'Coś poszło nie tak…'

                    if response is not None:
                        helpers.msg(self.client, chan, nick+": "+response)

cli = IRCClient(IRCHandler, host=config.get('irc', 'server'), port=config.getint('irc', 'port'), nick=config.get('irc', 'nick'))

app = IRCApp()
app.addClient( cli )

try:
    app.run()
except KeyboardInterrupt:
    quit()
