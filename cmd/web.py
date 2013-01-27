# -*- coding:utf-8 -*-
alias=[]

import urllib
import re
import HTMLParser

def cmd_web(con,line,args):
    if args==None:
        return
    if not args.startswith('http://') and not args.startswith('https://'):
        args='http://'+args
    data=urllib.urlopen(args).read()

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
    con.query('PRIVMSG',line.target,'[%s]  %s'%(args,data))

def main():
    pass

if __name__ == '__main__':
    main()
