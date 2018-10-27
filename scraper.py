# -*- coding: utf-8 -*-
"""
Created on Thu Oct 25 23:26:42 2018

@author: clara
"""


import requests
from bs4 import BeautifulSoup
from time import sleep
import csv

#Creamos el fichero vacio
f = open('dataset.csv', 'w')
writer = csv.writer(f)
writer.writerow(('id', 'type', 'name', 'yearpublished', 'minplayers', 'maxplayers', 'playingtime',
                 'minplaytime', 'maxplaytime', 'minage', 'users_rated', 'average_rating',
                 'bayes_average_rating', 'total_owners', 'total_traders', 'total_wanters',
                 'total_wishers', 'total_comments', 'total_weights', 'average_weight'))
#url para la consulta a la API en base al id que nos trae la info del juego
base = 'http://www.boardgamegeek.com/xmlapi2/thing?id={}&stats=1'
gamelink= list()
npage = 1
times= 0

#Seleccionamos el valor de cada variable
def get_val(tag, term):
    try:
        val = tag.find(term)['value'].encode('ascii', 'ignore')
    except:
        val = 'NaN'
    return val

#Nos traemos solo los pimeros 200 registros para esta practica
while times < 1:
    times= times + 1
    #Definimos la url para obtener los ids de los primeros juegos en el ranking de boardgameweek
    r = requests.get("https://boardgamegeek.com/browse/boardgame/page/%i?sort=rank&sortdir=asc" % (npage,))
    soup = BeautifulSoup(r.text, "html.parser")    
    table = soup.find_all("tr", attrs={"id": "row_"})  # Obtenmos la lista de todos los tags de la lista de juegos de la url
    
    # Obtenemos la información de cada url de los juegos con un bucle for
    for idx, row in enumerate(table):
        links = row.find_all("a")
        if "name" in links[0].attrs.keys():
            del links[0]
        gamelink.append(links[1])  # Obtenemos la url relativa de cada juego para obtener solo el id despues
    for i in range(0, len(gamelink)):   
        #Buscamos la informacion de cada juego en base al identificador obtenido anteriormente recorriendo la lista de ids
        url = base.format(gamelink[i]["href"].split("/")[2])
        req = requests.get(url)
        soup = BeautifulSoup(req.content, 'xml')
        items = soup.find_all('item')
        for item in items:
            gid = item['id']
            gtype = item['type']
            gname = get_val(item, 'name')   
            gyear = get_val(item, 'yearpublished')
            gmin = get_val(item, 'minplayers')
            gmax = get_val(item, 'maxplayers')
            gplay = get_val(item, 'playingtime')
            gminplay = get_val(item, 'minplaytime')
            gmaxplay = get_val(item, 'maxplaytime')
            gminage = get_val(item, 'minage')
            usersrated = get_val(item.statistics.ratings, 'usersrated')
            avg = get_val(item.statistics.ratings, 'average')
            bayesavg = get_val(item.statistics.ratings, 'bayesaverage')
            owners = get_val(item.statistics.ratings, 'owned')
            traders = get_val(item.statistics.ratings, 'trading')
            wanters = get_val(item.statistics.ratings, 'wanting')
            wishers = get_val(item.statistics.ratings, 'wishing')
            numcomments = get_val(item.statistics.ratings, 'numcomments')
            numweights = get_val(item.statistics.ratings, 'numweights')
            avgweight = get_val(item.statistics.ratings, 'averageweight')
            # escribimos en el csv la informacion
            writer.writerow((gid, gtype, gname, gyear, gmin, gmax, gplay, gminplay, gmaxplay, gminage,
                         usersrated, avg, bayesavg, owners, traders, wanters, wishers, numcomments,
                         numweights, avgweight))
        #En la web de boardgamegeek se pide que las consultas estén espaciadas en al menos 1 segundo
        sleep(2)
f.close()