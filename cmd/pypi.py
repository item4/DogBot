# -*- coding:utf-8 -*-

alias = []
handler = []

import xmlrpclib

from distutils.version import StrictVersion, LooseVersion

# source base : https://github.com/pypa/pip/blob/develop/pip/commands/search.py

def cmd_pypi(bot, line, args):
    if not args:
        bot.con.query(
            'PRIVMSG',
            line.target,
            u'Python Packeage Index에서 해당하는 키워드를 검색합니다 | usage: ?pypi wand'
        )
        return

    try:
        pypi = xmlrpclib.ServerProxy('https://pypi.python.org/pypi')
        hits = pypi.search({'name': args, 'summary': args}, 'or')
    except:
        bot.con.query(
            'PRIVMSG',
            line.target,
            u'멍멍! xmlrpc 접속에 실패했어요!'
        )
        return

    packages = {}
    for hit in hits:
        name = hit['name']
        summary = hit['summary']
        version = hit['version']
        score = hit['_pypi_ordering']
        if score is None:
            score = 0

        if name not in packages.keys():
            packages[name] = {'name': name, 'summary': summary, 'versions': [version], 'score': score}
        else:
            packages[name]['versions'].append(version)

            # if this is the highest version, replace summary and score
            if version == highest_version(packages[name]['versions']):
                packages[name]['summary'] = summary
                packages[name]['score'] = score

        if name.lower() == args.lower():
            packages[name]['score'] += 100000

    # each record has a unique name now, so we will convert the dict into a list sorted by score
    package_list = sorted(packages.values(), key=lambda x: x['score'], reverse=True)[:3]

    for package in package_list:
        res = '%s/%s' % (package['name'],highest_version(package['versions']))
        if package['summary']:
            res += ' - ' + package['summary']

        bot.con.query(
            'PRIVMSG',
            line.target,
            res
        )

def compare_versions(version1, version2):
    try:
        return cmp(StrictVersion(version1), StrictVersion(version2))
    # in case of abnormal version number, fall back to LooseVersion
    except ValueError:
        pass
    try:
        return cmp(LooseVersion(version1), LooseVersion(version2))
    except TypeError:
    # certain LooseVersion comparions raise due to unorderable types,
    # fallback to string comparison
        return cmp([str(v) for v in LooseVersion(version1).version],
                   [str(v) for v in LooseVersion(version2).version])

def highest_version(versions):
    return reduce((lambda v1, v2: compare_versions(v1, v2) == 1 and v1 or v2), versions)