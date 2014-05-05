# -*- coding:utf-8 -*-

alias = [u'마크서버']
handler = []

import socket
import re


def cmd_mcs(bot, line, args):
    if not args:
        args='mc.sjkoon.com'

    if args.find(':') > 0:
        server, port = args.split(':',1)
    else:
        server = args
        port = 25565

    try:
        s = socket.socket()
        s.settimeout(5)
        s.connect((server,port))
    except:
        bot.con.query(
            'PRIVMSG',
            line.target,
            '[%s] Offline' % args
        )
    else:

        s.send('\xfe\x01')

        data = s.recv(256)

        if data[0] != '\xff':
            bot.con.query(
                'PRIVMSG',
                line.target,
                '[%s] Offline' % args
            )
        else:
            data = map(lambda x:x.replace('\x00',''),data[3:].split('\x00\x00'))
            data[3] = re.sub(r'\xa7.','',data[3]).replace(r'\xa7','')
            data = map(lambda x:x.decode('u8','ignore'),data)

            res='[%s/%s] Online - %s' % (args,data[2],data[3])
            if len(data) == 6:
                res += ' (%s/%s)' % (data[4],data[5])
            bot.con.query(
                'PRIVMSG',
                line.target,
                res
            )