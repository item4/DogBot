# -*- coding:utf-8 -*-

from DogBot.system.bot import *


def main():
        dog = DogBot()
        dog.load_config()
        dog.start()

if __name__ == '__main__':
    main()