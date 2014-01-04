#!/usr/bin/python2
# -*- coding: utf-8 -*-
from oyoyo.client import IRCClient
from oyoyo.cmdhandler import DefaultCommandHandler
from oyoyo import helpers
import logging
import commands
import socket
import time
import re

class irc_config:
    server = 'chat.freenode.net'
    port = 6667

    nick = 'GLaDZIOS'

    channels = ['#hackerspace-krk']


logging.basicConfig(level=logging.DEBUG)

is_command_pattern = re.compile('\![a-zA-Z0-9]+')
def iscommand(text):
    return True if is_command_pattern.match(text) else False

class IRCHandler(DefaultCommandHandler):
    def endofmotd(self, server, target, text):
        for channel in irc_config.channels:
            helpers.join(self.client, channel)
    def nicknameinuse(self, server, wtf, nick, reason):
        helpers.nick(self.client, nick+'_')
    def privmsg(self, nick, chan, msg):
        print "%s in %s said: %s" % (nick, chan, msg)
        if msg[0] == '!':
            s = msg.split(' ')
            if iscommand(s[0]):
                command = s[0][1:]
                arguments = s[1:]
                sender = nick.split('!')[0]

                if hasattr(commands, command) and callable(getattr(commands, command)):
                    try:
                        response = getattr(commands, command)(nick, chan, arguments)
                    except:
                        response = 'Coś poszło nie tak…'

                    helpers.msg(self.client, chan, sender+": "+response)

cli = IRCClient(IRCHandler, host=irc_config.server, port=irc_config.port, nick=irc_config.nick)

try:
    conn = cli.connect()
except:
    time.sleep(10)
    conn = cli.connect()

while True:
    try:
        conn.next()
    except KeyboardInterrupt:
        conn.close()
        quit()
    except socket.error as e:
        print "Socket error (%d) reconnecting after delay" % e
        time.sleep(10)
        print "Now"
        conn = cli.connect()
