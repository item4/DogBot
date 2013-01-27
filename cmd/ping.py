# -*- coding:utf-8 -*-
alias=[]

def cmd_ping(con,line,*args):
    con.query('PRIVMSG',line.target,'%s, pong'%line.nick)

def main():
    pass

if __name__ == '__main__':
    main()
