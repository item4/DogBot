# -*- coding:utf-8 -*-
alias=[]

import urllib
import re

def cmd_css(bot,line,args):
    if args is None:
        return

    args = args.lower()

    data = urllib.urlopen('http://w3schools.com/cssref/default.asp').read()
    data = data.decode('utf8').replace('\r','').replace('\n','')
    data = re.search(r'<tr>\s*<td>(?:<a href="([^"]+)">)?%s(?:</a>)?</td>\s*<td>([^<]+)</td>\s*<td>(\d+)</td>\s*</tr>' % args,data)
    """


    """
    if not data:
        bot.con.query(
            'PRIVMSG',
            line.target,
            u'그런거 없다'
        )
    else:
        res = u'[%s/CSS%s] %s' % (args,data.group(3),data.group(2))
        if data.group(1):
            res += u' - http://w3schools.com/cssref/%s' % data.group(1)
        bot.con.query(
            'PRIVMSG',
            line.target,
            res
        )

def main():
    pass

if __name__ == '__main__':
    main()
