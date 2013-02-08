# -*- coding:utf-8 -*-
alias=[]

import urllib
import re
import HTMLParser

def cmd_web(bot,line,args):
    if args==None:
        bot.con.query(
            'PRIVMSG',
            line.target,
            u'웹페이지의 내용을 간략히 보여줍니다. | usgae: ?web url'
        )
        return
    if not args.startswith('http://') and not args.startswith('https://'):
        args='http://'+args
    try:
        data=urllib.urlopen(args).read()
    except:
        bot.con.query(
            'PRIVMSG',
            line.target,
            u'접속 실패'
        )

    try:
        data=data.decode('cp949')
    except:
        data=data.decode('utf8','replace')

    data=HTMLParser.HTMLParser().unescape(data)
    data=data.replace('\n',' ').replace('\r','')
    data=re.sub(r'\s{2,}',' ',data)
    data=re.sub(r'<(style|script|title)[^>]*>.*?</\1>','',data,re.I|re.S)
    data=re.sub(r'</?[^>]+>','',data)

    if len(data)>150:
        data=data[:150]
    bot.con.query(
        'PRIVMSG',
        line.target,
        '[%s]  %s'%(args,data)
    )

def main():
    pass

if __name__ == '__main__':
    main()
