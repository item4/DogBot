# -*- coding:utf-8 -*-

alias = [u'사전']

import re
import urllib
import time

def cmd_dic(bot, line, args):
    if not args:
        return

    if ' ' in args:
        keyword, num = args.split(' ',1)
        try:
            num = int(num) - 1
        except ValueError:
            num = 0
        if num < 0:
            num = 0
    else:
        keyword = args
        num = 0


    data = urllib.urlopen('http://dic.daum.net/search.do?%s' % \
                          urllib.urlencode({'q':keyword.encode('utf8')})).read()

    data = data.decode('utf8').replace('\r','').replace('\n','')

    data = re.findall('<strong[^>]+>\s*<a href="([^>]+)" class="link_txt">', data)

    if not data:
        bot.con.query(
            'PRIVMSG',
            line.target,
            u'검색 결과가 없습니다.'
        )
        return

    try:
        url = 'http://dic.daum.net' + data[num]
    except IndexError:
        bot.con.query(
            'PRIVMSG',
            line.target,
            u'검색 범위 초과. (최대 %d까지)' % len(data)
        )
        return

    data = urllib.urlopen(url).read()

    data = data.decode('utf8','ignore').replace('\r','').replace('\n','')

    data = re.findall('(?:<span[^>]+>(.+?)</span>\s*)?<p class="txt_sense( no_num)?">(.+?)</p>', data)

    print num, len(data)

    if data:
        res = ''
        i = 1
        for n, nonum, desc in data:
            desc = re.sub('</?[^>]+>', '', desc)
            if n or nonum:
                res += '%d. ' % i
                i += 1
                res += desc + ' / '
            else:
                res += desc + ' '

            if len(res) > 100:
                cut = -3 if res.endswith(' / ') else -1
                bot.con.query(
                    'PRIVMSG',
                    line.target,
                    res[:cut]
                )
                res = ''
        if res:
            cut = -3 if res.endswith(' / ') else -1
            bot.con.query(
                'PRIVMSG',
                line.target,
                res[:cut]
            )


            time.sleep(.4)
    else:
        bot.con.query(
            'PRIVMSG',
            line.target,
            u'파싱할 수 없습니다. 관리자에게 해당 주소를 제보해주세요 : ' + url
        )