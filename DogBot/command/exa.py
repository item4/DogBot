# -*- coding:utf-8 -*-
from __future__ import print_function

alias = ["?"]
handler = []

from urllib import urlencode
from urllib2 import urlopen, URLError, HTTPError
from contextlib import closing
import hashlib

BASE_URL = "https://ecmaxp.pe.kr/api/_export/irc"
AUTH_TOKEN = "5961a3a8ab0192813db1d47f21353455"
MAXINUM_LINE_LENGTH = 450
MAXIMUM_SPEAK_CHANCE = 3

def cmd_exa(bot, line, args):
    if not args:
        bot.con.query(
            'PRIVMSG',
            line.target,
            u'Usage: >? <Function Name>(<Arguments>, <Keyword Arguments>)'
        )
        return

    ctx = dict(
        token = AUTH_TOKEN,
        nick = line.nick,
        ident = hashlib.sha256(line.ip).hexdigest()[::4],
        server = bot.host,
        line = args,
        method = "item4/DogBot",
    )

    try:
        with closing(urlopen(BASE_URL, urlencode(ctx))) as res:
            data = res.read(4096)
    except (URLError, HTTPError), e:
        bot.con.query(
            'PRIVMSG',
            line.target,
            u'[!:INTERNAL] %s' % (e,)
        )
        return

    count = maxcount = MAXIMUM_SPEAK_CHANCE
    for ret in data.decode("utf-8", "replace").splitlines():
        ret = ret.rstrip()
        ret = ret[:MAXINUM_LINE_LENGTH]
        if ret:
            bot.con.query(
                'PRIVMSG',
                line.target,
                ret,
            )
            count -= 1
            if not count:
                break

    if maxcount == count:
        bot.con.query(
            'PRIVMSG',
            line.target,
            u'[@] Empty result.',
        )
