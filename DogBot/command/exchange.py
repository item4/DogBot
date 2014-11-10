# -*- coding: utf-8 -*-

alias = [u'환율', 'money']
handler = []

import json
import re
import urllib


exchange_table_pattern = re.compile('var\s*exchangeData\s*=\s*\[(.+?)\];', re.S)


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
        '$': 'USD', '\\': 'KRW', u'원': 'KRW',
        u'엔': 'JPY', 'JPY100': 'JPY', 'IDR100': 'IDR',
        'VND100': 'VND' ,u'달러': 'USD', u'유로': 'EUR'
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
        ex_to = 'KRW'
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

    data = urllib.urlopen('http://finance.daum.net/exchange/exchangeMain.daum').read().decode('cp949')

    exchange_table = json.loads('[' + exchange_table_pattern.search(data).group(1) + ']')
    from_data = None
    to_data = None
    for e in exchange_table:
        if from_data is None and ex_from == e[1]:
            from_data = e

        if to_data is None and ex_to == e[1]:
            to_data = e

        if from_data and to_data:
            break

    if from_data is None or to_data is None:
        bot.con.query(
            'PRIVMSG',
            line.target,
            u'멍멍! 해당 국가를 찾을 수 없어요!'
        )
        return

    from_rate = float(from_data[3]) or 1.
    to_rate = float(to_data[3]) or 1.

    if from_data[1] in ['JPY', 'IDR', 'VND']:
        from_rate /= 100.
    if to_data[1] in ['JPY', 'IDR', 'VND']:
        to_rate /= 100.

    exchange = money/to_rate*from_rate

    bot.con.query(
        'PRIVMSG',
        line.target,
        u'%.2f %s %s = %.2f %s %s' %
         (money,from_data[0],from_data[1],
          exchange,to_data[0],to_data[1])
    )
