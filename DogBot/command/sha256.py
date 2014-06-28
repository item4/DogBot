# -*- coding:utf-8 -*-

alias = []
handler = []

import hashlib


def cmd_sha256(bot, line, args):
    if not args:
        bot.con.query(
            'PRIVMSG',
            line.target,
            u'입력받은 문자열의 sha256 인코딩 결과를 출력합니다. | usage: ?sha256 string'
        )
        return
    bot.con.query(
        'PRIVMSG',
        line.target,
        '[SHA256] %s = %s' % (args,hashlib.sha256(args.encode('u8')).hexdigest())
    )