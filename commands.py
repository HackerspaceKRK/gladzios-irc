# -*- coding: utf-8 -*-
def say(sender, channel, arguments):
    return ' '.join(arguments)

def at(sender, channel, arguments):
    import requests
    try:
        r = requests.get('http://hskrk-whois.tojestto.pl/whois') # http://hskrk.pl/whois 301 http://hskrk-whois.tojestto.pl/whois
    except:
        return u'Błąd pobierania danych!'

    if callable(r.json):
        j = r.json()
    else:
        j = r.json
    l = len(j['users'])

    if l == 0:
        return u'Żywego ducha nie uświadczysz…'
    return u'%s urządzeń, w tym białkowe: %s' % (l+j['total_devices_count'], ', '.join(j['users']))
