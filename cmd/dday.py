# -*- coding: utf-8 -*-

alias = []

import time
import sqlite3

def cmd_dday(bot, line, args):
    if not args:
        bot.con.query(
            'PRIVMSG',
            line.target,
            u'해당 날짜까지 며칠 남았는지, 혹은 며칠 지났는지 계산합니다. ?기억 기능과 연동됩니다. 기억과 날짜가 겹칠경우 앞에 @를 붙여주세요. | usage: ?dday 20131231 | ?dday 지구멸망'
        )
        return


    if args[0] == '@':
        args = args[1:]
    else:
        conn = sqlite3.connect(bot.system.dbname)
        with conn:
            c = conn.cursor()
            c.execute('select `content` from `memo` where `keyword`=? limit 1;',(args,))

            data = c.fetchone()

            if data is not None:
                args = data[0]

    try:
        day = time.strptime(args,'%Y%m%d')
        dday = time.mktime(day)
    except:
        bot.con.query(
            'PRIVMSG',
            line.target,
            u'멍멍! 날짜가 올바른 형식이 아닙니다.'
        )
        return

    today = time.localtime()
    dday -= time.mktime((today[0],today[1],today[2],0,0,0,today[6],today[7],today[8]))

    if dday > 0:
        bot.con.query(
            'PRIVMSG',
            line.target,
            u'{0}까지 {1:,}일 남았습니다.'.format(time.strftime('%Y-%m-%d',day),int(dday//86400))
        )
    else:
        bot.con.query(
            'PRIVMSG',
            line.target,
            u'{0}로부터 {1:,}일 지났습니다.'.format(time.strftime('%Y-%m-%d',day),int(-dday//86400))
        )