# -*- coding:utf-8 -*-
alias=[u'html']

import urllib
import re

def cmd_tag(bot,line,args):
    if args is None:
        return

    args = args.lower()
    tag = args

    if tag in ['h1','h2','h3','h4','h5','h6']:
        tag = '&lt;h1&gt; to &lt;h6&gt;'
    elif tag in ['comment','<!---->','<!--...-->']:
        tag = '&lt;!--...--&gt;'
    elif tag == 'doctype':
        tag = '&lt;!DOCTYPE&gt;'
    else:
        tag = '&lt;%s&gt;' % tag

    data = urllib.urlopen('http://w3schools.com/tags/default.asp').read()
    data = data.decode('utf8').replace('\r','').replace('\n','')
    data = re.search(r'<tr><td><a href="([^"]+)"(?: class="notsupported")?>%s</a>(<span class="new">New</span>)?</td><td>(.+?)</td></tr>' % tag,data)
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
        description = data.group(3).replace('<span class="deprecated">','').replace('</span>','')
        if data.group(2):
            description = '[NEW tag in HTML5]' + description
        bot.con.query(
            'PRIVMSG',
            line.target,
            u'%s %s - http://w3schools.com/tags/%s' % (tag,description,data.group(1))
        )

def main():
    pass

if __name__ == '__main__':
    main()
