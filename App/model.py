"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf # SIEMPRE DEJAR CONFIG DE PRIMERAS
from DISClib.DataStructures.bst import maxKey
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Algorithms.Sorting import mergesort as ms
from DISClib.Algorithms.Sorting import selectionsort as selection
assert cf
import datetime
import time
import folium

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos

def newCatalog():
    catalog={'ufos':None,
             'dateIndex':None,
             "durationIndex":None,
             "cityIndex":None,
             "longitudIndex":None,
             "hourIndex":None}
    catalog['ufos']=lt.newList('ARRAY_LIST')
    catalog['dateIndex']=om.newMap(omaptype='RBT',
                                   comparefunction=compareDatesMap)
    catalog['cityIndex']=om.newMap(omaptype='RBT',
                                   comparefunction=compareCitiesMap)
    catalog['durationIndex']=om.newMap(omaptype='RBT',
                                   comparefunction=compareDurationMap)
    catalog['longitudIndex']=om.newMap(omaptype='RBT',
                                   comparefunction=compareLatLongMap)
    catalog["hourIndex"]=om.newMap(omaptype='RBT',
                                   comparefunction=compareHoursMap)
    return catalog


# Funciones para agregar informacion al catalogo

def addUfo(catalog,ufo):
    lt.addLast(catalog['ufos'],ufo)
    posicion=lt.size(catalog['ufos'])
    updateIndexDate(catalog,ufo,posicion)
    updateIndexCity(catalog,ufo,posicion)
    updateDuration(catalog,ufo,posicion)
    updateLongitud(catalog,ufo,posicion)
    updateIndexHour(catalog,ufo,posicion)


def updateIndexDate(catalog,ufo,posicion):
    ufoDate=datetime.datetime.strptime(ufo["datetime"], '%Y-%m-%d %H:%M:%S')
    if om.contains(catalog['dateIndex'],ufoDate.date()):
        lt.addLast(om.get(catalog['dateIndex'],ufoDate.date())["value"],posicion)
    else:
        lista=lt.newList("ARRAY_LIST")
        lt.addLast(lista,posicion)
        om.put(catalog['dateIndex'],ufoDate.date(),lista)

def updateIndexCity(catalog,ufo,posicion):
    ufoCity=ufo["city"]
    if om.contains(catalog['cityIndex'],ufoCity):
        lt.addLast(om.get(catalog['cityIndex'],ufoCity)["value"],posicion)
    else:
        lista=lt.newList("ARRAY_LIST")
        lt.addLast(lista,posicion)
        om.put(catalog['cityIndex'],ufoCity,lista)

def updateDuration(catalog,ufo,posicion):
    duration=ufo["duration (seconds)"]
    duration=int(float(duration))
    if om.contains(catalog['durationIndex'],duration):
        lt.addLast(om.get(catalog['durationIndex'],duration)["value"],posicion)
    else:
        lista=lt.newList("ARRAY_LIST")
        lt.addLast(lista,posicion)
        om.put(catalog['durationIndex'],duration,lista)           

def updateLongitud(catalog,ufo,posicion):
    longitud=ufo["longitude"]
    latitud=ufo["latitude"]
    longitud=round(float(longitud),2)
    latitud=round(float(latitud),2)
    if(om.contains(catalog["longitudIndex"],longitud)):
        mapLat=om.get(catalog["longitudIndex"],longitud)["value"]
        if (om.contains(mapLat,latitud)):
            lt.addLast(om.get(mapLat,latitud)["value"],posicion)
        else:
            lista=lt.newList("ARRAY_LIST")
            lt.addLast(lista,posicion)
            om.put(mapLat,latitud,lista)
    else:
        mapLat=om.newMap(omaptype='RBT',
                                comparefunction=compareLatLongMap)
        lista=lt.newList("ARRAY_LIST")
        lt.addLast(lista,posicion)
        om.put(mapLat,latitud,lista)
        om.put(catalog["longitudIndex"],longitud,mapLat)


