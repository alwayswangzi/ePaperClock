#!/usr/bin/env python3
# coding: utf-8

import sys
import os
import re
import requests
from lxml import etree

def get_weather():
	#定义保存结果的字典
	dict = {'city_name' : u'南京'}
	'''
	city_name
	day_temp
	night_temp
	day_weather
	night_weather

	'''
	try:
		header = {'User-Agent':'AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31 Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_2) '}
		r = requests.get('http://www.nmc.gov.cn/publish/forecast/AJS/nan-jing.html', headers = header, timeout = 10)
		r.encoding = 'utf-8'
		html = r.text
		tree = etree.HTML(html)
	except Exception, e:
		print e
		sys.exit(1)

	#HTML解析

	rt = tree.xpath('//*[@id="forecast"]/div[1]/div[1]/table/tbody/tr[4]/td[1]')
	if rt:
		dict['day_temp'] = re.sub(r'\s', "", rt[0].text)
		
	rt = tree.xpath('//*[@id="forecast"]/div[1]/div[1]/table/tbody/tr[4]/td[2]')
	if rt:
		dict['night_temp'] = re.sub(r'\s', "", rt[0].text)
		
	rt = tree.xpath('//*[@id="forecast"]/div[1]/div[1]/table/tbody/tr[3]/td[1]')
	if rt:
		dict['day_weather'] = rt[0].text
		
	rt = tree.xpath('//*[@id="forecast"]/div[1]/div[1]/table/tbody/tr[3]/td[2]')
	if rt:
		dict['night_weather'] = rt[0].text
		
	rt = tree.xpath('//*[@id="forecast"]/div[1]/div[1]/table/tbody/tr[5]/td[1]')
	if rt:
		dict['wind_dir'] = rt[0].text
		
	rt = tree.xpath('//*[@id="forecast"]/div[1]/div[1]/table/tbody/tr[6]/td[1]')
	if rt:
		dict['wind_class'] = rt[0].text
		
	rt = tree.xpath('//*[@id="forecast"]/div[2]/div[2]/div[4]')
	if rt:
		dict['tomorrow_weather'] = re.sub(r'\s', "", rt[0].text)
		
	rt = tree.xpath('//*[@id="forecast"]/div[2]/div[2]/div[5]')
	if rt:
		dict['tomorrow_temp'] = re.sub(r'\s', "", rt[0].text)

	return dict
	
if __name__ == '__main__':
	ret = get_weather()
	print ret['city_name']
	print ret['real_temp']
	print ret['day_temp']
	if ret.has_key('night_temp'):
		print ret['night_temp']
	print ret['day_weather']
	if ret.has_key('night_weather'):
		print ret['night_weather']
	print ret['wind_dir']
	print ret['wind_class']
	print ret['tomorrow_weather']
	print ret['tomorrow_temp']

