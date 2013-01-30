# -*- coding:utf-8 -*-
alias=[]

import urllib
import re

def cmd_cppf(bot,line,args):
    if args is None:
        return

    args = args.lower()

    url = 'http://cplusplus.com/%s' % args

    data = urllib.urlopen(url).read()
    data = data.decode('utf8').replace('\n','')
    data = re.search(ur'<div id="I_type">(.+?)</div><h1>(.+?)</h1><div id="I_file"[^>]+>&lt;(.+?)&gt;</div>(?:<div class="C_prototype"><pre>(.+?)</pre></div>)?<div id="I_description">(.+?)</div>',data)
    """

    """
    if data:
        if data.group(4):
            description = data.group(4).split('\r')
        else:
            description = []

        bot.con.query(
            'PRIVMSG',
            line.target,
            u'\x02%s\x02: %s (%s, #include <%s>)' % (data.group(2),\
                                                    data.group(5),\
                                                    data.group(1),\
                                                    data.group(3))
        )
        for x in description:
            bot.con.query(
                'PRIVMSG',
                line.target,
                x.strip().replace('      ','')
            )
        bot.con.query(
            'PRIVMSG',
            line.target,
            url
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
