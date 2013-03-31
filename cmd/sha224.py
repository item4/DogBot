# -*- coding:utf-8 -*-

alias = []
handler = []

import hashlib

def cmd_sha224(bot, line, args):
    if not args:
        bot.con.query(
            'PRIVMSG',
            line.target,
            u'입력받은 문자열의 sha224 인코딩 결과를 출력합니다. | usage: ?sha224 string'
        )
        return
    bot.con.query(
        'PRIVMSG',
        line.target,
        '[SHA224] %s = %s' % (args,hashlib.sha224(args).hexdigest())
    )

def main():
    pass

if __name__ == '__main__':
    main()
