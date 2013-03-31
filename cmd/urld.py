# -*- coding: utf-8 -*-

alias = []
handler = []

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

    data = data.encode('latin-1')

    try:
        data = data.decode('utf8')
        encoding = 'UTF-8'
    except:
        try:
            data = data.decode('cp949')
            encoding = 'CP949'
        except:
            bot.con.query(
                'PRIVMSG',
                line.target,
                u'멍멍! 인코딩 파악에 실패했습니다.'
            )

    #print repr(data)

    bot.con.query(
        'PRIVMSG',
        line.target,
        u'[%s] %s: %s' % (encoding, args, data)
    )



def main():
    pass

if __name__ == '__main__':
    main()
