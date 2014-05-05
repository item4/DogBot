# -*- coding: utf-8 -*-

alias = ['>']
handler = []

from urllib import urlencode
from urllib2 import urlopen, URLError, HTTPError
from contextlib import closing
import threading
import hashlib
import traceback

try:
    import websocket
except ImportError:
    websocket = None

REQUEST_URL     = "https://ecmaxp.pe.kr/api/_export/irc"
DELAY_REQUEST_URL = "wss://ecmaxp.pe.kr/api/_export/irc/wait/"

AUTH_TOKEN = "5961a3a8ab0192813db1d47f21353455"
MAXINUM_LINE_LENGTH = 450
MAXIMUM_WAIT_CHANCE = 2
MAXIMUM_SPEAK_CHANCE = 4


def build_ctx(bot, line, args):
    ctx = dict(
        token=AUTH_TOKEN,
        nick=line.nick,
        ident=hashlib.sha256(line.ip).hexdigest()[::4],
        server=bot.server,
        line=args.encode('u8', 'replace'),
        method='item4/DogBot',
    )

    return ctx


def request(bot, line, args):
    ctx = build_ctx(bot, line, args)

    with closing(urlopen(REQUEST_URL, urlencode(ctx))) as res:
        return res.read(4096)


def delay_request(bot, line, key):
    ws = websocket.create_connection(DELAY_REQUEST_URL + key)
    try:
        return ws.recv().decode('u8')
    finally:
        ws.close()


def cmd_exa(bot, line, args):
    if not args:
        bot.con.query(
            'PRIVMSG',
            line.target,
            u'EcmaXp의 API 모음집 연동 명령어 입니다. | usage: ?> help()'
        )
        return

    try:
        data = request(bot, line, args)
    except (URLError, HTTPError), e:
        emsg = traceback.format_exception_only(type(e), e)[-1]
        bot.con.query(
            'PRIVMSG',
            line.target,
            u'[!:INTERNAL] %s' % (emsg,)
        )
        return

    speaked = False
    speakcount = MAXIMUM_SPEAK_CHANCE
    waitcount = MAXIMUM_WAIT_CHANCE

    lines = data.decode("u8", "replace").splitlines()
    while lines:
        ret = lines.pop(0)
        target, mode = line.target, "PRIVMSG"

        ret = ret.rstrip()
        cmd, sep, arg = ret.partition(" ")
        if cmd.startswith("[#") and cmd.endswith("]"):
            if cmd == "[#:DELAY]":
                if waitcount:
                    waitcount -= 1
                    if not websocket:
                        ret = "[!:INTERNAL] DELAY Call Failed (ImportError: No module named websocket)"
                    else:
                        try:
                            ret = delay_request(bot, line, arg)
                        except websocket.WebSocketException, e:
                            emsg = traceback.format_exception_only(type(e), e)[-1]
                            bot.con.query(
                                'PRIVMSG',
                                line.target,
                                u'[!:INTERNAL] %s' % (emsg,)
                            )
                            return
                else:
                    ret = "[!:INTERNAL] DELAY Call Failed (No more chance)"

                lines.append(ret)
                continue
            elif cmd == "[#:NOTICE]":
                target, mode = line.nick, "NOTICE"
                ret = arg
            else:
                continue

        ret = ret[:MAXINUM_LINE_LENGTH]
        if ret:
            speaked = True
            bot.con.query(
                mode,
                target,
                ret,
            )

            speakcount -= 1
            if not speakcount:
                break

    if not speaked:
        bot.con.query(
            'PRIVMSG',
            line.target,
            u'[@] Empty Result.',
        )
