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


from DISClib.DataStructures.bst import maxKey
import config as cf
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
    print(ValueUltimaHora)

    UltimaHora=lt.newList("ARRAY_LIST")
    lt.addLast(UltimaHora,{"hour":horaMaxima.strftime('%H:%M'),
                            "count":ValueUltimaHora["value"]["size"]})

    #Avistamientos dentro del rango de horas usuario
    horaInicialTime=datetime.datetime.strptime(horaInicial,'%H:%M').time()
    horaFinalTime=datetime.datetime.strptime(horaFinal,'%H:%M').time()
    rangoHoras=om.values(catalog["hourIndex"],horaInicialTime,horaFinalTime)
    listaOrdenadaAvistamientos=listaRespuestaHoras(catalog, rangoHoras)
    listaRespuesta=listaOrdenadaAvistamientos[0]
    contadorAvistamientos=listaOrdenadaAvistamientos[1]
    return rangoHoras,listaRespuesta,contadorAvistamientos,UltimaHora

def listaRespuestaHoras(catalog, listaRangoHoras): #función complementaria req3
    """
    Función complementaria requerimiento 3

    Se recorre la lista de rango de horas para contar el número de
    avistamientos, al mismo tiempo, se agregan las 3 primeras y 3 
    últimas horas a una nueva lista (lista6Horas). Seguido a esto,
    se obtienen los UFOs en orden crónologico, para esto se hace
    un ordenamiento en la primera y última hora cuando tienen +3 
    fechas, para otros casos [....]

    """
    size=listaRangoHoras["size"]
    pos=1
    lista6Horas=lt.newList("ARRAY_LIST")
    contadorAvistamientos=0
    for hora in lt.iterator(listaRangoHoras):
        if pos<3 or pos>=size-3: #Se sacan las 3 primeras y 3 últimas horas dentro del rango de horas
            lt.addLast(lista6Horas,hora)
        contadorAvistamientos+=hora["size"]
        pos+=1
    
    i=1
    listaRespuesta=lt.newList("ARRAY_LIST")
    recorrer=True
    while recorrer and i<=lista6Horas["size"]:
        elementoLista=lt.getElement(lista6Horas,i)
        if (i==1 and listaRespuesta["size"]<3 and elementoLista["size"]>=3):
            cont=0 #elementos agregados
            pos=1 #pos
            sortList(elementoLista,compareDateHour,sortType=1,ordenarInicio=True,ordenarFinal=False)
            while cont<=3:
                elementoOrdenado=lt.getElement(elementoLista,pos)
                ufo=lt.getElement(catalog['ufos'],elementoOrdenado["pos"])
                lt.addLast(listaRespuesta,ufo)
                cont+=1
                pos+=1
        elif (i==6 and listaRespuesta["size"]>=3) and elementoLista["size"]>=3:
            cont=1 #elementos agregados
            pos=elementoLista["size"] #POS
            sortList(elementoLista,compareDateHour,sortType=1,ordenarInicio=False,ordenarFinal=True)
            while cont<=3:
                elementoOrdenado=lt.getElement(elementoLista,pos)
                ufo=lt.getElement(catalog['ufos'],elementoOrdenado["pos"])
                lt.addLast(listaRespuesta,ufo)
                pos-=1
                cont+=1
        i+=1
    # print("**************************************************")
    # print(lista6Horas,contadorAvistamientos)
    # print("**************************************************")
    # print("*********UFOSSSS*****************************************")
    # print(listaRespuesta)
    # print("**************************************************")
    return listaRespuesta, contadorAvistamientos


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
    Función usado para obtener los 3 primeros y últimos elementos
    Primero se recorre las posiciones de los keys de una tabla, seguido a esto
    se obtiene su valor correspondiente, el cual será una lista (lista_en_pos).
    Después de esto se recorrerá sobre esta lista (lista_en_pos) y se añadirán elementos
    a la lista de respuesta. Al tener los 3 primeros elementos se pasará a la última posición
    de la tabla para obtener los 3 últimos.
    La función se detendrá hasta tener 6 elementos en la lista de respuesta.
    
    Parámetros
        tabla: lista con keys -> árbol (<key,value>)
    Retorno
        lista_respuesta: lista con los 3 primeros y 3 últimos elementos
    
    """
    keys=tabla
    numeroAvistamientos=0
    if requerimiento=="req4": #se convierte de single linked a array
        keys=lt.newList("ARRAY_LIST")
        for key in lt.iterator(tabla): 
            lt.addLast(keys,key)
            numeroAvistamientos+=key["size"] #contador de avistamientos

    recorrer=True
    pos=1
    lista_respuesta=lt.newList("ARRAY_LIST")
    while recorrer and lista_respuesta["size"]<=6:
        key_actual=lt.getElement(keys,pos)
        lista_en_pos=key_actual
        #lista_en_pos=om.get(catalog["dateIndex"],key_actual)["value"] #Se obtiene la lista correspondiente a esa pos
        pos_j=1
        
        condiciones_elementos= True
        while condiciones_elementos and pos_j<=lista_en_pos["size"]: #Se detendrá el recorrido de cada key
            
            pos_UFOlist=lt.getElement(lista_en_pos,pos_j)
            elemento=lt.getElement(catalog["ufos"],pos_UFOlist) #elemento que se agrega en la lista de respuesta
            lt.addLast(lista_respuesta,elemento)
            pos_j+=1

            if lista_respuesta["size"]>=6 and (pos>(keys["size"]-5)+1) and (keys["size"]>=3+1): #se cumple siempre que la lista sea >3
                condiciones_elementos=False
                
            elif lista_respuesta["size"]>=3 and pos<3+1 and keys["size"]>=3+1: #se cumple siempre que la lista sea>3
                condiciones_elementos=False
            
            elif lista_respuesta["size"]>=6:
                condiciones_elementos=False # se termina el proceso en cualquier otro caso (se evitan errores en caso de que la lista sea de tamaño <6 // se puede usar también un break 

        if lista_respuesta["size"]>=6:
            recorrer=False
        if pos==3+1 or lista_respuesta["size"]==3: #Se pasa a la última posición cuando se han obtenido los 3 primeros elementos 
            pos=keys["size"]
            
        elif lista_respuesta["size"]<=3 and pos<3+1:
            pos+=1
            
        elif lista_respuesta["size"]>3 and pos>(keys["size"]-5+1):
            pos-=1
    
    if requerimiento=="req4": #se ordenan los últimos 3 UFOS por fecha
        sortList(lista_respuesta,compareUFObyDate,sortType=1,
                ordenarInicio=False,ordenarFinal=True)
    return lista_respuesta,numeroAvistamientos

def contarAvistamientosZonaGeografica(catalog,long_min,long_max,lat_min,lat_max):
    
    pass

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

def compareDateHour(fecha1,fecha2): #req3
    fecha1dt= datetime.datetime.strptime(fecha1["fecha"][:10], '%Y-%m-%d').date()
    fecha2dt= datetime.datetime.strptime(fecha2["fecha"][:10], '%Y-%m-%d').date()
    return fecha1dt<fecha2dt


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
                                        ordenarInicio,
                                        ordenarFinal)
    elif sortType == 2:
        sorted_list= sa.sort(lista,cmpFunction)
    else:
        sorted_list=sa.sort(lista,cmpFunction)
    return sorted_list
