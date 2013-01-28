# -*- coding:utf-8 -*-
alias=[u'pf']

import urllib
import re

def cmd_phpf(con,line,args):
    if args is None:
        return

    args = args.lower()

    if args.find('::') > 0:
        category,function = args.split('::',1)
    else:
        category = 'function'
        function = args

    function = function.replace('_','-')

    url = 'http://kr.php.net/manual/kr/%s.%s.php' % (category,function)


    data = urllib.urlopen(url).read()
    data = data.decode('utf8','ignore').replace('\r','').replace('\n','')

    data = re.search(ur'<p class="verinfo">\(([^\)]+)\)</p><p class="refpurpose"><span class="refname">([^<]+)</span> &mdash; <span class="dc-title">([^<]+)</span></p>\s*</div>\s*<div[^>]+>\s*<h3 class="title">[^<]+</h3>\s*<div class="methodsynopsis dc-description">(.+?)</div>',data)
    """

    """
    if data:
        description = data.group(4)
        description = re.sub(r'</?[^>]+>','',description)

        con.query(
            'PRIVMSG',
            line.target,
            u'\x02%s\x02: %s (%s)' % (data.group(2).replace('&gt;','>'),
                                    data.group(3).replace('&#039;',"'"),
                                    data.group(1).replace('&gt;','>'))
        )
        con.query(
            'PRIVMSG',
            line.target,
            description
        )
        con.query(
            'PRIVMSG',
            line.target,
            url
        )

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
