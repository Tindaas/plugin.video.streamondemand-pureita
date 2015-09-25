# -*- coding: utf-8 -*-
#------------------------------------------------------------
# streamondemand - XBMC Plugin
# Ricerca "Biblioteca"
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os, sys
import time

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "biblioteca"
__category__ = "F"
__type__ = "generic"
__title__ = "Biblioteca"
__language__ = "IT"

host = "http://altadefinizione.co"

headers = [
    ['User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:38.0) Gecko/20100101 Firefox/38.0'],
    ['Accept-Encoding', 'gzip, deflate'],
    ['Referer', 'http://altadefinizione.co/'],
    ['Connection', 'keep-alive']
]

DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("streamondemand.biblioteca mainlist")
    itemlist = []
    itemlist.append( Item(channel=__channel__, title="Film per Registi [A]", action="cat_registi_A", url="http://altadefinizione.co/registi/", thumbnail="http://cinema.clubefl.gr/wp-content/themes/director-theme/images/logo.png"))
    itemlist.append( Item(channel=__channel__, title="Film per Registi [B C D]", action="cat_registi_B_C_D", url="http://altadefinizione.co/registi/", thumbnail="http://cinema.clubefl.gr/wp-content/themes/director-theme/images/logo.png"))
    itemlist.append( Item(channel=__channel__, title="Film per Registi [E F]", action="cat_registi_E_F", url="http://altadefinizione.co/registi/", thumbnail="http://cinema.clubefl.gr/wp-content/themes/director-theme/images/logo.png"))
    itemlist.append( Item(channel=__channel__, title="Film per Registi [G]", action="cat_registi_G", url="http://altadefinizione.co/registi/", thumbnail="http://cinema.clubefl.gr/wp-content/themes/director-theme/images/logo.png"))
    itemlist.append( Item(channel=__channel__, title="Film per Registi [H I]", action="cat_registi_H_I", url="http://altadefinizione.co/registi/", thumbnail="http://cinema.clubefl.gr/wp-content/themes/director-theme/images/logo.png"))
    itemlist.append( Item(channel=__channel__, title="Film per Registi [J]", action="cat_registi_J", url="http://altadefinizione.co/registi/", thumbnail="http://cinema.clubefl.gr/wp-content/themes/director-theme/images/logo.png"))
    itemlist.append( Item(channel=__channel__, title="Film per Registi [K L]", action="cat_registi_K_L", url="http://altadefinizione.co/registi/", thumbnail="http://cinema.clubefl.gr/wp-content/themes/director-theme/images/logo.png"))
    itemlist.append( Item(channel=__channel__, title="Film per Registi [M]", action="cat_registi_M", url="http://altadefinizione.co/registi/", thumbnail="http://cinema.clubefl.gr/wp-content/themes/director-theme/images/logo.png"))
    itemlist.append( Item(channel=__channel__, title="Film per Registi [N O P]", action="cat_registi_N_O_P", url="http://altadefinizione.co/registi/", thumbnail="http://cinema.clubefl.gr/wp-content/themes/director-theme/images/logo.png"))
    itemlist.append( Item(channel=__channel__, title="Film per Registi [Q R]", action="cat_registi_Q_R", url="http://altadefinizione.co/registi/", thumbnail="http://cinema.clubefl.gr/wp-content/themes/director-theme/images/logo.png"))
    itemlist.append( Item(channel=__channel__, title="Film per Registi [S]", action="cat_registi_S", url="http://altadefinizione.co/registi/", thumbnail="http://cinema.clubefl.gr/wp-content/themes/director-theme/images/logo.png"))
    itemlist.append( Item(channel=__channel__, title="Film per Registi [T U V]", action="cat_registi_T_U_V", url="http://altadefinizione.co/registi/", thumbnail="http://cinema.clubefl.gr/wp-content/themes/director-theme/images/logo.png"))
    itemlist.append( Item(channel=__channel__, title="Film per Registi [W X Y Z]", action="cat_registi_W_X_Y_Z", url="http://altadefinizione.co/registi/", thumbnail="http://cinema.clubefl.gr/wp-content/themes/director-theme/images/logo.png"))
    #itemlist.append( Item(channel=__channel__, title="Film per Attori/Attrici", action="cat_attori", url="http://altadefinizione.co/attori/", thumbnail="http://repository-butchabay.googlecode.com/svn/branches/eden/skin.cirrus.extended.v2/extras/moviegenres/All%20Movies%20by%20Actor.png"))
    itemlist.append( Item(channel=__channel__, title="Elenco Film [A-Z]", action="categorias", url="http://www.darkstream.tv/", thumbnail="http://repository-butchabay.googlecode.com/svn/branches/eden/skin.cirrus.extended.v2/extras/moviegenres/Movies%20A-Z.png"))
    #itemlist.append( Item(channel=__channel__, title="Cerca...", action="search", thumbnail="http://dc467.4shared.com/img/fEbJqOum/s7/13feaf0c8c0/Search"))

    
    return itemlist


