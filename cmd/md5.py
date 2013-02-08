# -*- coding:utf-8 -*-
alias=[]

import hashlib

def cmd_md5(bot,line,args):
    if args==None:
        bot.con.query(
            'PRIVMSG',
            line.target,
            u'입력받은 문자열의 md5 인코딩 결과를 출력합니다. | usage: ?md5 string'
        )
        return
    bot.con.query(
        'PRIVMSG',
        line.target,
        '[MD5] %s = %s' % (args,hashlib.md5(args).hexdigest())
    )

def main():
    pass

if __name__ == '__main__':
    main()
