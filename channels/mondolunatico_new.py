# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# streamondemand.- XBMC Plugin
# Canal para mondolunatico_new
# http://www.mimediacenter.info/foro/viewforum.php?f=36
# ------------------------------------------------------------
import re
import urlparse

from core import config
from core import logger
from core import scrapertools
from core.item import Item
from core.tmdb import infoSod

__channel__ = "mondolunatico_new"
__category__ = "F"
__type__ = "generic"
__title__ = "mondolunatico_new (IT)"
__language__ = "IT"

DEBUG = config.get_setting("debug")

host = "http://mondolunatico.org"

headers = [
    ['User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0'],
    ['Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'],
    ['Accept-Language', 'en-US,en;q=0.5'],
    ['Accept-Encoding', 'gzip, deflate']
]

DEBUG = config.get_setting("debug")

def isGeneric():
    return True


def mainlist(item):
    logger.info("streamondemand.istreaming mainlist")
    itemlist = [Item(channel=__channel__,
                     title="[COLOR azure]Ultimi Film Inseriti[/COLOR]",
                     action="peliculas",
                     url="%s/stream/movies/" % host,
                     extra="movie",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/popcorn_cinema_P.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Film Per Categoria[/COLOR]",
                     action="categorias",
                     url="%s/stream/" % host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/genres_P.png"),
                Item(channel=__channel__,
                     title="[COLOR yellow]Cerca...[/COLOR]",
                     action="search",
                     extra="movie",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/search_P.png")]

    return itemlist


def categorias(item):
    itemlist = []

    # Descarga la pagina
    data = scrapertools.cache_page(item.url, headers=headers)
    bloque = scrapertools.get_match(data, '<ul class="genres falsescroll">(.*?)</ul>')

    # Extrae las entradas (carpetas)
    patron = '<li[^>]+><a href="([^"]+)"[^>]>(.*?)<\/a>'
    matches = re.compile(patron, re.DOTALL).findall(bloque)

    for scrapedurl, scrapedtitle in matches:
        if (DEBUG): logger.info("title=[" + scrapedtitle + "], url=[" + scrapedurl + "]")
        itemlist.append(
            Item(channel=__channel__,
                 action="peliculas",
                 title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                 url=scrapedurl,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/genre_P.png",
                 folder=True))

    return itemlist


def search(item, texto):
    logger.info("[mondolunatico.py] " + item.url + " search " + texto)
    item.url = host + "/stream?s=" + texto
    try:
        if item.extra == "movie":
            return pelis_movie_src(item)
    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error("%s" % line)
        return []


def pelis_movie_src(item):
    logger.info("streamondemand.mondolunatico_new peliculas")

    itemlist = []

    # Descarga la pagina
    data = scrapertools.cache_page(item.url, headers=headers)

    # Extrae las entradas (carpetas)
    patron = '<div class="thumbnail animation-2">\s*<a href="([^"]+)">\s*<img src="([^"]+)" alt="(.*?)" />'
    matches = re.compile(patron, re.DOTALL).findall(data)

    scrapedplot = ""
    for scrapedurl, scrapedthumbnail, scrapedtitle, in matches:
        title = scrapertools.decodeHtmlentities(scrapedtitle)
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 extra=item.extra,
                 action="findvideos",
                 title=title,
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 fulltitle=title,
                 show=title,
                 plot=scrapedplot,
                 folder=True), tipo='movie'))

    return itemlist

def peliculas(item):
    logger.info("streamondemand.mondolunatico_new peliculas")

    itemlist = []

    # Descarga la pagina
    data = scrapertools.cache_page(item.url, headers=headers)

    # Extrae las entradas (carpetas)
    patron = '<div class="poster">\s*<a href="(.*?)"><img src="(.*?)" alt="(.*?)">'
    matches = re.compile(patron, re.DOTALL).findall(data)

    scrapedplot = ""
    for scrapedurl, scrapedthumbnail, scrapedtitle, in matches:
        title = scrapertools.decodeHtmlentities(scrapedtitle)
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 extra=item.extra,
                 action="findvideos",
                 title=title,
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 fulltitle=title,
                 show=title,
                 plot=scrapedplot,
                 folder=True), tipo='movie'))

    # Extrae el paginador
    patronvideos = '<span class="current">[^<]+<\/span><a href=\'(.*?)\''
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    if len(matches) > 0:
        scrapedurl = urlparse.urljoin(item.url, matches[0])
        itemlist.append(
            Item(channel=__channel__,
                 action="HomePage",
                 title="[COLOR yellow]Torna Home[/COLOR]",
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

