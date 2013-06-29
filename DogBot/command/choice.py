# -*- coding:utf-8 -*-

alias = [u'select',u'선택',u'골라']
handler = []

import random

def cmd_choice(bot, line, args):
    if not args:
        bot.con.query(
            'PRIVMSG',
            line.target,
            u'나열된 내용중에 하나를 선택해줍니다. | usgae: ?선택 a,b,c'
        )
        return

    if ',' in args:
        data = map(lambda x:x.strip(),args.split(','))
    elif '/' in args:
        data = map(lambda x:x.strip(),args.split('/'))
    elif '|' in args:
        data = map(lambda x:x.strip(),args.split('|'))
    else:
        data = args.split(' ')

    data = filter(None,data)

    if len(data) == 0:
        bot.con.query(
            'PRIVMSG',
            line.target,
            u'멍멍! 선택할 인자가 없습니다'
        )
    else:
        bot.con.query(
            'PRIVMSG',
            line.target,
            u'결과: %s' % random.choice(data)
        )