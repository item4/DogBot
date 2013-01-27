# -*- coding:utf-8 -*-
alias=[]

import hashlib

def cmd_sha224(con,line,args):
    if args==None:
        return
    con.query('PRIVMSG',line.target,'[SHA224] %s = %s'%(args,hashlib.sha224(args).hexdigest()))

def main():
    pass

if __name__ == '__main__':
    main()
