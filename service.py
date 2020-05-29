# -*- coding: utf-8 -*-

import xbmc
import xbmcaddon

properties = [
	'context.trailer.autoplay',
	'context.trailer.selectplay']


class PropertiesUpdater(xbmc.Monitor):
	def __init__(self):
		for id in properties:
			if xbmcaddon.Addon().getSetting(id) == 'true':
				xbmc.executebuiltin('SetProperty({0},true,home)'.format(id))
				xbmc.log('Context menu item enabled: {0}'.format(id),xbmc.LOGNOTICE)


	def onSettingsChanged(self):
		for id in properties:
			if xbmcaddon.Addon().getSetting(id) == 'true':
				xbmc.executebuiltin('SetProperty({0},true,home)'.format(id))
				xbmc.log('Context menu item enabled: {0}'.format(id),xbmc.LOGNOTICE)
			else:
				xbmc.executebuiltin('ClearProperty({0},home)'.format(id))
				xbmc.log('Context menu item disabled: {0}'.format(id),xbmc.LOGNOTICE)


# start monitoring settings changes events
xbmc.log('Context.Trailer: service started', xbmc.LOGNOTICE)
properties_monitor = PropertiesUpdater()

# wait until abort is requested
properties_monitor.waitForAbort()
xbmc.log('Context.Trailer: service stopped',xbmc.LOGNOTICE)
