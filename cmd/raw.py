# -*- coding:utf-8 -*-

alias=[]

def cmd_raw(bot, line, args):
    if line.login != 'item4':
        return
    temp = args.split(' ',2)
    bot.con.query(
        temp[0],
        temp[1],
        temp[2]
    )