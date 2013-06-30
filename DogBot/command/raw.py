# -*- coding:utf-8 -*-

alias = []
handler = []

import re

def cmd_raw(bot, line, args):
    if line.login != 'item4':
        bot.con.query(
            'PRIVMSG',
            line.target,
            u'으르렁…! 관리자만 사용가능한 명령어입니다.'
        )
        return
    elif not args:
        bot.con.query(
            'PRIVMSG',
            line.target,
            u'멍멍! 명령어를 입력해주세요.'
        )
        return

    temp = args.split(' ',3)
    temp[0] = temp[0].upper()
    if temp[0] == 'NICK':
        bot.nick = temp[1]
    elif temp[0] == 'MODE':
        chunk = ' '.join(temp[1:]).split(' ',2)

        if len(chunk) == 3 and chunk[0][0] == '#':
            t = re.match('\((.+?)\)(.+$)', bot.db['server']['PREFIX'])

            mode_str = list(t.group(1))
            prefix_str = list(t.group(2))

            channel, mode, t = chunk
            flag = ''
            i = 0
            nicks = t.split()
            for m in list(mode):
                if m in '+-':
                    flag = m
                else:
                    try:
                        t = prefix_str[mode_str.index(m)]
                        if t in 'qaoh' and t not in bot.db['channel'][channel]['member'][bot.nick]:
                            bot.con.query(
                                'PRIVMSG',
                                line.target,
                                u'멍멍! 해당 쿼리의 수행 권한이 없어요!'
                            )
                            return
                        if flag == '+':
                            bot.db['channel'][channel]['member'][nicks[i]] = bot.db['channel'][channel]['member'][nicks[i]] | set(t)
                        else:
                            bot.db['channel'][channel]['member'][nicks[i]] = bot.db['channel'][channel]['member'][nicks[i]] - set(t)
                    except:
                        pass
                    i += 1

        bot.con.query(' '.join(temp))
        return
    elif temp[0] in ['QUIT','EXIT']:
        bot.con.query(
            'PRIVMSG',
            line.target,
            u'멍멍! QUIT, EXIT는 명령어를 이용해주세요!'
        )
        return

    bot.con.query(*temp)