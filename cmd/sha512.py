# -*- coding:utf-8 -*-
alias=[]

import hashlib

def cmd_sha512(bot,line,args):
    if args==None:
        bot.con.query(
            'PRIVMSG',
            line.target,
            u'입력받은 문자열의 sha512 인코딩 결과를 출력합니다. | usage: ?sha512 string'
        )
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
