# -*- coding:utf-8 -*-
alias=[]

import hashlib

def cmd_sha1(con,line,args):
    if args==None:
        return
    con.query('PRIVMSG',line.target,'[SHA1] %s = %s'%(args,hashlib.sha1(args).hexdigest()))

def main():
    pass

if __name__ == '__main__':
    main()
