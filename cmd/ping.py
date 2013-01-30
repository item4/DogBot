# -*- coding:utf-8 -*-
alias=[]

def cmd_ping(bot,line,*args):
    bot.con.query(
        'PRIVMSG',
        line.target,
        '%s, pong!' % line.nick
    )

def main():
    pass

if __name__ == '__main__':
    main()
