# -*- coding: utf-8 -*-

import json
import random
import re
import traceback
import urllib2
import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin

try:
	from urllib import quote_plus
except:
	from urllib.parse import quote_plus

from resources.lib.modules import tools


class Trailer:
	def __init__(self):
		self.base_link = 'https://www.youtube.com'
		self.key = xbmcaddon.Addon('plugin.video.youtube').getSetting('youtube.api.key')
		if self.key == '': self.key = random.choice([
			'AIzaSyA0LiS7G-KlrlfmREcCAXjyGqa_h_zfrSE',
			'AIzaSyDgcri5Aipa9EBeE48IJAYyd71aiPOpwWw',
			'AIzaSyBOXZVC-xzrdXSAmau5UM3rG7rc8eFIuFw'])
		try:
			self.key_link = '&key=%s' % self.key
		except:
			pass
		self.search_link = 'https://www.googleapis.com/youtube/v3/search?part=snippet&type=video&maxResults=15&q=%s' + self.key_link
		self.youtube_watch = 'https://www.youtube.com/watch?v=%s'


	def play(self, type='', name='', year='', url='', imdb='', windowedtrailer=0):
		tools.busy()
		try:
			url = self.worker(type, name, year, url, imdb)
			if not url:
				return
			xbmc.executebuiltin("PlayMedia(%s)" % (url))
			if windowedtrailer == 1:
				xbmc.sleep(100)
				while xbmc.Player().isPlayingVideo():
					xbmc.sleep(100)
				xbmc.executebuiltin("Dialog.Close(%s, true)" % xbmcgui.getCurrentWindowDialogId())
		except:
			traceback.print_exc()

	def worker(self, type, name, year, url, imdb):
		try:
			if url.startswith(self.base_link):
				url = self.resolve(url)
				if not url:
					raise Exception()
				return url
			elif not url.startswith('http'):
				url = self.youtube_watch % url
				url = self.resolve(url)
				if not url:
					raise Exception()
				return url
			else:
				raise Exception()
		except:
			# traceback.print_exc()
			query = name + ' ' + str(year) + ' trailer'
			query = self.search_link % quote_plus(query)
			return self.search(query, type, name, year, imdb)


	def search(self, url, type, name, year, imdb):
		try:
			apiLang = tools.apiLanguage().get('youtube', 'en')
			if apiLang != 'en':
				url += "&relevanceLanguage=%s" % apiLang

			result = urllib2.urlopen(url).read()
			json_items = json.loads(result).get('items', [])
			items = [i.get('id', {}).get('videoId') for i in json_items]

			labels = [i.get('snippet', {}).get('title') for i in json_items]
			labels = [tools.replaceHTMLCodes(i) for i in labels]
			tools.hide()
			select = xbmcgui.Dialog().select('YOUTUBE TRAILERS:', labels)
			if select == -1: return
			items = [items[select]]

			# if 'error' in result:
				# items = json.loads(result).get('error', []).get('errors', [])
				# # log_utils.log('message = %s' % str(items[0].get('message')), __name__, log_utils.LOGDEBUG)

			for vid_id in items:
				url = self.resolve(vid_id)
				xbmc.log('url = %s' % url, 2)
				if url:
					return url
		except:
			traceback.print_exc()
			return


	def resolve(self, url):
		try:
			id = url.split('?v=')[-1].split('/')[-1].split('?')[0].split('&')[0]
			result = urllib2.urlopen(self.youtube_watch % id).read()
			message = tools.parseDOM(result, 'div', attrs={'id': 'unavailable-submessage'})
			message = ''.join(message)
			alert = tools.parseDOM(result, 'div', attrs={'id': 'watch7-notification-area'})
			if len(alert) > 0:
				return
			if re.search('[a-zA-Z]', message):
				return
			url = 'plugin://plugin.video.youtube/play/?video_id=%s' % id
			return url
		except:
			traceback.print_exc()
			# log_utils.error()
			return