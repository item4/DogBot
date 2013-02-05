# -*- coding:utf-8 -*-
alias=[u'날씨']

import urllib
import re

def cmd_aws(bot,line,args):
    if args is None:
        return


    data = urllib.urlopen('http://203.247.66.10/cgi-bin/aws/nph-aws_txt_min').read()
    data = data.decode('cp949').replace('\r','').replace('\n','')

    if '>' + args + '<' not in data:
        data = urllib.urlopen('http://203.247.66.10/cgi-bin/aws/nph-aws_txt_min?&0&MINDB_60M&0&a').read()
        data = data.decode('cp949').replace('\r','').replace('\n','')

    print args in data

    time = re.search(u'\[ 매분관측자료 \] \d+\.\d+\.\d+\.(\d+:\d+)',data)
    data = re.search(ur'<tr[^>]+><td[^>]+><a[^>]+>\d+</a></td><td[^>]+><a[^>]+>%s</a></td><td[^>]+>\d+m</td><td>(<font color=red>○</font>|<font color=blue>●</font>|-)</td><td[^>]*>([^<]*)</td><td[^>]*>[^<]*</td><td[^>]*>[^<]*</td><td[^>]*>[^<]*</td><td[^>]*>([^<]*)</td><td>([^<]*)</td><td class=textg>[^<]*</td><td class=textg>([^<]*)</td><td class=textg>([^<]*)</td><td[^>]*>[^<]*</td><td[^>]*>[^<]*</td><td[^>]*>[^<]*</td><td>([^<]*)</td><td>([^<]*)</td><td align=left class=text2 nowrap>([^<]*)</td></tr>' % args,data)
    """
<tr align=center bgcolor=#F2F2F2 class=text><td bgcolor=#BBDDFF><a href='javascript:parent.parent.menu.stn_select(957);'>957</a></td>
<td bgcolor=#BBDDFF width=50 nowrap><a href='javascript:parent.parent.menu.stn_select(957);'>십이동파</a></td>
<td align=right width=40>91m</td><td>-</td>
<td>.</td><td>.</td><td>.</td><td>.</td><td>.</td><td>0.6</td><td class=textg>338.0</td><td class=textg>NNW</td><td class=textg>6.3</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>.</td><td>1016.4</td><td align=left class=text2 nowrap>전라북도 군산시 옥도면 연도리</td></tr>
    """


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
            u'그런거 없다'
        )




def main():
    pass

if __name__ == '__main__':
    main()