def updateIndexHour(catalog,ufo,posicion):
    ufoDateTime=datetime.datetime.strptime(ufo["datetime"][11:-3],'%H:%M').time() #Key
    #fechaTime=datetime.datetime.strptime(ufo["datetime"][:10], '%Y-%m-%d').date()
    fechaTime=ufo["datetime"]#[:10]
    info={"pos":posicion,"fecha":fechaTime} #elemento de la lista value
    if om.contains(catalog['hourIndex'],ufoDateTime):
        lt.addLast(om.get(catalog['hourIndex'],ufoDateTime)["value"],info) #se agrega la pos
    else:
        lista=lt.newList("ARRAY_LIST")
        lt.addLast(lista,info)
        om.put(catalog['hourIndex'],ufoDateTime,lista)


# Funciones para creacion de datos

# Funciones de consulta

def avistamientosPorCiudad(catalog,ciudad): # Requerimiento Grupal 1: Contar los avistamientos de una ciudad
    numeroCiudades=om.size(catalog["cityIndex"])
    ufos=om.get(catalog["cityIndex"],ciudad)["value"]
    listaAvistamiento=lt.newList("ARRAY_LIST")
    for indice in lt.iterator(ufos):
        lt.addLast(listaAvistamiento,lt.getElement(catalog["ufos"],indice))
    listaAvistamiento=sortList(listaAvistamiento,compareUFObyDate,1)
    return listaAvistamiento, numeroCiudades

def avistamientosPorDuracion(catalog,segundos_min,segundos_max): # Requerimiento Individual 2: Contar avistamientos por duración
    segundos_min=int(float(segundos_min))
    segundos_max=int(float(segundos_max))
    numeroDuraciones=om.size(catalog["durationIndex"])

    mayorDuracion=om.maxKey(catalog["durationIndex"])
    cantidadUfosMayorDuracion=lt.size(mayorDuracion["value"])
    mayorDuracion=mayorDuracion["key"]

    
    keySet=om.keySet(catalog["durationIndex"])
    posicionInicial=om.rank(segundos_min+1)
    keySet=lt.subList(keySet,posicionInicial,om.rank(segundos_max+1)-posicionInicial)
    listaAvistamientos=lt.newList("ARRAY_LIST")
    for dur in lt.iterator(keySet):
        listaIndex=om.get(catalog["durationIndex"],dur)["value"]
        for indice in listaIndex:
           lt.addLast(listaAvistamientos,lt.getElement(catalog["ufos"],indice))

    return listaAvistamientos, numeroDuraciones, mayorDuracion, cantidadUfosMayorDuracion

def avistamientosHoraMinuto(catalog,horaInicial,horaFinal): #req individual 3
    """
    Función principal requerimiento 3
    1. Se obtiene la hora máxima con maxKey.
    2. Se obtienen las horas dentro del rango ingresado por el usuario
    usuario
    Parámetros:
        catalog: catálogo con árboles y lista relacionados a avistamientos de UFOs
        horaInicial: Hora inicial dada por el usuario
        horaFinal: Hora Final dada por el usuario
    Retorno:
        rangoHoras: lista con los ufos que están dentro del rango de esa hora
        listaRespuesta: lista con los 3 primeros y 3 últimos UFOs dentro de ese rango
        contadorAvistamientos: contador de avistamientos ufos dentro del rango de fechas
        UltimaHora: hora máxima de avistamiento de UFOs
    """
    #Hora máxima
    horaMaxima=om.maxKey(catalog["hourIndex"])
    ValueUltimaHora=om.get(catalog["hourIndex"],horaMaxima)

    UltimaHora=lt.newList("ARRAY_LIST")
    lt.addLast(UltimaHora,{"hour":horaMaxima.strftime('%H:%M'),
                            "count":ValueUltimaHora["value"]["size"]})

    #Avistamientos dentro del rango de horas usuario
    horaInicialTime=datetime.datetime.strptime(horaInicial,'%H:%M').time()
    horaFinalTime=datetime.datetime.strptime(horaFinal,'%H:%M').time()
    rangoHoras=om.values(catalog["hourIndex"],horaInicialTime,horaFinalTime)
    listaOrdenadaAvistamientos=ListasRespuesta(catalog, rangoHoras,requerimiento="req3")
    listaRespuesta=listaOrdenadaAvistamientos[0]
    contadorAvistamientos=listaOrdenadaAvistamientos[1]
    return rangoHoras,listaRespuesta,contadorAvistamientos,UltimaHora


