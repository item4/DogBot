# -*- coding:utf-8 -*-

alias = []
handler = []

def cmd_raw(bot, line, args):
    if line.login != 'item4':
        bot.con.query(
            'PRIVMSG',
            line.target,
            u'으르렁…! 관리자만 사용가능한 명령어입니다.'
        )
        return
    temp = args.split(' ',2)
    temp[0] = temp[0].upper()
    if temp[0] == 'NICK':
        bot.nick = temp[1]
    elif temp[0] in ['QUIT','EXIT']:
        bot.con.query(
            'PRIVMSG',
            line.target,
            u'멍멍! QUIT, EXIT는 명령어를 이용해주세요!'
        )
        return
    bot.con.query(*temp)