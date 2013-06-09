# -*- coding:utf-8 -*-

alias = []
handler = []

import urllib
import re

def cmd_cppf(bot, line, args):
    if not args:
        bot.con.query(
            'PRIVMSG',
            line.target,
            u'C++ 함수와 상수등의 정보를 보여줍니다. | usgae: ?cppf name'
        )
        return

    args = args.lower()

    if '::' in args:
        if args.startswith('std::'):
            args = args[5:]
        url = 'http://cplusplus.com/reference/%s' % args.replace('::','/')
        print url
    else:
        url = 'http://cplusplus.com/search.do?%s' % urllib.urlencode({'q':args})

    con = urllib.urlopen(url)
    data = con.read()
    data = data.decode('utf8').replace('\n','')
    data = re.search(ur'<div id="I_type">(.+?)</div><div id="I_file"[^>]*>&lt;(.+?)&gt;\r?</div><h1>(.+?)</h1>(?:<div class="C_prototype">((?:<div[^>]+>.+?</div>)+|<pre>.+?</pre>|<table>.+?</table>)</div>)?<div id="I_description">(.+?)</div>',data)
    """

<table><tr class="odd"><th>default (1)</th><td><pre>
template &lt;class RandomAccessIterator&gt;
  void sort (RandomAccessIterator first, RandomAccessIterator last);
</pre></td></tr><tr class="even"><th>custom (2)</th><td><pre>
template &lt;class RandomAccessIterator, class Compare&gt;
  void sort (RandomAccessIterator first, RandomAccessIterator last, Compare comp);</pre></td></tr></table>
    """

    if data:
        description = []
        if data.group(4):
            intable = []
            inpre = []
            if data.group(4).startswith('<div '):
                temp = re.finditer(r'<div title="([^"]+)"[^>]*>(.+?)</div>',data.group(4))
                for x in temp:
                    if x.group(2).startswith('<table>'):
                        intable.append((x.group(1),x.group(2)))
                    else:
                        inpre.append((x.group(1),None,x.group(2)[5:-6]))
            elif data.group(4).startswith('<table>'):
                intable.append((None,data.group(4)))
            else:
                inpre.append((None,None,data.group(4)[5:-6]))

            if intable:
                for version,temp in intable:
                    sub = re.finditer(r'<tr[^>]+><th>(.+?)</th><td><pre>(.+?)</pre></td></tr>',temp)
                    for x in sub:
                        inpre.append((version,x.group(1),x.group(2)))

            if inpre:
                for version, case, desc in inpre:
                    print repr(desc)
                    temp = desc.split('\r')
                    print temp
                    for t in temp:
                        if not t:
                            continue
                        print t
                        res = t.strip().replace('&amp;','&')
                        res = re.sub('\s{2,}',' ',res)
                        res = res.replace('&lt;','<').replace('&gt;','>')
                        if case:
                            res = '%s: ' % case + res
                        if version:
                            res = '[%s]' % version + res
                        description.append(res)

        name = data.group(2).replace('\r','')

        name = re.sub(r'</?[^>]+>','',name)

        bot.con.query(
            'PRIVMSG',
            line.target,
            u'\x02%s\x02: %s (%s, #include <%s>)' % (name.replace('&lt;','<').replace('&gt;','>'),
                                                    data.group(5),
                                                    data.group(1),
                                                    data.group(3))
        )
        for x in description:
            bot.con.query(
                'PRIVMSG',
                line.target,
                x
            )
        bot.con.query(
            'PRIVMSG',
            line.target,
            con.url
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
