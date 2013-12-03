# -*- coding:utf-8 -*-

from DogBot.system.bot import *

def main():
        dog = DogBot()
        dog.load_config()
        dog.add_connect(u'irc.ozinger.org', 6667, 'utf8', ['#item4','#hest','#snoin','#snoin-dev','#sj','#nagi'])
        dog.start()

if __name__ == '__main__':
    main()