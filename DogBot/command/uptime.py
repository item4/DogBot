# -*- coding:utf-8 -*-

alias = []
handler = []

import time

from DogBot.utility.time import read_time


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