# -*- coding:utf-8 -*-

alias = ['pyre2', 'pyre27', 'py2', 'py27']
handler = []


import urllib

from sphinx.ext.intersphinx import read_inventory_v1, read_inventory_v2


def cmd_pyre(bot, line, args):
    if not args:
        bot.con.query(
            'PRIVMSG',
            line.target,
            u'Python 2.7 문서 링크 | usage: ?pyre library_name'
        )
        return

    bot.con.query(
        'PRIVMSG',
        line.target,
        u'http://docs.python.org/2.7/library/%s.html' % args
    )




PACKAGES = {
    'flask': 'http://flask.pocoo.org/docs/',
    'wand': 'http://docs.wand-py.org/en/0.3.7/'
}

def urljoin(*params):
    return '/'.join(params).replace('//', '')


def get_inventory(url):
    inv_url = urljoin(url, 'objects.inv')
    f = urllib.urlopen(inv_url)
    line = f.readline().rstrip().decode('utf-8')
    if line == '# Sphinx inventory version 1':
        invdata = read_inventory_v1(f, url, urljoin)
    elif line == '# Sphinx inventory version 2':
        invdata = read_inventory_v2(f, url, urljoin)
    else:
        raise ValueError(line)
    return invdata


def main():
    if len(sys.argv) < 2:
        print('usage:', sys.argv[0], 'PACKAGE-NAME', file=sys.stderr)
        raise SystemExit(1)
    package = sys.argv[1]
    try:
        url = PACKAGES[package]
    except KeyError:
        print('unsupported package:', package, file=sys.stderr)
        raise SystemExit(1)
    result = get_inventory(url)
    pprint.pprint(result['py:class'])


if __name__ == '__main__':
    main()
