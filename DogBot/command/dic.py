# -*- coding:utf-8 -*-

alias = ['d',u'사전']
handler = []

import re
import urllib
import time


def cmd_dic(bot, line, args):
    if not args:
        bot.con.query(
            'PRIVMSG',
            line.target,
            u'다음 사전에서 검색하여 결과를 보여줍니다 | usage: ?dic 단어 | ?dic -dic ke 단어 (ke:한영, ek:영한, kk:국어, ee:영영, hh:한자, kj:한일, kc:한중)'
        )
        return

    if ' ' in args:
        if args.startswith('-dic'):
            dic, args = args[5:].split(' ', 1)
        else:
            dic = None
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
    else:
        dic = None
        keyword = args
        num = 0

    data = urllib.urlopen('http://dic.daum.net/search.do?%s' % \
                          urllib.urlencode({'q': keyword.encode('utf8')})).read()

    data = data.decode('utf8').replace('\r', '').replace('\n', '')

    data = re.findall('<strong[^>]+>\s*<a href="([^>]+)" class="\s*link_txt\s*"\s*>', data)

    if dic:
        data = filter(lambda x: '=' + dic + 'w' in x, data)

    if not data:
        bot.con.query(
            'PRIVMSG',
            line.target,
            u'멍멍! 검색 결과가 없습니다.'
        )
        return

    try:
        url = 'http://dic.daum.net' + data[num]
        if url.find('view_example.do') > 0:
            url = url.replace('view_example.do', 'view.do')
    except IndexError:
        bot.con.query(
            'PRIVMSG',
            line.target,
            u'멍멍! 검색 범위를 초과했어요. 최대 %d까지 가능해요.' % len(data)
        )
        return

    data = urllib.urlopen(url).read()

    data = data.decode('u8', 'ignore').replace('\r', '').replace('\n', '')

    try:
        keyword = re.search('<strong class="tit"><span class="inner_tit">(.+?)</span>.+', data).group(1)
    except:
        keyword = '?'

    temp = url[40:42]
    
    dic_category_list = {'ek':u'영한','ke':u'한영','ee':u'영영','kk':u'국어',
                         'hh':u'한자','kj':u'한일','kc':u'한중','kh':u'힌디',
                         'kt':u'터키',
                         'kr':u'러시아','kd':u'프랑스','kv':u'베트남',
                         'ki':u'이탈리아'
                         }
    dic_category = dic_category_list.get(temp, u'미상')

    match = re.findall('(?:<h4[^>]+>([^<]+)</h4>\s*<div[^>]+>\s*<div[^>]+>\s*)?(?:<span[^>]+>([^<]+)</span>\s*)?<p class="txt_sense( no_num)?">(.+?)</p>', data)

    if match:
        bot.con.query(
            'PRIVMSG',
            line.target,
            u'검색단어 : %s (사전 : %s)' % (keyword, dic_category)
        )
        res = ''
        i = 1
        lines = 0
        for wordtype, n, nonum, desc in match:
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
                if lines > 2:
                    bot.con.query(
                        'PRIVMSG',
                        line.target,
                        u'멍멍! 결과가 너무 길어요! 직접 가서 보세요 - ' + url
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
        match = re.findall('<p class="txt_sense"(?: no_num)?>(.+?)</p>', data)
        if match:
            bot.con.query(
                'PRIVMSG',
                line.target,
                u'검색단어 : %s (사전 : %s)' % (keyword, dic_category)
            )
            for x in match:
                x = re.sub('</?[^>]+>', '', x)
                bot.con.query(
                    'PRIVMSG',
                    line.target,
                    x
                )
        else:
            bot.con.query(
                'PRIVMSG',
                line.target,
                u'멍멍! 파싱할 수 없습니다! 관리자에게 해당 주소를 제보해주세요 : ' + url
            )