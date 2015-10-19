# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# streamondemand - XBMC Plugin
# Canal para streamingfilmit
# http://blog.tvalacarta.info/plugin-xbmc/streamondemand/
# ------------------------------------------------------------
import urlparse
import re
import sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "streamingfilmit"
__category__ = "F"
__type__ = "generic"
__title__ = "Streamingfilmit.com (IT)"
__language__ = "IT"

DEBUG = config.get_setting("debug")

host = "http://www.streamingfilmit.com"

headers = [
    ['User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:38.0) Gecko/20100101 Firefox/38.0'],
    ['Accept-Encoding', 'gzip, deflate'],
    ['Referer', host],
    ['Connection', 'keep-alive']
]


def isGeneric():
    return True


def mainlist(item):
    logger.info("streamondemand.streamingfilmit mainlist")
    itemlist = [Item(channel=__channel__,
                     title="[COLOR azure]Ultimi Film Inseriti[/COLOR]",
                     action="peliculas",
                     url=host,
                     thumbnail="http://dc584.4shared.com/img/XImgcB94/s7/13feaf0b538/saquinho_de_pipoca_01"),
                Item(channel=__channel__,
                     title="[COLOR azure]Film Per Categoria[/COLOR]",
                     action="categorias",
                     url=host,
                     thumbnail="http://xbmc-repo-ackbarr.googlecode.com/svn/trunk/dev/skin.cirrus%20extended%20v2/extras/moviegenres/All%20Movies%20by%20Genre.png"),
                Item(channel=__channel__,
                     title="[COLOR yellow]Cerca...[/COLOR]",
                     action="search",
                     thumbnail="http://dc467.4shared.com/img/fEbJqOum/s7/13feaf0c8c0/Search")]

    return itemlist


def categorias(item):
    itemlist = []

    # Descarga la pagina
    data = scrapertools.cache_page(item.url, headers=headers)
    bloque = scrapertools.get_match(data, '<ul>(.*?)</ul>')

    # Extrae las entradas (carpetas)
    patron = '<a href="([^"]+)" >(.*?)</a>(.*?)\s*</li>'
    matches = re.compile(patron, re.DOTALL).findall(bloque)

    for scrapedurl, scrapedtitle, scrapedtot in matches:
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle.replace("Animazione", ""))
        scrapedurl = scrapertools.decodeHtmlentities(scrapedurl.replace("%s/category/animazione/" % host, ""))
        if DEBUG: logger.info("title=[" + scrapedtitle + "], url=[" + scrapedurl + "]")
        itemlist.append(
            Item(channel=__channel__,
                 action="pelicat",
                 title="[COLOR azure]" + scrapedtitle + "[/COLOR][COLOR gray]" + scrapedtot + "[/COLOR]",
                 url=scrapedurl,
                 thumbnail="http://xbmc-repo-ackbarr.googlecode.com/svn/trunk/dev/skin.cirrus%20extended%20v2/extras/moviegenres/All%20Movies%20by%20Genre.png",
                 folder=True))

    return itemlist


def search(item, texto):
    logger.info("[streamingfilmit.py] " + item.url + " search " + texto)
    item.url = host + "/?s=" + texto
    try:
        return peliculas(item)
    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error("%s" % line)
        return []


def peliculas(item):
    logger.info("streamondemand.streamingfilmit peliculas")
    itemlist = []

    # Descarga la pagina
    data = scrapertools.cache_page(item.url, headers=headers)

    # Extrae las entradas (carpetas)
    patron = '<a title="([^"]+)" href="([^"]+)">\s*'
    patron += '<[^>]+>\s*'
    patron += '<[^>]+>\s*'
    patron += '<img[^=]+=[^=]+=[^=]+="([^"]+)"[^>]+>'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedtitle, scrapedurl, scrapedthumbnail in matches:
        html = scrapertools.cache_page(scrapedurl, headers=headers)
        start = html.find("<div id=\"detay-aciklama\">")
        end = html.find("</p>", start)
        scrapedplot = html[start:end]
        scrapedplot = re.sub(r'<[^>]*>', '', scrapedplot)
        scrapedplot = scrapertools.decodeHtmlentities(scrapedplot)
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle)
        if DEBUG: logger.info(
            "title=[" + scrapedtitle + "], url=[" + scrapedurl + "], thumbnail=[" + scrapedthumbnail + "]")
        itemlist.append(
            Item(channel=__channel__,
                 action="findvideos",
                 fulltitle=scrapedtitle,
                 show=scrapedtitle,
                 title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 plot=scrapedplot,
                 folder=True))

    # Extrae el paginador
    patronvideos = '<a class="nextpostslink" rel="next" href="([^"]+)">&raquo;</a>'
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    if len(matches) > 0:
        scrapedurl = urlparse.urljoin(item.url, matches[0])
        itemlist.append(
            Item(channel=__channel__,
                 action="peliculas",
                 title="[COLOR orange]Successivo>>[/COLOR]",
                 url=scrapedurl,
                 thumbnail="http://2.bp.blogspot.com/-fE9tzwmjaeQ/UcM2apxDtjI/AAAAAAAAeeg/WKSGM2TADLM/s1600/pager+old.png",
                 folder=True))

    return itemlist


