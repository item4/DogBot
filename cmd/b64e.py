# -*- coding: utf-8 -*-

alias = []

import base64

def cmd_b64e(bot, line, args):
    if not args:
        bot.con.query(
            'PRIVMSG',
            line.target,
            u'입력받은 문자열을 base64 인코딩합니다. | usage: ?b64e 가나다'
        )
        return

    bot.con.query(
        'PRIVMSG',
        line.target,
        u'%s: %s' % (args,base64.b64encode(args.encode('utf8')))
    )

def main():
    pass

if __name__ == '__main__':
    main()
