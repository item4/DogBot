# -*- coding: utf-8 -*-

alias = []
handler = []

import urllib
import urlparse


def cmd_urle(bot, line, args):
    if not args:
        bot.con.query(
            'PRIVMSG',
            line.target,
            u'입력받은 주소를 인코딩합니다. | usage: ?urle http://item4.net/가나다'
        )
        return

    data = urlparse.urlparse(args)

    if data.netloc:
        new_data = [data.scheme,
                    data.netloc,
                    urllib.quote(data.path.encode('u8')),
                    data.params]

        if data.query:
            temp = []
            for x in data.query.split('&'):
                t = x.split('=',1)
                if len(t) == 2:
                    temp.append(urllib.quote(t[0].encode('u8')) + '=' + urllib.quote(t[1].encode('u8')))
                else:
                    temp.append(urllib.quote(t[0].encode('u8')))

            new_data.append('&'.join(temp))
        else:
            new_data.append('')

        new_data.append(data.fragment)

        data = urlparse.urlunparse(new_data)

    else:
        data = urllib.quote(args.encode('u8'))

    bot.con.query(
        'PRIVMSG',
        line.target,
        u'%s: %s' % (args, data)
    )

def main():
    pass

if __name__ == '__main__':
    main()
