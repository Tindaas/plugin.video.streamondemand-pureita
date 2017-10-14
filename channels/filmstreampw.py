# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# StreamOnDemand-PureITA / XBMC Plugin
# Canale filmstreampw
# http://www.mimediacenter.info/foro/viewtopic.php?f=36&t=7808
# ------------------------------------------------------------
import re
import urlparse

from core import config
from core import logger
from core import scrapertools
from core import servertools
from core.item import Item
from core.tmdb import infoSod

__channel__ = "filmstreampw"
__category__ = "F"
__type__ = "generic"
__title__ = "Fimstream.pw (IT)"
__language__ = "IT"

headers = [
    ['User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:38.0) Gecko/20100101 Firefox/38.0'],
    ['Accept-Encoding', 'gzip, deflate']
]

host = 'http://beststreaming.info/'

DEBUG = config.get_setting("debug")


def isGeneric():
    return True


def mainlist(item):
    logger.info("streamondemand.filmstreampw mainlist")
    itemlist = [Item(channel=__channel__,
                     title="[COLOR azure]Ultimi Film Inseriti[/COLOR]",
                     action="peliculas",
                     url=host + "/film/",
                     extra="movie",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/popcorn_cinema_P.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Film Per Genere[/COLOR]",
                     action="categorias",
                     url=host,
                     extra="movie",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/genres_P.png"),
                Item(channel=__channel__,
                     title="[COLOR yellow]Cerca...[/COLOR]",
                     action="search",
                     extra="movie",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/search_P.png")]
    return itemlist


def categorias(item):
    logger.info("streamondemand.filmstreampw categorias")
    itemlist = []

    data = scrapertools.cache_page(item.url, headers=headers)

    # Narrow search by selecting only the combo
    patron = '<ul class="box-bg right-navi clearfix">([^?]+)</select>'
    bloque = scrapertools.get_match(data, patron)

    # The categories are the options for the combo
    patron = '<li><a href="([^"]+)">(.*?)</a></li>'
    matches = re.compile(patron, re.DOTALL).findall(bloque)

    for scrapedurl, scrapedtitle in matches:
        scrapedurl = urlparse.urljoin(item.url, scrapedurl)
        scrapedthumbnail = ""
        scrapedplot = ""
        if (DEBUG): logger.info(
            "title=[" + scrapedtitle + "], url=[" + scrapedurl + "], thumbnail=[" + scrapedthumbnail + "]")
        itemlist.append(
            Item(channel=__channel__,
                 action="peliculas",
                 extra=item.extra,
                 title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 plot=scrapedplot))

    return itemlist


def search(item, texto):
    logger.info("[filmstreampw.py] " + item.url + " search " + texto)
    item.url = host + "/index.php?do=search&subaction=search&story=" + texto

    try:
        if item.extra == "movie":
            return peliculasx(item)
        if item.extra == "serie":
            return peliculasx_tv(item)

    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error("%s" % line)
        return []


def peliculasx(item):
    logger.info("streamondemand.filmstreampw peliculas")
    itemlist = []

    # Descarga la pagina
    data = scrapertools.cache_page(item.url, headers=headers)

    # Extrae las entradas (carpetas)
    patron = '<div class="news2 float">.*?<div class="boxgrid2 caption2">.*?<a href="([^"]+)">.*?<img.*?src="([^"]+)"/>.*?<div class="cover2 boxcaption2">.*?<div class="boxgridtext">(.*?)</div>.*?<br>'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedthumbnail, scrapedtitle in matches:
        html = scrapertools.cache_page(scrapedurl, headers=headers)
        start = html.find("<li class=\"current\" style=\"font-size: 15px; line-height: 18px;\">")
        end = html.find("</div></li>", start)
        scrapedplot = html[start:end]
        scrapedplot = re.sub(r'<[^>]*>', '', scrapedplot)
        scrapedplot = scrapertools.decodeHtmlentities(scrapedplot)
        scrapedtitle = scrapedtitle.strip()
        if (DEBUG): logger.info(
            "title=[" + scrapedtitle + "], url=[" + scrapedurl + "], thumbnail=[" + scrapedthumbnail + "]")
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 extra=item.extra,
                 action="episodios" if item.extra == "serie" else "findvideos",
                 fulltitle=scrapedtitle,
                 show=scrapedtitle,
                 title=scrapedtitle,
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 plot=scrapedplot,
                 folder=True), tipo='movie'))

    return itemlist


def peliculas(item):
    logger.info("streamondemand.filmstreampw peliculas")
    itemlist = []

    # Descarga la pagina
    data = scrapertools.cache_page(item.url, headers=headers)

    # Extrae las entradas (carpetas)
    patron = '<div class="boxgrid2[^>]+>[^<]+<a href="([^"]+)">[^<]+<img.*?[^"]+"[^"]+" src="([^"]+)"[^>]+>[^>]+>[^>]+>([^<]+)<br>'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedthumbnail, scrapedtitle in matches:
        scrapedplot = ""
        scrapedtitle = scrapedtitle.strip()
        if (DEBUG): logger.info(
            "title=[" + scrapedtitle + "], url=[" + scrapedurl + "], thumbnail=[" + scrapedthumbnail + "]")
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 extra=item.extra,
                 action="findvideos",
                 fulltitle=scrapedtitle,
                 show=scrapedtitle,
                 title=scrapedtitle,
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 plot=scrapedplot,
                 folder=True), tipo='movie'))

    # Extrae el paginador
    patronvideos = '<a href="([^"]+)">Avanti</a>'
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    if len(matches) > 0:
        scrapedurl = urlparse.urljoin(item.url, matches[0])
        itemlist.append(
            Item(channel=__channel__,
                 action="HomePage",
                 title="[COLOR yellow]Torna Home[/COLOR]",
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/return_home_P.png",
                 folder=True)),
        itemlist.append(
            Item(channel=__channel__,
                 extra=item.extra,
                 action="peliculas",
                 title="[COLOR orange]Successivo >>[/COLOR]",
                 url=scrapedurl,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/successivo_P.png",
                 folder=True))

    return itemlist



def HomePage(item):
    import xbmc
    xbmc.executebuiltin("ReplaceWindow(10024,plugin://plugin.video.streamondemand-pureita-master)")


def findvideos(item):
    logger.info("streamondemand.filmstreampw findvideos")

    data = scrapertools.cache_page(item.url, headers=headers)

    itemlist = servertools.find_video_items(data=data.replace(r'\/', '/'))

    for videoitem in itemlist:
        videoitem.title = item.title + videoitem.title.replace("-", "|")
        videoitem.fulltitle = item.fulltitle
        videoitem.thumbnail = item.thumbnail
        videoitem.show = item.show
        videoitem.plot = item.plot
        videoitem.channel = __channel__

    return itemlist
