# -*- coding:utf-8 -*-

alias = [u'사전']
handler = []

import re
import urllib
import time

def cmd_dic(bot, line, args):
    if not args:
        bot.con.query(
            'PRIVMSG',
            line.target,
            u'다음 사전에서 검색하여 결과를 보여줍니다 | usage: ?dic 단어'
        )
        return

    if ' ' in args:
        temp = args.split(' ')
        keyword = ' '.join(temp[:-1])
        num = temp[-1]
        try:
            num = int(num) - 1
        except ValueError:
            keyword = args
            num = 0
        if num < 0:
            keyword = args
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
        if url.find('view_example.do') > 0:
            url = url.replace('view_example.do','view.do')
    except IndexError:
        bot.con.query(
            'PRIVMSG',
            line.target,
            u'검색 범위 초과. (최대 %d까지)' % len(data)
        )
        return

    data = urllib.urlopen(url).read()

    data = data.decode('utf8','ignore').replace('\r','').replace('\n','')

    data = re.findall('(?:<h4[^>]+>([^<]+)</h4>\s*<div[^>]+>\s*<div[^>]+>\s*)?(?:<span[^>]+>([^<]+)</span>\s*)?<p class="txt_sense( no_num)?">(.+?)</p>', data)

    if data:
        res = ''
        i = 1
        lines = 0
        for wordtype, n, nonum, desc in data:
            desc = re.sub('</?[^>]+>', '', desc)
            if wordtype:
                res += wordtype + ' '
                i = 1
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
                lines += 1
                if lines > 4:
                    bot.con.query(
                        'PRIVMSG',
                        line.target,
                        u'멍멍! 너무 길어요. 직접 가서 보세요 - ' + url
                    )
                    return
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