def selectionPlace(lst,cmpfunction): #Funcion complementaria req 3
    """
    ***FUNCIÓN EDITADA DE LA DISCLIB (ordenamiento selection)***

    La función recorrerá toda una lista, tomará el máximo o mínimo 
    dependiendo de la funciín de comparación, cuando termine de hacer 
    el recorrido se cambiará de lugar el elemento que se está buscando con
    la última pos. Después de esto se elimina el elemento de la 
    última posición y se retornará este elemento eliminado.
    
    """
    size = lt.size(lst)
    pos1 = 1
    minimum = pos1    # minimun tiene el menor elemento
    pos2 = pos1 + 1
    while (pos2 <= size):
        if (cmpfunction(lt.getElement(lst, pos2),
           (lt.getElement(lst, minimum)))):
            minimum = pos2  # minimum = posición elemento más pequeño
        pos2 += 1
    lt.exchange(lst, size, minimum)  # elemento más pequeño -> elem pos1
    minimo=lt.getElement(lst, size)
    lt.removeLast(lst)
    return minimo


def avistamientoRangoFechas(catalog,fechaInicial,fechaFinal): #req grupal 4
    """
    Función principal requerimiento 4
    Parámetros:
        catalog: catálogo con árboles y lista relacionados a avistamientos de UFOs
        fechaInicial: Fecha inicial dada por el usuario
        fechaFinal: Fecha Final dada por el usuario
    Retorno:
        respuestaUltimasFechas: últimas 5 fechas de avistamientos
        soloRango: fechas de avistamientos dentro del rango de fechas
        diasAvistamientos: días con avistamientos de UFOs dentro del rango de fechas
        listaRespuestaView: lista con los 3 primeros y últimos avistamientos
        sizeArbol=total de fechas de avistamientos de UFOs
    """
    date1=(datetime.datetime.strptime(fechaInicial, '%Y-%m-%d')).date()
    date2=(datetime.datetime.strptime(fechaFinal, '%Y-%m-%d')).date()

    sizeArbol=om.size(catalog["dateIndex"])
    
    #actualización reto 
    minkey=om.minKey(catalog["dateIndex"])
    infoMinKey=om.get(catalog["dateIndex"],minkey)["value"]
    respuestaUltimasFechas=lt.newList("ARRAY_LIST")
    lt.addLast(respuestaUltimasFechas,{"date":minkey.strftime('%Y-%m-%d'),
                                        "count":infoMinKey["size"]})
    #Fechas dentro del rango brindado por el usuario
    avistamientoRango=om.values(catalog["dateIndex"],date1,date2)
    diasAvistamientos=avistamientoRango["size"] #Días distintos con avistamientos
    contadorYLista=ListasRespuesta(catalog,avistamientoRango,"req4")
    listaRespuestaView=contadorYLista[0] #3 primeros y 3 últimos avistamientos
    contadorAvistamientos=contadorYLista[1] #Contador del total de avistamientos en el rango

    return respuestaUltimasFechas, avistamientoRango,diasAvistamientos,listaRespuestaView,sizeArbol,contadorAvistamientos

