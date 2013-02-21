# -*- coding: utf-8 -*-

def read_time(_time):
    _time = _time
    day, _time = divmod(_time,86400)
    hour, _time = divmod(_time,3600)
    minute, second = divmod(_time,60)
    temp = []
    if day:
        temp.append(str(int(day))+u'일')
    if hour:
        temp.append(str(int(hour))+u'시간')
    if minute:
        temp.append(str(int(minute))+u'분')
    if second or (not day and not hour and not minute):
        temp.append(str(int(second))+u'초')

    return ' '.join(temp)

def main():
    pass

if __name__ == '__main__':
    main()
