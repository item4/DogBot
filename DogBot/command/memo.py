# -*- coding:utf-8 -*-

alias = [u'기억',u'덧붙',u'잊어',u'알려']
handler = []

import sqlite3

"""
DB Scheme
create table memo (uid integer primary key autoincrement, keyword varchar(50), content text, writer varchar(30))
"""


def cmd_memo(bot, line, args):
    if ' ' not in line.message[1:]:
        if line.message[1:].startswith('memo'):
            bot.con.query(
                'PRIVMSG',
                line.target,
                u'메모 기능입니다 | usage: ?memo add 단어 정보'
            )
            return
        else:
            cmd = line.message[1:]
            args = ''
    else:
        cmd, _ = line.message[1:].split(' ',1)

    if args is None:
        args = ''

    if cmd == u'기억':
        cmd = 'add'
    elif cmd == u'덧붙':
        cmd = 'append'
    elif cmd == u'잊어':
        cmd = 'remove'
    elif cmd == u'알려':
        cmd = 'view'
    elif args.startswith('add'):
        cmd = 'add'
        if ' ' in args:
            _, args = args.split(' ',1)
        else:
            args = ''
    elif args.startswith('append'):
        cmd = 'append'
        if ' ' in args:
            _, args = args.split(' ',1)
        else:
            args = ''
    elif args.startswith('remove'):
        cmd = 'remove'
        if ' ' in args:
            _, args = args.split(' ',1)
        else:
            args = ''
    elif args.startswith('view'):
        cmd = 'view'
        if ' ' in args:
            _, args = args.split(' ',1)
        else:
            args = ''
    else:
        bot.con.query(
            'PRIVMSG',
            line.target,
            u'멍멍! 알 수 없는 명령어입니다.'
        )
        return

    if not args:
        if cmd == 'add':
            bot.con.query(
                'PRIVMSG',
                line.target,
                u'입력받은 정보를 기억해줍니다. | usage: ?기억 단어 정보'
            )
        elif cmd == u'append':
            bot.con.query(
                'PRIVMSG',
                line.target,
                u'입력받은 정보를 이미 저장된 기억에 덧붙여줍니다. | usage: ?덧붙 단어 정보'
            )
        else:
            bot.con.query(
                'PRIVMSG',
                line.target,
                u'입력받은 단어를 저장된 기억에서 지워줍니다. | usage: ?잊어 단어'
            )
        return
    elif ' ' not in args and cmd in ['add','append']:
        bot.con.query(
            'PRIVMSG',
            line.target,
            u'멍멍! 파라메터가 부족합니다.'
        )
        return

    if cmd in ['add','append']:
        keyword, desc = args.split(' ',1)
    else:
        keyword = args

    if len(keyword) > 50:
        bot.con.query(
            'PRIVMSG',
            line.target,
            u'멍멍! 키워드가 너무 깁니다.'
        )
        return



    con = sqlite3.connect(bot.system.dbname)
    c = con.cursor()

    with con:
        c.execute('select `uid` from `memo` where `keyword`=? limit 1;', (keyword,))
        uid = c.fetchone()
        if uid and cmd == 'add':
            bot.con.query(
                'PRIVMSG',
                line.target,
                u'멍멍! 이미 저장된 단어입니다.'
            )
            return
        elif uid is None and cmd != 'add':
            bot.con.query(
                'PRIVMSG',
                line.target,
                u'멍멍! 저장되지 않은 단어입니다.'
            )
            return

        if uid is not None:
            uid = uid[0]

        if cmd == 'add':
            try:
                c.execute('insert into `memo` (`uid`,`keyword`,`content`,`writer`) values (NULL,?,?,?)', (keyword, desc, line.nick))
            except Exception as e:
                bot.con.query(
                    'PRIVMSG',
                    line.target,
                    u'멍멍! 저장도중 에러가 발생하였습니다. - %s' % e
                )
            else:
                bot.con.query(
                    'PRIVMSG',
                    line.target,
                    u'이런건 좀 기억해주겠다.'
                )
        elif cmd == 'remove':
            try:
                c.execute('delete from `memo` where `uid`=?;', (uid,))
            except Exception as e:
                bot.con.query(
                    'PRIVMSG',
                    line.target,
                    u'멍멍! 삭제도중 에러가 발생하였습니다. - %s' % e
                )
            else:
                bot.con.query(
                    'PRIVMSG',
                    line.target,
                    u'이젠 잊어주겠다.'
                )
        else:
            c.execute('select * from `memo` where `uid`=? limit 1;', (uid,))

            if cmd == 'view':
                _, keyword, desc, writer = c.fetchone()
                bot.con.query(
                    'PRIVMSG',
                    line.target,
                    u'%s: %s 라고 %s가 최종 저장함.' % (keyword,desc,writer)
                )
            elif cmd == 'append':
                _, _, old_desc, _ = c.fetchone()
                desc = old_desc + ' | ' + desc
                try:
                    c.execute('update `memo` set `content`=? where `uid`=?;', (desc, uid))
                except Exception as e:
                    bot.con.query(
                        'PRIVMSG',
                        line.target,
                        u'멍멍! 저장도중 에러가 발생하였습니다. - %s' % e
                    )
                else:
                    bot.con.query(
                        'PRIVMSG',
                        line.target,
                        u'이런건 좀 더 기억해주겠다.'
                    )

        con.commit()