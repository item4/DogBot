# -*- coding:utf-8 -*-
alias=[]

import time

def read_time(_time):
    day, _time = divmod(_time,86400)
    hour, _time = divmod(_time,3600)
    minute, second = divmod(_time,60)
    temp = []
    if day:
        temp.append(str(int(day))+u'일')
    if hour:
        temp.append(str(int(hour))+u'시간')
    if minute:
        temp.append(str(int(minute))+u'분')
    if second or (not day and not hour and not minute):
        temp.append(str(int(second))+u'초')

    return ' '.join(temp)

def cmd_uptime(bot, line, args):
    temp = time.time()
    bot.con.query(
        'PRIVMSG',
        line.target,
        u'봇 메인 시작으로부터 ' + read_time(temp - bot.system.start_time) + u' 경과'
    )
    bot.con.query(
        'PRIVMSG',
        line.target,
        u'봇 해당 오브젝트 시작으로부터 ' + read_time(temp - bot.start_time) + u' 경과'
    )