def cat_registi_A(item):
    logger.info("streamondemand.biblioteca cat_registi_A")
    itemlist = []

    # Descarga la pagina
    data = anti_cloudflare( item.url )
    
    # Extrae las entradas (carpetas)
    patron  = '<li><a href="http://altadefinizione.co/regista/a.*?" rel="tag">(.*?)</a></li>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for scrapedtitle in matches:
        titolo = scrapedtitle.replace(" ","+")
        itemlist.append( Item(channel=__channel__, action="do_search", extra=titolo, title= scrapedtitle , folder=True) )

    return itemlist

def cat_registi_B_C_D(item):
    logger.info("streamondemand.biblioteca cat_registi_B_C_D")
    itemlist = []

    # Descarga la pagina
    data = anti_cloudflare( item.url )
    
    # Extrae las entradas (carpetas)
    patron  = '<li><a href="http://altadefinizione.co/regista/[bcd].*?" rel="tag">(.*?)</a></li>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for scrapedtitle in matches:
        titolo = scrapedtitle.replace(" ","+")
        itemlist.append( Item(channel=__channel__, action="do_search", extra=titolo, title= scrapedtitle , folder=True) )

    return itemlist

def cat_registi_E_F(item):
    logger.info("streamondemand.biblioteca cat_registi_E_F")
    itemlist = []

    # Descarga la pagina
    data = anti_cloudflare( item.url )
    
    # Extrae las entradas (carpetas)
    patron  = '<li><a href="http://altadefinizione.co/regista/[ef].*?" rel="tag">(.*?)</a></li>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for scrapedtitle in matches:
        titolo = scrapedtitle.replace(" ","+")
        itemlist.append( Item(channel=__channel__, action="do_search", extra=titolo, title= scrapedtitle , folder=True) )

    return itemlist

def cat_registi_G(item):
    logger.info("streamondemand.biblioteca cat_registi_G")
    itemlist = []

    # Descarga la pagina
    data = anti_cloudflare( item.url )
    
    # Extrae las entradas (carpetas)
    patron  = '<li><a href="http://altadefinizione.co/regista/g.*?" rel="tag">(.*?)</a></li>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for scrapedtitle in matches:
        titolo = scrapedtitle.replace(" ","+")
        itemlist.append( Item(channel=__channel__, action="do_search", extra=titolo, title= scrapedtitle , folder=True) )

    return itemlist

def cat_registi_H_I(item):
    logger.info("streamondemand.biblioteca cat_registi_H_I")
    itemlist = []

    # Descarga la pagina
    data = anti_cloudflare( item.url )
    
    # Extrae las entradas (carpetas)
    patron  = '<li><a href="http://altadefinizione.co/regista/[hi].*?" rel="tag">(.*?)</a></li>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for scrapedtitle in matches:
        titolo = scrapedtitle.replace(" ","+")
        itemlist.append( Item(channel=__channel__, action="do_search", extra=titolo, title= scrapedtitle , folder=True) )

    return itemlist

def cat_registi_J(item):
    logger.info("streamondemand.biblioteca cat_registi_J")
    itemlist = []

    # Descarga la pagina
    data = anti_cloudflare( item.url )
    
    # Extrae las entradas (carpetas)
    patron  = '<li><a href="http://altadefinizione.co/regista/[j].*?" rel="tag">(.*?)</a></li>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for scrapedtitle in matches:
        titolo = scrapedtitle.replace(" ","+")
        itemlist.append( Item(channel=__channel__, action="do_search", extra=titolo, title= scrapedtitle , folder=True) )

    return itemlist

def cat_registi_K_L(item):
    logger.info("streamondemand.biblioteca cat_registi_K_L")
    itemlist = []

    # Descarga la pagina
    data = anti_cloudflare( item.url )
    
    # Extrae las entradas (carpetas)
    patron  = '<li><a href="http://altadefinizione.co/regista/[kl].*?" rel="tag">(.*?)</a></li>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for scrapedtitle in matches:
        titolo = scrapedtitle.replace(" ","+")
        itemlist.append( Item(channel=__channel__, action="do_search", extra=titolo, title= scrapedtitle , folder=True) )

    return itemlist

