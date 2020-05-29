# -*- coding: utf-8 -*-

import sys
import xbmc
import xbmcaddon

from resources.lib.modules import trailer

ADDON = xbmcaddon.Addon()

if __name__ == '__main__':
	windowed = ADDON.getSetting("windowed") == "true"

	info = sys.listitem.getVideoInfoTag()
	type = info.getMediaType()
	name =info.getTitle()
	year = info.getYear()
	imdb = info.getIMDBNumber()

	trailer.Trailer().play(type, name, year, imdb, windowedtrailer=1 if windowed else 0)