def pelicat(item):
    logger.info("streamondemand.streamingfilmit pelicat")
    itemlist = []

    # Descarga la pagina
    data = scrapertools.cache_page(item.url, headers=headers)

    # Extrae las entradas (carpetas)
    patron = '<div class="kapsa">\s*'
    patron += '<a href="([^"]+)">\s*'
    patron += '<[^>]+>\s*'
    patron += '<[^>]+>\s*'
    patron += '<img[^=]+=[^=]+=[^=]+="([^"]+)"[^>]+>\s*'
    patron += '<[^>]+>\s*'
    patron += '<[^>]+>\s*'
    patron += '[^>]+>[^>]+>[^>]+>[^>]+>[^>]+>[^>]+>[^>]+>[^>]+>\s*'
    patron += '<[^>]+>\s*'
    patron += '<[^>]+>\s*'
    patron += '<h4><a[^>]+>(.*?)</a></h4>'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedthumbnail, scrapedtitle in matches:
        html = scrapertools.cache_page(scrapedurl, headers=headers)
        start = html.find("<div id=\"detay-aciklama\">")
        end = html.find("</p>", start)
        scrapedplot = html[start:end]
        scrapedplot = re.sub(r'<[^>]*>', '', scrapedplot)
        scrapedplot = scrapertools.decodeHtmlentities(scrapedplot)
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle)
        if DEBUG: logger.info(
            "title=[" + scrapedtitle + "], url=[" + scrapedurl + "], thumbnail=[" + scrapedthumbnail + "]")
        itemlist.append(
            Item(channel=__channel__,
                 action="findvideos",
                 fulltitle=scrapedtitle,
                 show=scrapedtitle,
                 title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 plot=scrapedplot,
                 folder=True))

    # Extrae el paginador
    patronvideos = '<a class="nextpostslink" rel="next" href="([^"]+)">&raquo;</a>'
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    if len(matches) > 0:
        scrapedurl = urlparse.urljoin(item.url, matches[0])
        itemlist.append(
            Item(channel=__channel__,
                 action="pelicat",
                 title="[COLOR orange]Successivo>>[/COLOR]",
                 url=scrapedurl,
                 thumbnail="http://2.bp.blogspot.com/-fE9tzwmjaeQ/UcM2apxDtjI/AAAAAAAAeeg/WKSGM2TADLM/s1600/pager+old.png",
                 folder=True))

    return itemlist


def findvideos(item):
    logger.info("streamondemand.streamingfilmit findvideos")

    itemlist = []

    # Descarga la página
    data = scrapertools.cache_page(item.url, headers=headers)

    # Extrae las entradas
    patron = r'<td><a(?:\s*target="_blank"\s*rel="nofollow")?\s*href="([^"]+)"\s*(?:target="_blank")?>([^<]+)</a></td>'
    matches = re.compile(patron, re.DOTALL).findall(data)
    for scrapedurl, scrapedtitle in matches:
        title = item.title + " - " + scrapedtitle
        itemlist.append(
            Item(channel=__channel__,
                 action="play",
                 title=title,
                 url=scrapedurl,
                 fulltitle=item.fulltitle,
                 show=item.show,
                 folder=False))

    return itemlist


def play(item):
    logger.info("streamondemand.streamingfilmit play")

    data = scrapertools.cache_page(item.url, headers=headers)
    data = scrapertools.decodeHtmlentities(data).replace('http://cineblog01.pw', 'http://k4pp4.pw')

    url = scrapertools.find_single_match(data, r'<meta http-equiv="refresh" content="\d+;\s*url=([^"]+)"')

    data = scrapertools.cache_page(url, headers=headers)

    if "go.php" in url:
        try:
            data = scrapertools.get_match(data, 'window.location.href = "([^"]+)";')
        except IndexError:
            data = scrapertools.get_match(data, r'<a href="([^"]+)" class="btn-wrapper">Clicca per proseguire</a>')
    elif "/link/" in url:
        from lib.jsbeautifier.unpackers import packer
        try:
            data = scrapertools.get_match(data, "(eval.function.p,a,c,k,e,.*?)</script>")
            data = packer.unpack(data)
        except IndexError:
            pass

        data = scrapertools.get_match(data, 'var link(?:\s)?=(?:\s)?"([^"]+)";')
    else:
        data = url

    itemlist = servertools.find_video_items(data=data)

    for videoitem in itemlist:
        videoitem.title = item.show
        videoitem.show = item.show
        videoitem.fulltitle = item.fulltitle
        videoitem.thumbnail = item.thumbnail
        videoitem.channel = __channel__

    return itemlist
