# -*- coding: utf-8 -*-

__all__ = ['DogBotLine']

class DogBotLine:
    __slots__ = "nick", "ident", "ip", "mask", "server", "type", "target", "message", "login"
    nick = ident = ip = mask = server = type = target = message = login = None

    def __init__(self, msg, login):
        if ':' in msg[1:]:
            temp, message = msg[1:].split(' :',1)

            self.message = message
            temp = temp.rstrip()
            temp = temp.split(' ', 2)
            if '!' in temp[0]:
                self.mask = temp[0]
                try:
                    self.nick, t = self.mask.split('!',1)
                except:
                    print self.mask
                self.ident, self.ip = t.split('@',1)
            else:
                self.server = temp[0]
            self.type = temp[1]

            if len(temp) == 3:
                self.target = temp[2]
        else:
            self.mask, self.type, self.message = msg[1:].split(' ',2)
            if '!' in self.mask:
                try:
                    self.nick, t = self.mask.split('!',1)
                except:
                    print mask
                self.ident, self.ip = t.split('@',1)
            else:
                self.server = self.mask
                self.mask = None

        self.login = login.get(self.nick)

    def __repr__(self):
        temp = [self.nick,self.ident,self.ip,self.server,self.type,self.target,self.message,self.login]
        for i in xrange(len(temp)):
            if temp[i] is not None:
                temp[i] = temp[i].encode('utf8')

        format = "'nick':{!r},'ident':{!r},'ip':{!r},'server':{!r},"
        format += "type:{!r},target:{!r},message:{!r},login:{!r}"
        return '<DogBotLine>{' + format.format(*temp) + '}'

def main():
    pass

if __name__ == '__main__':
    main()
