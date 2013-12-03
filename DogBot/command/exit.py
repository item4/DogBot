# -*- coding:utf-8 -*-

alias = []
handler = []

def cmd_exit(bot, line, args):
    if line.login != 'item4':
        bot.con.query(
            'PRIVMSG',
            line.target,
            u'으르렁…! 관리자만 사용가능한 명령어입니다.'
        )
        return
    if not args:
        args = 'EXIT Program'

    bot.con.send(
        'QUIT :' + args
    )

    bot.system.running = False
    bot.system.exit_reason = args