# -*- coding:utf-8 -*-

alias = []

def cmd_topic(bot, line, args):
    try:
        topic = bot.db['channel'][line.target]['topic']
    except KeyError:
        bot.con.query(
            'PRIVMSG',
            line.target,
            u'토픽이 없거나 추출할 수 없는 환경'
        )
    bot.con.query(
        'PRIVMSG',
        line.target,
        '%s: %s' % (line.target, topic)
    )