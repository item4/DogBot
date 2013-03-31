# -*- coding:utf-8 -*-

alias = []
handler = []

import sqlite3

def cmd_db(bot, line, args):
    if line.login != 'item4':
        bot.con.query(
            'PRIVMSG',
            line.target,
            u'멍멍! 관리자만 사용가능한 명령어입니다.'
        )
        return
    elif not args:
        bot.con.query(
            'PRIVMSG',
            line.target,
            u'멍멍?'
        )
        return

    conn = sqlite3.connect(bot.system.dbname)
    with conn:
        c = conn.cursor()

        c.execute(args)
        res = c.fetchall()
        for x in res:
            bot.con.query(
                'PRIVMSG',
                line.target,
                repr(x)
            )

        conn.commit()

