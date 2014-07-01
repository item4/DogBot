# -*- coding:utf-8 -*-

alias = [u'구글','g']
handler = []

import urllib
import urllib2
import re
import HTMLParser


base_pattern = re.compile('<li class="g"[^>]*>(?P<div><div>)?<!--m-->(.+?)(?(div)</li><!--n-->|<!--n--></li>)')
temp_pattern = re.compile('<h3 class="r"><a href="([^"]+)"[^>]+>(.+?)</a></h3>')
desciption_pattern = re.compile('<span class="st">(.+?)</span>')


def cmd_gg(bot, line, args):
    if not args:
        bot.con.query(
            'PRIVMSG',
            line.target,
            u'구글 검색 명령어입니다. | usage: ?gg 검색어'
        )
        return

    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.52 Safari/537.17')]
    try:
        data = opener.open('http://www.google.co.kr/search?%s' % urllib.urlencode({'q': args.encode('u8')}), None, 3).read()
    except:
        bot.con.query(
            'PRIVMSG',
            line.target,
            u'멍멍! 접속에 실패했어요!'
        )
        return

    data = data.decode('u8', 'replace')
    data = data.replace('\n', ' ').replace('\r', '')
    f = data.find('<li class="g"')
    if f == -1:
        bot.con.query(
            'PRIVMSG',
            line.target,
            u'멍멍! 검색결과가 없어요!'
        )
    else:
        result = base_pattern.findall(data[f:])[:3]
        print result

        if not result:
            temp = data.find('<li class="g">') == -1 or data.find('<li class="g" ') == -1
            if temp:
                bot.con.query(
                    'PRIVMSG',
                    line.target,
                    u'멍멍! 검색결과가 없어요!'
                )
            else:
                bot.con.query(
                    'PRIVMSG',
                    line.target,
                    u'멍멍! 파싱에 실패했어요! 디버그 코드 : ' + str(data.find('<li class="g">'))
                )
            return

        for _, x in result:
            temp = temp_pattern.search(x)
            url, title = temp.group(1), temp.group(2)
            try:
                description = desciption_pattern.search(x).group(1)
            except AttributeError:
                res = u'[ %s - %s ] 설명이 없습니다.' % (title, url)
            else:
                res = u'[ %s - %s ] %s' % (title, url, description)

            res = res.replace('<br>', '').replace('<wbr>', '')
            res = res.replace('<b>', '').replace('</b>', '')
            res = res.replace('<em>', '\x02').replace('</em>', '\x02')
            res = res.replace('<span class="f">', '').replace('</span>', '')
            res = re.sub('<a [^>]+>(.+?)</a>', r'\1', res)

            res = HTMLParser.HTMLParser().unescape(res)
            bot.con.query(
                'PRIVMSG',
                line.target,
                res
            )