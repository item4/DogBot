# -*- coding:utf-8 -*-

alias = []
handler = []


import urllib

from sphinx.ext.intersphinx import read_inventory_v1, read_inventory_v2


def cmd_flask(bot, line, args):
    if not args:
        bot.con.query(
            'PRIVMSG',
            line.target,
            u'Flask API 문서 링크 | usage: ?flask resize'
        )
        return

    inv = get_inventory('http://flask.pocoo.org/docs/')
    i = 0
    for key in inv.iterkeys():
        for name in inv[key].iterkeys():
            print name,
            version, url = inv[key][name][1], inv[key][name][2]
            if name.lower().find(args) != -1:
                bot.con.query(
                    'PRIVMSG',
                    line.target,
                    '[%s] %s(%s) - %s' % (key, name, version, url)
                )
                i += 1
            if i > 2:
                break
        if i > 2:
            break

    if i == 0:
        bot.con.query(
            'PRIVMSG',
            line.target,
            u'멍멍! API 문서에서 검색어를 찾을 수 없어요!'
        )


def urljoin(*params):
    return '/'.join(params).replace('//', '/').replace(':/', '://')


def get_inventory(url):
    inv_url = urljoin(url, 'objects.inv')
    f = urllib.urlopen(inv_url)
    line = f.readline().rstrip().decode('utf-8')
    if line == '# Sphinx inventory version 1':
        invdata = read_inventory_v1(f, url, urljoin)
    elif line == '# Sphinx inventory version 2':
        invdata = read_inventory_v2(f, url, urljoin)
    else:
        raise ValueError(line)
    return invdata