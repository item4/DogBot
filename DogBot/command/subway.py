# -*- coding:utf-8 -*-

alias = [u'지하철']
handler = []

import json
import urllib
import time

from DogBot.utility.time import read_time


def cmd_subway(bot, line, args):
    if not args:
        bot.con.query(
            'PRIVMSG',
            line.target,
            u'수도권 지하철 최단노선을 검색합니다. | usage: ?지하철 서울 인천'
        )
        return
    
    if ' ' in args:
        start, end = map(lambda x:x.strip(), args.split(' ',2))
        start_id, end_id = 0, 0
    else:
        bot.con.query(
            'PRIVMSG',
            line.target,
            u'멍멍! 출발역과 도착역을 입력해주세요!'
        )
        return
    
    if start.endswith(u'역'):
        start = start[:-1]

    if end.endswith(u'역'):
        end = end[:-1]
    
    temp = urllib.urlopen('http://m.map.naver.com/external/SubwayProvide.xml?requestFile=metaData.json&readPath=1000&version=1.9').read()
    temp = temp.decode('u8')
    station_list = json.loads(temp)[0]['realInfo']
    
    for code in station_list:
        if code['name'] == start or code['name'] == start + u'역':
            start_id = code['id']
            break
        elif code['name'].startswith(start):
            start_id = code['id']

    if start_id == 0:
        bot.con.query(
            'PRIVMSG',
            line.target,
            u'멍멍! 출발역을 정상적으로 입력해주세요!'
        )
        return

    for code in station_list:
        if code['name'] == end or code['name'] == end + u'역':
            end_id = code['id']
            break
        elif code['name'].startswith(end):
            end_id = code['id']

    if end_id == 0:
        bot.con.query(
            'PRIVMSG',
            line.target,
            u'멍멍! 도착역을 정상적으로 입력해주세요!'
        )
        return
    
    if start_id == end_id:
        bot.con.query(
            'PRIVMSG',
            line.target,
            u'멍멍! 출발역과 도착역이 같아요!'
        )
        return

    temp = urllib.urlopen('http://map.naver.com/pubtrans/searchSubwayPath.nhn?serviceRegion=1000&fromStationID=' + start_id + '&toStationID=' + end_id + '&dayType=3&presetTime=3&departureDateTime=' + time.strftime('%Y%m%d%H%M%S') + '&caller=naver_map&output=json&searchType=1').read()
    temp = temp.decode('u8')

    try:
        data = json.loads(temp)['result']['subwayPaths'][0]
    except KeyError:
        bot.con.query(
            'PRIVMSG',
            line.target,
            u'멍멍! 에러가 발생했어요!'
        )
        return
    
    msg = data['path']['routes'][0]['stations'][0]['name'] + u' → ' + data['path']['routes'][-1]['stations'][-1]['name'] + \
    u' : {} 소요, 정차역 {:d}개, 환승 {:d}회, 카드 요금 {:,d}원, 현금 요금 {:,d}원'.format(read_time(data['summary']['overallTravelTimeInSecond']),data['summary']['overallNumberOfStations'], data['summary']['overallNumberOfTransfers'], data['fareInfos'][0]['fare'], data['fareInfos'][1]['fare'])
    bot.con.query(
        'PRIVMSG',
        line.target,
        msg
    )
    for route in data['path']['routes']:
        msg = route['stations'][0]['name'] + '(' + route['stations'][0]['departureTime'][:2] + ':' + route['stations'][0]['departureTime'][2:] + ')' + \
         ' ==(' + route['logicalLine']['name'] + ' ' + route['logicalLine']['direction'] + u'방면, ' + str(len(route['stations'])-1) + u'정거장)==> ' + \
         route['stations'][-1]['name'] + '(' + route['stations'][-1]['departureTime'][:2] + ':' + route['stations'][-1]['departureTime'][2:] + ')'
        if 'transfer' in route:
            msg += u' / 빠른 환승 : ' + str(route['transfer']['exitTrainNumber']) + '-' + str(route['transfer']['exitDoorNumber'])
        bot.con.query(
            'PRIVMSG',
            line.target,
            msg
        )