# -*- coding:utf-8 -*-
alias=[]

import urllib
import urllib2
import re
import HTMLParser

def cmd_gg(bot,line,args):
    if args==None:
        return
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.52 Safari/537.17')]
    data = opener.open('http://www.google.co.kr/search?%s' % urllib.urlencode({'q':args.encode('utf8')})).read()

    data=data.decode('utf8','replace')
    data=data.replace('\n',' ').replace('\r','')
    f=data.find('<li class="g">')
    if f==-1:
        con.query('PRIVMSG',line.target,u'검색 실패')
    else:
        data=data[f:]
        pattern=re.compile(r'<li class="g"><div[^>]*>\s*<div[^>]*>\s*<div[^>]*>\s*</div>\s*</div>\s*<h3 class="r"><a href="([^"]+)"[^>]+>(.+?)</a></h3><div class="s"><div class="f kv"><cite>.*?</cite>.*?</div>.*?<span class="st">(.*?)</span>(<div class=osl>.+?</div>)?</div></div><!--n-->(<table class="nrgt" cellpadding="0" cellspacing="0">.+?</table>)?</li>')

        iter=pattern.finditer(data)

        c=1
        for x in iter:
            res=u'[ %s - %s ] %s' % (x.group(2),x.group(1),x.group(3))
            res=res.replace('<br>','').replace('<wbr>','')
            res=res.replace('<b>','').replace('</b>','')
            res=res.replace('<em>','\x02').replace('</em>','\x02')
            res=res.replace('<span class="f">','').replace('</span>','')

            res=HTMLParser.HTMLParser().unescape(res)
            bot.con.query(
                'PRIVMSG',
                line.target,
                res
            )
            c+=1
            if c>3:
                break
        else:
            bot.con.query('PRIVMSG',line.target,u'파싱 실패')


    return



    if data:
        data=data[0]
        #if len(data)>150:
        #    data=data[:150]
        con.query(
            'PRIVMSG',
            line.target,
            u'[%s]  %s'%(args,data.group[0])
        )
    else:
        con.query('PRIVMSG',line.target,u'그런거 없다.')

def main():
    pass

if __name__ == '__main__':
    main()