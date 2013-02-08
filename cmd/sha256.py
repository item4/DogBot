# -*- coding:utf-8 -*-
alias=[]

import hashlib

def cmd_sha256(bot,line,args):
    if args==None:
        bot.con.query(
            'PRIVMSG',
            line.target,
            u'입력받은 문자열의 sha256 인코딩 결과를 출력합니다. | usage: ?sha256 string'
        )
        return
    bot.con.query(
        'PRIVMSG',
        line.target,
        '[SHA256] %s = %s' % (args,hashlib.sha256(args).hexdigest())
    )

def main():
    pass

if __name__ == '__main__':
    main()
