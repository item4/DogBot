# -*- coding:utf-8 -*-
alias=[]

import hashlib

def cmd_sha512(bot,line,args):
    if args==None:
        return
    bot.con.query(
        'PRIVMSG',
        line.target,
        '[SHA512] %s = %s' % (args,hashlib.sha512(args).hexdigest())
    )

def main():
    pass

if __name__ == '__main__':
    main()