def cat_registi_M(item):
    logger.info("streamondemand.biblioteca cat_registi_M")
    itemlist = []

    # Descarga la pagina
    data = anti_cloudflare( item.url )
    
    # Extrae las entradas (carpetas)
    patron  = '<li><a href="http://altadefinizione.co/regista/[m].*?" rel="tag">(.*?)</a></li>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for scrapedtitle in matches:
        titolo = scrapedtitle.replace(" ","+")
        itemlist.append( Item(channel=__channel__, action="do_search", extra=titolo, title= scrapedtitle , folder=True) )

    return itemlist

def cat_registi_N_O_P(item):
    logger.info("streamondemand.biblioteca cat_registi_N_O_P")
    itemlist = []

    # Descarga la pagina
    data = anti_cloudflare( item.url )
    
    # Extrae las entradas (carpetas)
    patron  = '<li><a href="http://altadefinizione.co/regista/[nop].*?" rel="tag">(.*?)</a></li>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for scrapedtitle in matches:
        scrapedtitle=scrapertools.decodeHtmlentities(scrapedtitle.replace("N/A",""))
        titolo = scrapedtitle.replace(" ","+")
        itemlist.append( Item(channel=__channel__, action="do_search", extra=titolo, title= scrapedtitle , folder=True) )

    return itemlist

def cat_registi_Q_R(item):
    logger.info("streamondemand.biblioteca cat_registi_Q_R")
    itemlist = []

    # Descarga la pagina
    data = anti_cloudflare( item.url )
    
    # Extrae las entradas (carpetas)
    patron  = '<li><a href="http://altadefinizione.co/regista/[qr].*?" rel="tag">(.*?)</a></li>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for scrapedtitle in matches:
        titolo = scrapedtitle.replace(" ","+")
        itemlist.append( Item(channel=__channel__, action="do_search", extra=titolo, title= scrapedtitle , folder=True) )

    return itemlist

def cat_registi_S(item):
    logger.info("streamondemand.biblioteca cat_registi_S")
    itemlist = []

    # Descarga la pagina
    data = anti_cloudflare( item.url )
    
    # Extrae las entradas (carpetas)
    patron  = '<li><a href="http://altadefinizione.co/regista/[s].*?" rel="tag">(.*?)</a></li>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for scrapedtitle in matches:
        titolo = scrapedtitle.replace(" ","+")
        itemlist.append( Item(channel=__channel__, action="do_search", extra=titolo, title= scrapedtitle , folder=True) )

    return itemlist

def cat_registi_T_U_V(item):
    logger.info("streamondemand.biblioteca cat_registi_T_U_V")
    itemlist = []

    # Descarga la pagina
    data = anti_cloudflare( item.url )
    
    # Extrae las entradas (carpetas)
    patron  = '<li><a href="http://altadefinizione.co/regista/[tuv].*?" rel="tag">(.*?)</a></li>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for scrapedtitle in matches:
        titolo = scrapedtitle.replace(" ","+")
        itemlist.append( Item(channel=__channel__, action="do_search", extra=titolo, title= scrapedtitle , folder=True) )

    return itemlist


def cat_registi_W_X_Y_Z(item):
    logger.info("streamondemand.biblioteca cat_registi_W_X_Y_Z")
    itemlist = []

    # Descarga la pagina
    data = anti_cloudflare( item.url )
    
    # Extrae las entradas (carpetas)
    patron  = '<li><a href="http://altadefinizione.co/regista/[wxyz].*?" rel="tag">(.*?)</a></li>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for scrapedtitle in matches:
        titolo = scrapedtitle.replace(" ","+")
        itemlist.append( Item(channel=__channel__, action="do_search", extra=titolo, title= scrapedtitle , folder=True) )

    return itemlist


def cat_attori(item):
    logger.info("streamondemand.biblioteca cat_attori")
    itemlist = []

    # Descarga la pagina
    data = anti_cloudflare( item.url )
    
    # Extrae las entradas (carpetas)
    patron  = '<li><a href=".*?" rel="tag">(.*?)</a></li>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for scrapedtitle in matches:
        titolo = scrapedtitle.replace(" ","+")
        itemlist.append( Item(channel=__channel__, action="do_search", extra=titolo, title= scrapedtitle , folder=True) )

    return itemlist

