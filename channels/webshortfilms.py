# -*- coding: utf-8 -*-
#------------------------------------------------------------
# streamondemand.- XBMC Plugin
# Canal para webshortfilms
# http://blog.tvalacarta.info/plugin-xbmc/streamondemand.
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "webshortfilms"
__category__ = "F"
__type__ = "generic"
__title__ = "webshortfilms (IT)"
__language__ = "IT"


DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("streamondemand.webshortfilms mainlist")
    itemlist = []
    itemlist.append( Item(channel=__channel__, title="[COLOR azure]Best Streaming Shortfilms[/COLOR]", action="peliculas", url="https://webshortfilms.wordpress.com/", thumbnail="http://orig03.deviantart.net/6889/f/2014/079/7/b/movies_and_popcorn_folder_icon_by_matheusgrilo-d7ay4tw.png"))

    
    return itemlist

def peliculas(item):
    logger.info("streamondemand.webshortfilms peliculas")
    itemlist = []

    # Descarga la pagina
    data = scrapertools.cache_page(item.url)

    # Extrae las entradas (carpetas)
    patron  = '<h2 class="entry-title">\s*<a href="(.*?)"[^>]+>(.*?)<'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for scrapedurl,scrapedtitle in matches:
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle)
        response = urllib2.urlopen(scrapedurl)
        html = response.read()
        start = html.find("</iframe></span>")
        end = html.find("</a></p>", start)
        scrapedplot = html[start:end]
        scrapedplot = re.sub(r'<.*?>', '', scrapedplot)
        scrapedplot = scrapertools.decodeHtmlentities(scrapedplot)
        #scrapedplot = ""
        scrapedthumbnail = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="findvideos", fulltitle=scrapedtitle, show=scrapedtitle, title=scrapedtitle, url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )

    # Extrae el paginador
    patronvideos  = '<div class="nav-previous"><a href="(.*)" ><span class="meta-nav">&larr;'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    if len(matches)>0:
        scrapedurl = urlparse.urljoin(item.url,matches[0])
        itemlist.append( Item(channel=__channel__, action="peliculas", title="[COLOR orange]Avanti >>[/COLOR]" , url=scrapedurl , folder=True) )

    return itemlist

