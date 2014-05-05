# -*- coding:utf-8 -*-

alias = []
handler = []

import hashlib


def cmd_sha384(bot, line, args):
    if not args:
        bot.con.query(
            'PRIVMSG',
            line.target,
            u'입력받은 문자열의 sha384 인코딩 결과를 출력합니다. | usage: ?sha384 string'
        )
        return
    bot.con.query(
        'PRIVMSG',
        line.target,
        '[SHA384] %s = %s' % (args,hashlib.sha384(args).hexdigest())
    )