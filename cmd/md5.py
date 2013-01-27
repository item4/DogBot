# -*- coding:utf-8 -*-
alias=[]

import hashlib

def cmd_md5(con,line,args):
    if args==None:
        return
    con.query('PRIVMSG',line.target,'[MD5] %s = %s'%(args,hashlib.md5(args).hexdigest()))

def main():
    pass

if __name__ == '__main__':
    main()
