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
        if type(res) == Decimal:
            bot.con.query(
                'PRIVMSG',
                line.target,
                '%s == %s' % (args, round(res, 6))
            )
        else:
            bot.con.query(
                'PRIVMSG',
                line.target,
                u'멍멍! 결과가 상수가 아니에요!'
            )

operator_function = [
                     'abs', 'sqrt', 'factorial',
                     'max', 'min', 'sum', 'count', 'len',
                     'avg', 'average', 'varp', 'var', 'stdevp', 'stdev',
                     'ceil', 'floor', 'round',
                     'log', 'ln', 'log10',
                     'deg', 'rad', 'degree', 'radian',
                     'acosh', 'asinh', 'atanh', 'acos', 'asin', 'atan', 'cosh',
                     'sinh', 'tanh', 'cos', 'sin', 'tan',
                     'test'
                     ]

operator_level = {}
operator_level['('] = -1
operator_level[')'] = -1
operator_level[','] = 0
operator_level['+'] = 1
operator_level['-'] = 1
operator_level['%'] = 2
operator_level['*'] = 3
operator_level['/'] = 3
operator_level['**'] = 4
operator_level['^'] = 4
for x in operator_function:
    operator_level[x] = 1000

operator_term = {}
operator_term['('] = 0
operator_term[')'] = 0
operator_term[','] = 2
operator_term['+'] = 2
operator_term['-'] = 2
operator_term['%'] = 2
operator_term['*'] = 2
operator_term['/'] = 2
operator_term['**'] = 2
operator_term['^'] = 2
for x in operator_function:
    operator_term[x] = 1


def average(args):
    return sum(args) / len(args)


def variance(args, entire=False):
    var = 0
    avg = average(args)
    for x in args:
        var += (avg - x) ** 2
    if entire:
        return var / (len(args) - 1)
    else:
        return var / len(args)


def priority(op):
    return operator_level[op]


def need_term(op):
    return operator_term[op]


def calc(args):
    args = re.sub('(-(?:\.\d+|\d+\.|\d+\.\d+|\d+|pi|e))', '+(\\1)', args)

    if args[0] == '+':
        args = '0' + args

    args = args.replace('(+', '(0+').replace(',+', ',0+')

    term_pattern = re.compile('\s*(-?\s*(?:\d+\.\d+|\.\d+|\d+\.|\d+)|pi|e)\s*')
    operator_pattern = re.compile('\s*(,|\+|-|\*\*|\*|/|%|\(\s*|\s*\)|' + '|'.join(operator_function) + ')\s*')

    result_stack = []
    operator_stack = []

    length = len(args)
    i = 0

    while i < length:
        term = term_pattern.match(args[i:])
        if term:
            temp = term.group(1).replace(' ', '')
            if temp == 'pi':
                t = math.pi
            elif temp == 'e':
                t = math.e
            else:
                t = temp

            result_stack.append(Decimal(t))
            i += len(term.group(0))
            continue

        operator = operator_pattern.match(args[i:])
        if operator:
            op = operator.group(1).replace(' ', '')

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

            i += len(operator.group(0))
            continue
        raise DogBotError(u'비정상적인 연산자 : ' + args[i:])

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
                elif op == 'acos':
                    res = math.acos(t)
                elif op == 'asin':
                    res = math.asin(t)
                elif op == 'atan':
                    res = math.atan(t)
                elif op == 'factorial':
                    res = math.factorial(t)
                elif op == 'log':
                    if type(t) == list:
                        res = math.log(t[0], t[1])
                    else:
                        res = math.log(t)
                elif op == 'ln':
                    res = math.log(t)
                elif op == 'log10':
                    res = math.log10(t)
                elif op == 'deg' or op == 'degree':
                    res = math.degrees(t)
                elif op == 'rad' or op == 'radian':
                    res = math.radians(t)
                elif op == 'acosh':
                    res = math.acosh(t)
                elif op == 'asinh':
                    res = math.asinh(t)
                elif op == 'atanh':
                    res = math.atanh(t)
                elif op == 'cosh':
                    res = math.cosh(t)
                elif op == 'sinh':
                    res = math.sinh(t)
                elif op == 'tanh':
                    res = math.tanh(t)
                elif op == 'max':
                    if type(t) != list:
                        res = t
                    else:
                        print t
                        res = max(t)
                elif op == 'min':
                    if type(t) != list:
                        res = t
                    else:
                        res = min(t)
                elif op == 'sum':
                    if type(t) != list:
                        res = t
                    else:
                        res = sum(t)
                elif op == 'count' or op == 'len':
                    if type(t) != list:
                        res = 1
                    else:
                        res = len(t)
                elif op == 'avg' or op == 'average':
                    if type(t) != list:
                        res = 1
                    else:
                        res = average(t)
                elif op == 'var':
                    if type(t) != list:
                        res = 0
                    else:
                        res = variance(t)
                elif op == 'varp':
                    if type(t) != list:
                        res = 0
                    else:
                        res = variance(t, True)
                elif op == 'stdev':
                    if type(t) != list:
                        res = 0
                    else:
                        res = float(variance(t)) ** .5
                elif op == 'stdevp':
                    if type(t) != list:
                        res = 0
                    else:
                        res = float(variance(t, True)) ** .5
                elif op == 'test':
                    res = 0

                res = Decimal(res)
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
                    if type(front) == list:
                        res = front + [back]
                    elif type(back) == list:
                        res = [front] + back
                    else:
                        res = [front, back]

            term_stack.append(res)
    if len(term_stack) > 1:
        raise DogBotError(u'비정상적인 인자들')

    return term_stack[0]


def main():
    pass

if __name__ == '__main__':
    main()
