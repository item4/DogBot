# -*- coding:utf-8 -*-

alias = []
handler = []

import json
import urllib


def cmd_dns(bot, line, args):
    if not args:
        bot.con.query(
            'PRIVMSG',
            line.target,
            u'해당 도메인이 주요 DNS 서버에 어느 IP로 연결되어있는지 조회합니다. | usage: ?dns naver.com | ?dns -168.126.63.1 naver.com (DNS 서버 지정)'
        )
        return

    server_list = [
                ('168.126.63.1','KT'),
                ('168.126.63.2','KT'),
                ('210.220.163.82','SK'),
                ('219.250.36.130','SK'),
                ('164.124.101.2','Dacom'),
                ('203.248.252.2','Dacom'),
                ('164.124.107.9','Powercom'),
                ('203.248.252.2','Powercom'),
                ('210.181.1.24','Dreamline'),
                ('210.181.4.25','Dreamline'),
                ('8.8.8.8','Google'),
                ('8.8.4.4','Google'),
                ('208.67.222.222','OpenDNS'),
                ('208.67.220.220','OpenDNS')
                ]

    if args[0] == '-':
        temp, args = args[1:].split(' ',2)
        server_list[:] = [(temp, 'User input')]

    if args.startswith('http://'):
        args = args[7:]
    elif args.startswith('https://'):
        args = args[8:]

    args = args.replace('/','')

    res = []

    bot.con.query(
        'PRIVMSG',
        line.target,
        u'Domain %s에 대하여 DNS Server 등록 상태를 검색합니다. 잠시 시간이 걸릴 수 있습니다.' % args
    )

    for server, name in server_list:
        data = urllib.urlopen('http://checkdnskr.appspot.com/api/lookup?%s' % urllib.urlencode({'domain':args.encode('u8'),'ip':server})).read()
        data = data.decode('u8')

        try:
            ip = json.loads(data)['A']
            if ', ' in ip:
                bot.con.query(
                    'PRIVMSG',
                    line.target,
                    u'멍멍! 너무 길어요! 다음 주소로 가서 직접 보세요. - http://checkdnskr.appspot.com/?domain=%s' % args
                )
                break
            res.append(u'%s(%s) → %s' % (name, server, ip))
        except:
            res.append(u'%s(%s) → Error' % (name, server))
    else:
        for i in xrange(0,len(server_list),4):
            bot.con.query(
                'PRIVMSG',
                line.target,
                ' | '.join(res[i:i+4])
            )