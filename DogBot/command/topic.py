# -*- coding:utf-8 -*-

alias = []
handler = []


def cmd_topic(bot, line, args):
    try:
        topic = bot.db['channel'][line.target]['topic']
    except KeyError:
        bot.con.query(
            'PRIVMSG',
            line.target,
            u'멍멍! 토픽이 없거나 추출할 수 없는 환경이에요!'
        )
        return
    bot.con.query(
        'PRIVMSG',
        line.target,
        '%s: %s' % (line.target, topic)
    )