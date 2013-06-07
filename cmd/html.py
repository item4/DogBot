# -*- coding:utf-8 -*-

alias = []
handler = []

import urllib
import re

def cmd_html(bot, line, args):
    if args is None:
        bot.con.query(
            'PRIVMSG',
            line.target,
            u'HTML Tag의 정보를 보여줍니다. | usgae: ?html tag_name | ex) ?html strong'
        )
        return

    args = args.lower()
    tag = args

    if tag in ['h1','h2','h3','h4','h5','h6']:
        tag = '&lt;h1&gt;,&lt;h2&gt;,&lt;h3&gt;,&lt;h4&gt;,&lt;h5&gt;,&lt;h6&gt;'
    else:
        tag = '&lt;%s&gt;' % tag

    data = urllib.urlopen('https://developer.mozilla.org/en-US/docs/Web/Guide/HTML/HTML5/HTML5_element_list').read()
    data = data.decode('utf8').replace('\r','').replace('\n','')
    data = re.search(r'<tr>\s*<td><a href="([^"]+)"><code>%s</code></a>( <a href="/en-US/docs/HTML/HTML5">.+?</a>)?</td>\s*<td>(.+?)</td>\s*</tr>' % tag,data)
    """

    """
    if not data:
        bot.con.query(
            'PRIVMSG',
            line.target,
            u'그런거 없다'
        )
    else:
        tag = tag.replace('&lt;','<').replace('&gt;','>')
        description = data.group(3)
        if data.group(2):
            description = '[HTML5] ' + description
        description = re.sub('</?[^>]*>','',description)
        bot.con.query(
            'PRIVMSG',
            line.target,
            u'%s %s - https://developer.mozilla.org%s' % (tag,description,data.group(1))
        )

def main():
    pass

if __name__ == '__main__':
    main()
