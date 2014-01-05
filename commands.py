# -*- coding: utf-8 -*-
from oyoyo import helpers
import sys, traceback
import requests

def say(nick, channel, arguments, sender, config, irc):
    return ' '.join(arguments)

def at(nick, channel, arguments, sender, config, irc):
    try:
        r = requests.get(config.get('at', 'spaceapi_url'))
        if callable(r.json):
            j = r.json()
        else:
            j = r.json

        msg = []
        msg.append(u"Hackerspace jest " + (u"otwarty" if j['state']['open'] else u"zamknięty"))

        any_lights = False
        lights_str = []
        for room, state in j['sensors']['ext_lights'].items():
            if state == True:
                any_lights = True
                lights_str.append(room)

        if any_lights:
            msg.append(u"Światło zaświecone w: " + ', '.join(lights_str))
        else:
            msg.append(u"Swiatła pogaszone")

        helpers.msg(irc.client, channel, nick + ': ' + ', '.join(msg))

    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_exception(exc_type, exc_value, exc_traceback, limit=2, file=sys.stdout)
        helpers.msg(irc.client, channel, nick + u": Spaceapi… nie działa.")

    try:
        r = requests.get(config.get('at', 'whois_url'))
        if callable(r.json):
            j = r.json()
        else:
            j = r.json
        l = len(j['users'])

        if l == 0:
            msg = u"Żywego ducha nie uświadczysz…"
        else:
            msg = u"%s urządzeń, w tym białkowe: %s" % (l+j['total_devices_count'], ', '.join(j['users']))

        helpers.msg(irc.client, channel, nick + u": " + msg)

    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_exception(exc_type, exc_value, exc_traceback, limit=2, file=sys.stdout)
        helpers.msg(irc.client, channel, nick + u": Whois… nie działa.")
