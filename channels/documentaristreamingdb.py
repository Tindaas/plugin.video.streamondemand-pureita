# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# streamondemand.- XBMC Plugin
# Canal para documentaristreamingdb
# http://www.mimediacenter.info/foro/viewforum.php?f=36
# ------------------------------------------------------------
import re
import urlparse

from core import config
from core import logger
from core import scrapertools
from core.item import Item
from core.tmdb import infoSod

__channel__ = "documentaristreamingdb"
__category__ = "D"
__type__ = "generic"
__title__ = "documentaristreamingdb (IT)"
__language__ = "IT"

DEBUG = config.get_setting("debug")

host = "http://www.documentari-streaming-db.com"

headers = [
    ['User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0'],
    ['Accept-Encoding', 'gzip, deflate']
]


def isGeneric():
    return True


def mainlist(item):
    logger.info("streamondemand.istreaming mainlist")
    itemlist = [Item(channel=__channel__,
                     title="[COLOR azure]Aggiornamenti[/COLOR]",
                     action="peliculas",
                     url="%s/?searchtype=movie&post_type=movie&s=" % host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/popcorn_cinema_P.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Categorie[/COLOR]",
                     action="categorias",
                     url=host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/genres_P.png"),
                Item(channel=__channel__,
                     title="[COLOR yellow]Cerca...[/COLOR]",
                     action="search",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/search_P.png")]

    return itemlist


def categorias(item):
    itemlist = []

    # Descarga la pagina
    data = scrapertools.cache_page(item.url, headers=headers)
    bloque = scrapertools.get_match(data, '<ul role="menu" class="collapse collapse-1156">(.*?)</ul>')

    # Extrae las entradas (carpetas)
    patron = '<li[^>]+><a[^h]+href="([^"]+)">(.*?)</a>'
    matches = re.compile(patron, re.DOTALL).findall(bloque)

    for scrapedurl, scrapedtitle in matches:
        if (DEBUG): logger.info("title=[" + scrapedtitle + "], url=[" + scrapedurl + "]")
        
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle.replace("Documentari ", ""))
        if scrapedtitle.startswith(("Tutte")):
            continue
        
        itemlist.append(
            Item(channel=__channel__,
                 action="peliculas",
                 title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                 url=scrapedurl,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/genre_P.png",
                 folder=True))

    return itemlist


def search(item, texto):
    logger.info("[strfilm.py] " + item.url + " search " + texto)
    item.url = host + "/?searchtype=movie&post_type=movie&s=" + texto
    try:
        return peliculas(item)
    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error("%s" % line)
        return []

def peliculas(item):
    logger.info("streamondemand.documentaristreamingdb peliculas")
    itemlist = []

    # Descarga la pagina
    data = scrapertools.cache_page(item.url, headers=headers)

    # Extrae las entradas (carpetas)
    patron = '<div class="movie-poster">\s*<img[^s]+src="(.*?)"[^=]+=[^=]+="(.*?)"[^>]+>\s*<a[^h]+href="(.*?)">'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedthumbnail, scrapedtitle, scrapedurl in matches:
        #html = scrapertools.cache_page(scrapedurl)
        #start = html.find("</div><h2>")
        #end = html.find("<p><strong>", start)
        #scrapedplot = html[start:end]
        #scrapedplot = re.sub(r'<[^>]*>', '', scrapedplot)
        #scrapedplot = scrapertools.decodeHtmlentities(scrapedplot)
        scrapedplot = ""
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle.replace("Serie Documentari ", ""))
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle.replace("Documentario ", ""))
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle.replace("Documentari ", ""))
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle.replace("streaming", " "))
        scrapedtitle = scrapedtitle.split('"')[0]
        if DEBUG: logger.info(
            "title=[" + scrapedtitle + "], url=[" + scrapedurl + "], thumbnail=[" + scrapedthumbnail + "]")
        itemlist.append(
            Item(channel=__channel__,
                 action="findvideos",
                 fulltitle=scrapedtitle,
                 show=scrapedtitle,
                 title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                 url=scrapedurl,
                 viewmode="movie_with_plot",
                 thumbnail=scrapedthumbnail,
                 plot=scrapedplot,
                 folder=True))

    # Extrae el paginador
    patronvideos = '<a class="next page-numbers" href="(.*?)">'
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
                 action="peliculas",
                 title="[COLOR orange]Successivo >>[/COLOR]",
                 url=scrapedurl,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/successivo_P.png",
                 folder=True))

    return itemlist


def HomePage(item):
    import xbmc
    xbmc.executebuiltin("ReplaceWindow(10024,plugin://plugin.video.streamondemand-pureita-master)")
