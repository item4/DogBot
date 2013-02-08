# -*- coding:utf-8 -*-

alias=[]

def cmd_raw(bot, line, args):
    if line.login != 'item4':
        bot.con.query(
            'PRIVMSG',
            line.target,
            u'멍멍! 관리자만 사용가능한 명령어입니다.'
        )
        return
    temp = args.split(' ',2)
    bot.con.query(*temp)