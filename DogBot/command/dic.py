# -*- coding:utf-8 -*-

alias = ['d',u'사전']
handler = []

import re
import urllib
import time


step1_pattern = re.compile('<strong[^>]+>\s*<a href="([^>]+)" class="\s*link_txt\s*"\s*>')

def cmd_dic(bot, line, args):
    if not args:
        bot.con.query(
            'PRIVMSG',
            line.target,
            u'다음 사전에서 검색하여 결과를 볼 수 있는 주소를 알려줍니다 | usage: ?dic 단어 | ?dic -dic 한영 단어'
        )
        return

    dic_category_list = {'ek':u'영한','ke':u'한영','ee':u'영영','kk':u'국어',
                         'hh':u'한자','kj':u'한일','kc':u'한중','kh':u'힌디',
                         'kt':u'터키','yk':u'태국',
                         'kr':u'러시아','kd':u'프랑스','kv':u'베트남',
                         'ki':u'이탈리아'
                         }
    dic_lang_list = {v:k for k,v in dic_category_list.items()}

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

    dic = dic_lang_list.get(dic, dic)
    
    data = urllib.urlopen('http://dic.daum.net/search.do?%s' % \
                          urllib.urlencode({'q': keyword.encode('u8')})).read()

    data = data.decode('u8').replace('\r', '').replace('\n', '')

    data = step1_pattern.findall(data)

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

    bot.con.query(
        'PRIVMSG',
        line.target,
        url
    )
