#!/usr/bin/env python
# coding: utf-8

import epd4in2
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from get_datetime import get_datetime
from get_weather import get_weather
import time
import os
import sys

def str2icon(str):
	icon = None
	if str == u'晴' :
		icon = 'A'
	elif str == u'多云' :
		icon = 'C'
	elif str == u'阴' :
		icon = 'D'
	elif str == u'阵雨' :
		icon = 'F'
	elif str == u'雷阵雨' :
		icon = 'U'
	elif str == u'雨夹雪' :
		icon = 'X'
	elif str == u'小雨' :
		icon = 'R'
	elif str == u'中雨' :
		icon = 'R'
	elif str == u'大雨' :
		icon = 'S'
	elif str == u'暴雨' :
		icon = 'S'
	elif str == u'大暴雨' :
		icon = 'S'
	elif str == u'小雪' :
		icon = 'W'
	elif str == u'中雪' :
		icon = 'W'
	elif str == u'大雪' :
		icon = 'W'
	elif str == u'暴雪' :
		icon = 'W'
	elif str == u'雾' :
		icon = 'N'
	elif str == u'霾' :
		icon = 'N'
	else :
		icon = 'A'
	
	return icon

def main():
	# 电子墨水屏初始化
	epd = epd4in2.EPD()
	epd.init()
	# 创建空图像
	image = Image.new('1', (400, 300), 1)
	draw = ImageDraw.Draw(image)
	# 主屏幕上下分割线
	draw.line([0, 100, 399, 100], fill = 0, width = 2)
	# 定义字体格式
	font_calibril_super = ImageFont.truetype('/usr/share/fonts/song/calibril', 90)
	font_song_small = ImageFont.truetype('/usr/share/fonts/song/simsun', 24)
	font_song_mid = ImageFont.truetype('/usr/share/fonts/song/simsun', 28)
	font_song_large = ImageFont.truetype('/usr/share/fonts/song/simsun', 40)
	font_icon = ImageFont.truetype('/usr/share/fonts/Weather&Time', 86)
	font_icon_mid = ImageFont.truetype('/usr/share/fonts/Weather&Time', 36)
	draw.ink = 256 + 256*256 + 256*256*256

	# 计数君
	count = 0

	while True:
		# 清空上半部分显示区域
		draw.rectangle([0, 0, 399, 98], fill = 'white')
		
		# 获取日期时间
		datetime = get_datetime()
		draw.text([0, 10], datetime['time'], font = font_calibril_super)
		draw.text([250, 10], datetime['date'], font = font_song_small)
		draw.text([250, 40], datetime['week'], font = font_song_small)
		draw.text([250, 70], u'农历' + '', font = font_song_small)
		
		# 获取室内温度
		temp = 20
                wet = 70
		draw.text([200, 110], 'k', font = font_icon_mid)
		draw.text([225, 120], str(temp) + u'℃', font = font_song_large)
		draw.text([300, 105], 'j', font = font_icon_mid)
		draw.text([325, 120], str(wet) + u'％', font = font_song_large)

		if(count == 0):
			#清空下半部分显示区域
			draw.rectangle([0, 102, 199, 299], fill = 'white')
			draw.rectangle([200, 230, 399, 299], fill = 'white')
			
			try:
				# 获取天气状况
				weather = get_weather()
				draw.text([100, 130], weather['city_name'], font = font_song_small)
				#draw.text([230, 170], weather['real_temp'], font = font_song_large)
				draw.text([100, 160], u'今日', font = font_song_small)
				draw.text([10, 110], str2icon(weather['day_weather']), font = font_icon)
				draw.line([53, 240, 53, 290], fill = 0)
				if weather.has_key('night_weather'):
					draw.text([20, 200], weather['day_weather'] + u'/' + weather['night_weather'], font = font_song_mid)
				else:
					draw.text([20, 200], weather['day_weather'], font = font_song_mid)
				if weather.has_key('night_temp'):
					draw.text([0, 240], u'气温 ' + weather['day_temp'] + u'/' + weather['night_temp'], font = font_song_small)
				else:
					draw.text([0, 240], u'气温 ' + weather['day_temp'], font = font_song_small)
				draw.text([0, 270], u'风力 ' + weather['wind_dir'] + weather['wind_class'], font = font_song_small)
				draw.line([293, 240, 293, 290], fill = 0)
				draw.text([240, 240], u'明日 ' + weather['tomorrow_weather'], font = font_song_small)
				draw.text([240, 270], u'天气 ' + weather['tomorrow_temp'], font = font_song_small)
			except Exception, e:
				print e
				draw.rectangle([0, 102, 399, 299], fill = 'white')
				draw.text([0, 200], u'数据获取失败！请检查网络连接！', font = font_song_small)
				epd.display_frame(epd.get_frame_buffer(image))
				#sys.exit(1)

		++count
		if(count == 20):
			count = 0

		epd.display_frame(epd.get_frame_buffer(image))
		time.sleep(60)


if __name__ == '__main__':
	main()
