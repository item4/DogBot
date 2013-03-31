# -*- coding: utf-8 -*-

alias = []
handler = []

import base64

def cmd_b64d(bot, line, args):
    if not args:
        bot.con.query(
            'PRIVMSG',
            line.target,
            u'Base64 인코딩된 문자열을 디코드합니다. | usage: ?b64d 6rCA64KY64uk'
        )
        return

    data = base64.b64decode(args).decode('utf8').splitlines()
    check = 0

    for x in data:
        if check == 0:
            bot.con.query(
                'PRIVMSG',
                line.target,
                u'%s: %s' % (args, x)
            )
            check = 1
        else:
            bot.con.query(
                'PRIVMSG',
                line.target,
                u'%s' % x
            )

def main():
    pass

if __name__ == '__main__':
    main()