def ListasRespuesta(catalog,tabla,requerimiento): #req 4 - función complementaria
    """
    ### FUNCIÓN COMPLEMENTARIA REQ4 Y REQ3
    Función usado para obtener los 3 primeros y últimos elementos
    Primero se recorre las posiciones de los keys de una tabla, seguido a esto
    se obtiene su valor correspondiente, el cual será una lista (lista_en_pos).
    Después de esto se recorrerá sobre esta lista (lista_en_pos) y se añadirán elementos*
    a la lista de respuesta. Al tener los 3 primeros elementos se pasará a la última posición
    de la tabla para obtener los 3 últimos.
    La función se detendrá hasta tener 6 elementos en la lista de respuesta.
    
    *los elementos en el caso de ser del requerimiento 4 se tomará el máximo o mínimo
    de la lista dependiendo de la posición
    
    Parámetros
        tabla: lista con keys -> árbol (<key,value>)
    Retorno
        lista_respuesta: lista con los 3 primeros y 3 últimos elementos
    
    """

    size=tabla["size"]
    i=1
    ufosPosCadaElemento=tabla
    numeroAvistamientos=0

    #Se obtiene una array lista con los 3 primeros y 3 últimos, además se cuentan los avistamientos
    if requerimiento=="req3" or requerimiento=="req4":
        ufosPosCadaElemento=lt.newList("ARRAY_LIST")
        for key in lt.iterator(tabla): 
            if i<=3 or i>size-3: #Se sacan las 3 primeras y 3 últimas horas dentro del rango de horas
                lt.addLast(ufosPosCadaElemento,key)
            numeroAvistamientos+=key["size"] #contador de avistamientos
            i+=1
    
    

    recorrer=True
    pos=1
    lista_respuesta=lt.newList("ARRAY_LIST")
    while recorrer and lista_respuesta["size"]<=6:
        key_actual=lt.getElement(ufosPosCadaElemento,pos)
        lista_en_pos=key_actual
        #lista_en_pos=om.get(catalog["dateIndex"],key_actual)["value"] #Se obtiene la lista correspondiente a esa pos
        pos_j=1
        
        condiciones_elementos= True
        while condiciones_elementos and pos_j<=lista_en_pos["size"]: #Se detendrá el recorrido de cada key
            
            pos_UFOlist=lt.getElement(lista_en_pos,pos_j)
            if requerimiento=="req4":
                elemento=lt.getElement(catalog["ufos"],pos_UFOlist) #elemento que se agrega en la lista de respuesta
            elif requerimiento=="req3":
                if pos<=3:
                    cmp=compareDateHourMin
                else:
                    cmp=compareDateHourMax
                elementoPos=selectionPlace(lista_en_pos,cmp)
                #print(f'***********ElementoPos{elementoPos}')
                elemento=lt.getElement(catalog["ufos"],elementoPos["pos"])
            #elemento=lt.getElement(catalog["ufos"],pos_UFOlist) #elemento que se agrega en la lista de respuesta
            lt.addLast(lista_respuesta,elemento)
            pos_j+=1

            if lista_respuesta["size"]>=6 and (pos>(ufosPosCadaElemento["size"]-5)+1) and (ufosPosCadaElemento["size"]>=3+1): #se cumple siempre que la lista sea >3
                condiciones_elementos=False
                
            elif lista_respuesta["size"]>=3 and pos<3+1 and ufosPosCadaElemento["size"]>=3+1: #se cumple siempre que la lista sea>3
                condiciones_elementos=False
            
            elif lista_respuesta["size"]>=6:
                condiciones_elementos=False # se termina el proceso en cualquier otro caso (se evitan errores en caso de que la lista sea de tamaño <6 // se puede usar también un break 

        if lista_respuesta["size"]>=6:
            recorrer=False
        if pos==3+1 or lista_respuesta["size"]==3: #Se pasa a la última posición cuando se han obtenido los 3 primeros elementos 
            pos=ufosPosCadaElemento["size"]
            
        elif lista_respuesta["size"]<=3 and pos<3+1:
            pos+=1
            
        elif lista_respuesta["size"]>3 and pos>(ufosPosCadaElemento["size"]-5+1):
            pos-=1
    
    #SE ORDENAN LOS ÚLTIMOS 3 ELEMENTOS
    sortList(lista_respuesta,compareUFObyDate,sortType=1,
                ordenarInicio=False,ordenarFinal=True)
    return lista_respuesta,numeroAvistamientos

def contarAvistamientosZonaGeografica(catalog,long_min,long_max,lat_min,lat_max): # Requerimiento Grupal 5: 
    """
    Req 5
    """
    long_min=round(float(long_min),2)
    long_max=round(float(long_max),2)
    lat_min=round(float(lat_min),2)
    lat_max=round(float(lat_max),2)

    if(long_max<long_min):
        long_temp=long_min
        long_min=long_max
        long_max=long_temp
    
    if(lat_max<lat_min):
        lat_temp=lat_min
        lat_min=lat_max
        lat_max=lat_temp

    lat_max+=0.01
    long_max+=0.01
    

    avistamientos=lt.newList("ARRAY_LIST")

    for arbolLat in lt.iterator(om.values(catalog["longitudIndex"],long_min,long_max)):
        for lat in lt.iterator(om.values(arbolLat,lat_min,lat_max)):
            for index in lt.iterator(lat):
                elemento=lt.getElement(catalog["ufos"],index)
                lt.addLast(avistamientos,elemento)
        
    return avistamientos