def categorias(item):
    logger.info("streamondemand.biblioteca categorias")
    itemlist = []

    # Descarga la pagina
    data = scrapertools.cache_page(item.url)
    
    # Extrae las entradas (carpetas)
    patron  = '<li class="menu-item-3[^>]+><a[^=]+=[^=]+="(.*?)">(.*?)</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for scrapedurl,scrapedtitle in matches:
        scrapedplot = ""
        scrapedthumbnail = ""
        scrapedtitle=scrapertools.decodeHtmlentities(scrapedtitle.replace("Home",""))
        scrapedtitle=scrapertools.decodeHtmlentities(scrapedtitle.replace("http://www.darkstream.tv/",""))
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"]")
        itemlist.append( Item(channel=__channel__, action="cat_elenco", title=scrapedtitle , url=scrapedurl , thumbnail="http://xbmc-repo-ackbarr.googlecode.com/svn/trunk/dev/skin.cirrus%20extended%20v2/extras/moviegenres/All%20Movies%20by%20Genre.png", folder=True) )

    return itemlist

def cat_elenco(item):
    logger.info("streamondemand.biblioteca cat_elenco")
    itemlist = []

    # Descarga la pagina
    data = scrapertools.cache_page(item.url)
    
    # Extrae las entradas (carpetas)
    patron  = '<a href=".*?">(.*?)</a>[^<]+<span style='
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for scrapedtitle in matches:
        scrapedtitle=scrapertools.decodeHtmlentities( scrapedtitle )
        titolo = scrapedtitle.replace(" ","+")
        itemlist.append( Item(channel=__channel__, action="do_search", extra=titolo, title= scrapedtitle , folder=True) )

    return itemlist

def do_search(item):
    logger.info("streamondemand.channels.biblioteca do_search")

    tecleado = item.extra
    mostra = tecleado.replace("+"," ")

    itemlist = []

    import os
    import glob
    import imp

    master_exclude_data_file = os.path.join( config.get_runtime_path() , "resources", "biblioteca.txt")
    logger.info("streamondemand.channels.buscador master_exclude_data_file="+master_exclude_data_file)

    exclude_data_file = os.path.join( config.get_data_path() , "biblioteca.txt")
    logger.info("streamondemand.channels.buscador exclude_data_file="+exclude_data_file)

    channels_path = os.path.join( config.get_runtime_path() , "channels" , '*.py' )
    logger.info("streamondemand.channels.buscador channels_path="+channels_path)

    excluir=""

    if os.path.exists(master_exclude_data_file):
        logger.info("streamondemand.channels.buscador Encontrado fichero exclusiones")

        fileexclude = open(master_exclude_data_file,"r")
        excluir= fileexclude.read()
        fileexclude.close()
    else:
        logger.info("streamondemand.channels.buscador No encontrado fichero exclusiones")
        excluir = "seriesly\nbuscador\ntengourl\n__init__"

    if config.is_xbmc():
        show_dialog = True

    try:
        import xbmcgui
        progreso = xbmcgui.DialogProgressBG()
        progreso.create("Ricerca di "+ mostra.title())
    except:
        show_dialog = False

    channel_files = glob.glob(channels_path)
    number_of_channels = len(channel_files)

    for index, infile in enumerate(channel_files):
        percentage = index*100/number_of_channels

        basename = os.path.basename(infile)
        basename_without_extension = basename[:-3]
        
        if basename_without_extension not in excluir:

            if show_dialog:
                progreso.update(percentage, ' Sto cercando "' + mostra+ '"')

            logger.info("streamondemand.channels.buscador Tentativo di ricerca su " + basename_without_extension + " per "+ mostra)
            try:

                # http://docs.python.org/library/imp.html?highlight=imp#module-imp
                obj = imp.load_source(basename_without_extension, infile)
                logger.info("streamondemand.channels.buscador cargado " + basename_without_extension + " de "+ infile)
                channel_result_itemlist = obj.search( Item() , tecleado)
                for item in channel_result_itemlist:
                    item.title = scrapertools.decodeHtmlentities( item.title )
                    item.title = item.title + "su" + basename_without_extension
                    item.viewmode = "list"

                itemlist.extend( channel_result_itemlist )
            except:
                import traceback
                logger.error( traceback.format_exc() )

        else:
            logger.info("streamondemand.channels.buscador do_search_results, Escluso il server " + basename_without_extension)

    itemlist = sorted(itemlist, key=lambda Item: Item.title) 

    if show_dialog:
        progreso.close()

    return itemlist

def anti_cloudflare(url):
    # global headers

    try:
        resp_headers = scrapertools.get_headers_from_response(url, headers=headers)
        resp_headers = dict(resp_headers)
    except urllib2.HTTPError, e:
        resp_headers = e.headers

    if 'refresh' in resp_headers:
        time.sleep(int(resp_headers['refresh'][:1]))
        
        scrapertools.get_headers_from_response(host + "/" + resp_headers['refresh'][7:], headers=headers)

    return scrapertools.cache_page(url, headers=headers)
