#!/usr/bin/env python
# coding: utf-8

import datetime

def get_datetime():
    dict = {}
    time_now = datetime.datetime.now()
    dict['time'] = time_now.strftime('%H:%M')
    dict['date'] = time_now.strftime('%Y-%m-%d')
    dict['week'] = [u'星期一',u'星期二',u'星期三',u'星期四',u'星期五',u'星期六',u'星期日'][time_now.isoweekday() - 1]
    if dict['time'][0] == '0':
        dict['time'] = dict['time'][1:]

    return dict