def listaReq6(listaUFOs):
    if listaUFOs["size"]>10:
        lista10Elementos=lt.newList("ARRAY_LIST")
        pos=1
        size=listaUFOs["size"]
        condicion=True
        while condicion:
            elemento=lt.getElement(listaUFOs,pos)
            if pos<=5 or pos>=size-5:
                lt.addLast(lista10Elementos,elemento)
                pos+=1
            if lista10Elementos["size"]==5:
                pos=size-5
            if lista10Elementos["size"]==10:
                condicion=False
    else:
        lista10Elementos=listaUFOs

    return lista10Elementos


def grafAvistamientosZonaGeografica(catalog,long_min,long_max,lat_min,lat_max, avistamientosCargados=None): #listaCoordenadas)
    """
    Función para visualizar los avistamientos de acuerdo a coordenadas.

    """

    if avistamientosCargados==None:
        avistamientosArea=contarAvistamientosZonaGeografica(catalog,long_min,long_max,lat_min,lat_max)
    else:
        avistamientosArea=avistamientosCargados
    
    listaCoordenadas=listaReq6(avistamientosArea)

    media_longitud=(float(long_min)+float(long_max))/2
    media_latitud=(float(lat_min)+float(lat_max))/2
    mapgraf=folium.Map(location=[media_latitud,media_longitud],zoom_start=6) #Se crea el mapa

    #Se crea una tabla de símbolos para coordenadas repetidas
    mapProbing=mp.newMap(numelements=11,maptype="PROBING")

    for avistamientoUFO in lt.iterator(listaCoordenadas):
        latitud=avistamientoUFO["latitude"]
        longitud=avistamientoUFO["longitude"]
        tuplaCoordenada=(latitud,longitud)
        existsCoordenada=mp.contains(mapProbing,tuplaCoordenada)
        if existsCoordenada:
            coordenada=mp.get(mapProbing,tuplaCoordenada)
            coordenadaInMap=me.getValue(coordenada)
        else:
            coordenadaInMap=lt.newList("ARRAY_LIST")
            mp.put(mapProbing,tuplaCoordenada,coordenadaInMap)
        lt.addLast(coordenadaInMap,avistamientoUFO)


    coordenadasAgrupadas=mp.valueSet(mapProbing)

    n=1
        #"datetime","city","state","country","shape","duration (seconds)","duration (hours/min)",
        # "comments","date posted","latitude","longitude"
    for avistamientoTupla in lt.iterator(coordenadasAgrupadas):
        nAvistamiento="Avistamientos:"
        qAvistamientos=0
        avistamientosEnLocacion=""
        for UFO in lt.iterator(avistamientoTupla):
            latitud=UFO["latitude"]
            longitud=UFO["longitude"]
            fecha=UFO["datetime"]
            nAvistamiento+=" #" +str(n)
            duracion=UFO["duration (seconds)"]
            forma= UFO["shape"]
            ciudadPais=UFO["city"] +", " + UFO["country"]

            infoPorAvistamiento=str("<br><b> Avistamiento: #"+str(n)+ "</b>"
                                    +"<br><b>Fecha y hora:  &nbsp </b>"+fecha
                                    +" <br><b>Duración: </b>" +duracion
                                    + "<br></b>"+"<b>Forma: </b>" +forma
                                    + "<br> ")
            
            avistamientosEnLocacion+=infoPorAvistamiento

            n+=1
            qAvistamientos+=1

        
        infoAvistamientoTupla=str("<br><h4> <b>"+nAvistamiento+ "&nbsp"+ "</b></h4>"
                            + "<br><b> Cantidad de avistamientos:"+str(qAvistamientos)+ "&nbsp"+ "</b> "
                            + "<br><b> Ciudad, País: </b>"+ciudadPais
                            + "<br><br><b> Info por cada avistamiento:</b><br>"
                            + avistamientosEnLocacion)

        infoHTML=folium.Html(infoAvistamientoTupla,script=True)
        
        fileImage=cf.data_dir+ "UFOS//ufoSpace.png"
        ufoIcon=folium.features.CustomIcon(fileImage,icon_size=(40,40))
        folium.Marker(location=[latitud, longitud], popup=folium.Popup(infoHTML, parse_html=False),icon=ufoIcon,tooltip=nAvistamiento).add_to(mapgraf)


    return mapgraf#.save("PRUEBA914PM.html")

