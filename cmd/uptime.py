# -*- coding:utf-8 -*-
alias=[]

import time

def cmd_uptime(bot, line, args):
    uptime = time.time() - bot.start
    day, uptime = divmod(uptime,86400)
    hour, uptime = divmod(uptime,3600)
    minute, second = divmod(uptime,60)
    temp = []
    if day:
        temp.append(str(int(day))+u'일')
    if hour:
        temp.append(str(int(hour))+u'시간')
    if minute:
        temp.append(str(int(minute))+u'분')
    if second or (not day and not hour and not minute):
        temp.append(str(int(second))+u'초')
    bot.con.query(
        'PRIVMSG',
        line.target,
        u'봇 시작으로부터 ' + ' '.join(temp) + u' 경과'
    )