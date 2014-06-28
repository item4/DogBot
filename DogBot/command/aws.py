# -*- coding:utf-8 -*-

alias = [u'날씨']
handler = []

import re
import urllib2

time_pattern = re.compile(u'\[ 매분관측자료 \] \d+\.\d+\.\d+\.(\d+:\d+)')

def cmd_aws(bot, line, args):
    if args is None:
        bot.con.query(
            'PRIVMSG',
            line.target,
            u'기상청 AWS 관측대의 정보를 보여줍니다. | usgae: ?aws 지역명 | ex) ?aws 서울'
        )
        return

    try:
        data = urllib2.urlopen('http://203.247.66.10/cgi-bin/aws/nph-aws_txt_min', None, 3).read()
        data = data.decode('cp949').replace('\r', '').replace('\n', '')

        if '>' + args + '<' not in data:
            data = urllib2.urlopen('http://203.247.66.10/cgi-bin/aws/nph-aws_txt_min?&0&MINDB_60M&0&a', None, 3).read()
            data = data.decode('cp949').replace('\r', '').replace('\n', '')
    except:
        bot.con.query(
            'PRIVMSG',
            line.target,
            u'멍멍! 기상청 AWS에 접속할 수 없어요!'
        )
        return

    time = time_pattern.search(data)
    data = re.search(ur'<tr[^>]+><td[^>]+><a[^>]+>\d+</a></td><td[^>]+><a[^>]+>%s</a></td><td[^>]+>\d+m</td><td>(<font color=red>○</font>|<font color=blue>●</font>|-)</td><td[^>]*>([^<]*)</td><td[^>]*>[^<]*</td><td[^>]*>[^<]*</td><td[^>]*>[^<]*</td><td[^>]*>([^<]*)</td><td>([^<]*)</td><td class=textg>[^<]*</td><td class=textg>([^<]*)</td><td class=textg>([^<]*)</td><td[^>]*>[^<]*</td><td[^>]*>[^<]*</td><td[^>]*>[^<]*</td><td>([^<]*)</td><td>([^<]*)</td><td align=left class=text2 nowrap>([^<]*)</td></tr>' % args,data)

    if data:
        if data.group(1) == '-' or data.group(1) == '.':
            rain = u'모름'
        elif data.group(1) == u'<font color=red>○</font>':
            rain = u'아니오'
        else:
            rain = u'예(15min:%s/일일:%s)' % (data.group(2),data.group(3))

        temperature = data.group(4)
        wind = u'%s %s㎧' % (data.group(5).replace('N',u'북').\
                                        replace('S',u'남').\
                                        replace('W',u'서').\
                                        replace('E',u'동'),data.group(6))
        humidity = data.group(7)
        pressure = data.group(8)
        position = data.group(9)

        res = u'[%s@%s/%s]' % (time.group(1),args,position)

        res += u' 강수:%s / %s℃ / 바람:%s' % (rain,temperature,wind)

        if humidity != '.':
            res += u' / 습도:%s%%' % humidity

        if pressure != '.':
            res += u' / 해면기압:%shPa' % pressure

        bot.con.query(
            'PRIVMSG',
            line.target,
            res
        )

    else:
        bot.con.query(
            'PRIVMSG',
            line.target,
            u'멍멍! 해당 지역명은 존재하지 않아요!'
        )