# -*- coding: utf-8 -*-

alias = [u'환율']
handler = []

import urllib
import re

def cmd_exchange(bot, line, args):
    if not args:
        bot.con.query(
            'PRIVMSG',
            line.target,
            u'환율 계산기입니다. | usage: ?환율 100$ | ?환율 100 엔 | ?환율 100 USD KRW'
        )
        return

    data = args.upper().split(' ')

    shortcut = {
        '$':'USD','KRW':'WON','\\':'WON',u'원':'WON',
        u'엔':'JPY100','JPY':'JPY100','IDR':'IDR100',
        'VND':'VND100',u'달러':'USD',u'유로':'EUR'
    }

    for x in shortcut:
        if data[0].endswith(x):
            data[0] = data[0][:-len(x)]
            data.append(x)
            break

    size = len(data)
    money = float(data[0])

    if size == 2:
        temp = shortcut.get(data[1])
        ex_from = temp if temp else data[1]
        ex_to = 'WON'
    elif size == 3:
        temp = shortcut.get(data[1])
        ex_from = temp if temp else data[1]
        temp = shortcut.get(data[2])
        ex_to = temp if temp else data[2]
    else:
        bot.con.query(
            'PRIVMSG',
            line.target,
            u'멍멍! 인자 개수가 이상해요!'
        )
        return

    data = urllib.urlopen('http://finance.daum.net/exchange/exchangeMain.daum').read().decode('utf8')

    from_data = re.search(r"""ex\[\d+\] = '%s';ex_rate\[\d+\] = "(.+?)";country\[\d+\] = '(.+?)'; k_ex\[\d+\] = '(.+?)';full_k_ex\[\d+\] = '.+?';""" % ex_from,data)
    to_data = re.search(r"""ex\[\d+\] = '%s';ex_rate\[\d+\] = "(.+?)";country\[\d+\] = '(.+?)'; k_ex\[\d+\] = '(.+?)';full_k_ex\[\d+\] = '.+?';""" % ex_to,data)

    if not from_data or not to_data:
        bot.con.query(
            'PRIVMSG',
            line.target,
            u'멍멍! 해당 국가를 찾을 수 없어요!'
        )
        return

    from_rate = float(from_data.group(1))
    to_rate = float(to_data.group(1))

    exchange = money/to_rate*from_rate

    bot.con.query(
        'PRIVMSG',
        line.target,
        u'%.2f %s %s = %.2f %s %s' %
         (money,from_data.group(2),from_data.group(3),
        exchange,to_data.group(2),to_data.group(3))
    )