#Funciones de consulta para el lab 8 - VIEW
def infoTreeUFOS(catalog):
    sizeUFOs=lt.size(catalog["ufos"])
    alturaCityIndex=om.height(catalog['cityIndex'])
    nElementosCityIndex= om.size(catalog['cityIndex'])
    return sizeUFOs,alturaCityIndex,nElementosCityIndex

# Funciones utilizadas para comparar elementos dentro de una lista

def compareDatesMap(date1, date2):
    """
    Compara dos fechas
    """
    if (date1 == date2):
        return 0
    elif (date1 > date2):
        return 1
    else:
        return -1


def compareCitiesMap(city1,city2):
    """
    Compara dos ciudades
    """
    if (city1 == city2):
        return 0
    elif (city1 > city2):
        return 1
    else:
        return -1

def compareDurationMap(dur1,dur2):
    """
    Compara dos duraciones
    """
    if (dur1 == dur2):
        return 0
    elif (dur1 > dur2):
        return 1
    else:
        return -1

def compareLatLongMap(l1,l2):
    """
    Compara dos longitude o latitudes
    """
    if (l1 == l2):
        return 0
    elif (l1 > l2):
        return 1
    else:
        return -1

def compareHoursMap(hour1, hour2): #req 3 map
    """
    Compara dos horas
    """
    if (hour1 == hour2):
        return 0
    elif (hour1 > hour2):
        return 1
    else:
        return -1

def compareUFObyDate(ufo1,ufo2):
    """
    Compara dos fechas
    """
    date1=time.strptime(ufo1["datetime"], '%Y-%m-%d %H:%M:%S')
    date2=time.strptime(ufo2["datetime"], '%Y-%m-%d %H:%M:%S')

    return date1 < date2

def compareUFObyCity(ufo1,ufo2):
    return ufo1["city"] < ufo2["city"]

def compareDuration(dur1,dur2):
    return dur1<dur2

def compareDateHourMin(fecha1,fecha2): #req3 ORDEN DE MENOR A MAYOR
    fecha1dt= datetime.datetime.strptime(fecha1["fecha"][:10], '%Y-%m-%d').date()
    fecha2dt= datetime.datetime.strptime(fecha2["fecha"][:10], '%Y-%m-%d').date()
    return fecha1dt<fecha2dt

def compareDateHourMax(fecha1,fecha2): #req3 ORDEN DE MAYOR A MENOR
    fecha1dt= datetime.datetime.strptime(fecha1["fecha"][:10], '%Y-%m-%d').date()
    fecha2dt= datetime.datetime.strptime(fecha2["fecha"][:10], '%Y-%m-%d').date()
    return fecha1dt>fecha2dt

# Funciones de ordenamiento

def sortList(lista,cmpFunction,sortType=1,ordenarInicio=True,
            ordenarFinal=True,posAOrdenar=3):
    """
    Función de ordenamiento que se usará en distintos requerimientos dependiendo
    del ordenamiento deseado
    Parámetros: 
        lista: lista que se ordenara
        cmpFunction: función de comparación
        sortType: tipo de ordenamiento (1)Selection Edit - (2)Merge
    Retorno:
        lista ordenada por insertion
    """
    if sortType == 1: #Selection Sort Edit
        sorted_list= selection.sortEdit(lista,cmpFunction,
                                        posAOrdenar,
                                        ordenarInicio=ordenarInicio,
                                        ordenarFinal=ordenarFinal)
    elif sortType == 2:
        sorted_list= ms.sort(lista,cmpFunction)
    else:
        sorted_list=sa.sort(lista,cmpFunction)
    return sorted_list
