# -*- coding: utf-8 -*-

alias = ['=', u'계산']
handler = []

from DogBot.system.error import DogBotError

import math
import re

from decimal import Decimal


def cmd_calc(bot, line, args):
    if not args:
        bot.con.query(
            'PRIVMSG',
            line.target,
            u'구글 검색을 통해 계산을 수행합니다. | usage: ?= 1+2*3/4'
        )
        return
    try:
        res = calc(args)
    except DogBotError as e:
        bot.con.query(
            'PRIVMSG',
            line.target,
            u'멍멍! 에러났어요! - %s' % (e,)
        )
    else:
        bot.con.query(
            'PRIVMSG',
            line.target,
            '%.8f' % (res,)
        )

operator_level = {}
operator_level['('] = 0
operator_level[')'] = 0
operator_level[','] = 10000
operator_level['abs'] = 1000
operator_level['sin'] = 1000
operator_level['cos'] = 1000
operator_level['tan'] = 1000
operator_level['sqrt'] = 1000
operator_level['ceil'] = 1000
operator_level['floor'] = 1000
operator_level['round'] = 1000
operator_level['+'] = 1
operator_level['-'] = 1
operator_level['%'] = 2
operator_level['*'] = 3
operator_level['/'] = 3
operator_level['**'] = 4
operator_level['^'] = 4

operator_term = {}
operator_term['('] = 0
operator_term[')'] = 0
operator_term[','] = 2
operator_term['abs'] = 1
operator_term['sin'] = 1
operator_term['cos'] = 1
operator_term['tan'] = 1
operator_term['sqrt'] = 1
operator_term['ceil'] = 1
operator_term['floor'] = 1
operator_term['round'] = 1
operator_term['+'] = 2
operator_term['-'] = 2
operator_term['%'] = 2
operator_term['*'] = 2
operator_term['/'] = 2
operator_term['**'] = 2
operator_term['^'] = 2


def priority(op):
    return operator_level[op]


def need_term(op):
    return operator_term[op]


def calc(args):
    args = re.sub('(-(?:\.\d+|\d+\.|\d+\.\d+|\d+|pi|e))', '+(\\1)', args)

    if args[0] == '+':
        args = '0' + args

    args = args.replace('(+', '(0+')

    term_pattern = re.compile('-?(?:\d+\.\d+|\.\d+|\d+\.|\d+)|pi|e')
    operator_pattern = re.compile(',|\+|-|\*\*|\*|/|%|\(|\)|abs|sin|cos|tan|sqrt|ceil|floor|round')

    result_stack = []
    operator_stack = []

    length = len(args)
    i = 0

    while i < length:
        term = term_pattern.match(args[i:])
        if term:
            temp = term.group(0)
            if temp == 'pi':
                t = math.pi
            elif temp == 'e':
                t = math.e
            else:
                t = temp

            result_stack.append(Decimal(t))
            i += len(temp)
            continue

        operator = operator_pattern.match(args[i:])
        if operator:
            op = operator.group(0)

            if op == '(':
                operator_stack.append(op)
            elif op == ')':
                temp = operator_stack.pop()
                while temp != '(':
                    result_stack.append(temp)
                    temp = operator_stack.pop()
            else:
                if operator_stack and priority(operator_stack[-1]) >= priority(op):
                    result_stack.append(operator_stack.pop())
                operator_stack.append(op)

            i += len(op)
            continue
        raise DogBotError(u'비정상적인 연산자')

    while operator_stack:
        result_stack.append(operator_stack.pop())

    term_stack = []

    while result_stack:
        some = result_stack[0]
        result_stack[:] = result_stack[1:]
        if type(some) == Decimal:
            term_stack.append(some)
        else:
            op = some
            temp = need_term(op)
            if temp == 1:
                t = term_stack.pop()
                if op == 'abs':
                    res = abs(t)
                elif op == 'sin':
                    res = math.sin(t)
                elif op == 'cos':
                    res = math.cos(t)
                elif op == 'tan':
                    res = math.tan(t)
                elif op == 'sqrt':
                    res = math.sqrt(t)
                elif op == 'ceil':
                    res = math.ceil(t)
                elif op == 'floor':
                    res = math.floor(t)
                elif op == 'round':
                    res = round(float(t[0]), int(t[1]))
            elif temp == 2:
                try:
                    back = term_stack.pop()
                    front = term_stack.pop()
                except IndexError:
                    raise DogBotError(u'인자 갯수가 올바르지 않음')

                if op == '+':
                    res = Decimal(front + back)
                elif op == '-':
                    res = Decimal(front - back)
                elif op == '*':
                    res = Decimal(front * back)
                elif op == '/':
                    res = Decimal(front / back)
                elif op == '%':
                    res = Decimal(front % back)
                elif op == '**':
                    res = Decimal(front ** back)
                elif op == '^':
                    res = Decimal(front ** back)
                elif op == ',':
                    res = (front, back)

            term_stack.append(res)

    return term_stack[0]


def main():
    pass

if __name__ == '__main__':
    main()
