# -*- coding:utf-8 -*-

from system.bot import *

def main():
    dog = DogBot()
    dog.add_connect(u'irc.ozinger.org', 6667, 'utf8', ['#item4','#snoin-dev'])
    dog.start()

if __name__ == '__main__':
    main()