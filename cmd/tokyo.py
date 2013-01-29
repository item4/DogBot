# -*- coding:utf-8 -*-
alias=[u'도쿄도','tokyotosho']

import urllib
import re

def cmd_tokyo(con,line,args):
    if args is None:
        url = 'http://www.tokyotosho.info/?cat=7'
    else:
        url = 'http://www.tokyotosho.info/search.php?%s' % urllib.urlencode({'terms':args.encode('utf8'),'type':7})

    try:
        data = urllib.urlopen(url).read()
    except IOError:
        con.query(
            'PRIVMSG',
            line.target,
            u'timeout'
        )
        return
    data = data.decode('utf8').replace('\r','').replace('\n','')
    data = re.finditer(r'<tr[^>]+><td[^>]+><a[^>]+><span[^>]+></span></a></td><td[^>]+><a[^>]+><span[^>]+></span></a> <a rel="nofollow" type="application/x-bittorrent" href="([^"]+)">(.+?)</a></td><td[^>]+>(?:<a[^>]+>Website</a> \| )?<a[^>]+>Details</a></td></tr><tr[^>]+><td[^>]+>(?:Authorized: <span class="auth_ok">Yes</span> )?Submitter: (?:<a[^>]+>.*?</a>|Anonymous) \| Size: ([^\|]+) \| Date: ([^\|]+)(?: \| Comment: .*?)?</td><td[^>]+>S: <span[^>]+>(\d+)</span> L: <span[^>]+>(\d+)</span> C: <span[^>]+>(\d+)</span> ID: \d+</td></tr>',data)
    """


    """
    i = 1
    for x in data:
        res=u'%s (%s/%s/S:%s/L:%s/C:%s) - %s' % (\
            x.group(2).replace('<span class="s"> </span>',''),\
            x.group(3),x.group(4),x.group(5),x.group(6),\
            x.group(7),x.group(1).replace('&amp;','&'))
        con.query(
            'PRIVMSG',
            line.target,
            res
        )
        i += 1
        if i > 3:
            break
    else:
        con.query(
            'PRIVMSG',
            line.target,
            u'그런거 없다'
        )




def main():
    pass

if __name__ == '__main__':
    main()
