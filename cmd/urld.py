# -*- coding: utf-8 -*-

alias = []

import urllib

def cmd_urld(bot, line, args):
    if not args:
        bot.con.query(
            'PRIVMSG',
            line.target,
            u'URL 인코딩된 문자열을 해독합니다 | usage: ?urld %EA%B0%80%EB%82%98%EB%8B%A4'
        )
        return

    data = urllib.unquote(args)

    print repr(data)

    data = data.encode('latin-1').decode('utf8')

    #print repr(data)

    bot.con.query(
        'PRIVMSG',
        line.target,
        u'%s: %s' % (args, data)
    )



def main():
    pass

if __name__ == '__main__':
    main()
