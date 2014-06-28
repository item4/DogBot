# -*- coding:utf-8 -*-

alias = []
handler = []

import hashlib


def cmd_md5(bot, line, args):
    if not args:
        bot.con.query(
            'PRIVMSG',
            line.target,
            u'입력받은 문자열의 md5 인코딩 결과를 출력합니다. | usage: ?md5 string'
        )
        return
    bot.con.query(
        'PRIVMSG',
        line.target,
        '[MD5] %s = %s' % (args,hashlib.md5(args.encode('u8')).hexdigest())
    )