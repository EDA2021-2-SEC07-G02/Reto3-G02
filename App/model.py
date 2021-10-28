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
             'dateIndex':None}
    catalog['ufos']=lt.newList('ARRAY_LIST')
    catalog['dateIndex']=om.newMap(omaptype='RBT',
                                   comparefunction=compareDates)
    catalog['cityIndex']=om.newMap(omaptype='RBT',
                                   comparefunction=compareDates)
    return catalog


# Funciones para agregar informacion al catalogo

def addUfo(catalog,ufo):
    lt.addLast(catalog['ufos'],ufo)
    posicion=lt.size(catalog['ufos'])
    updateIndexDate(catalog,ufo,posicion)
    updateIndexCity(catalog,ufo,posicion)


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

# Funciones para creacion de datos

# Funciones de consulta

def avistamientosPorCiudad(catalog,ciudad): # Requerimiento Grupal 1: Contar los avistamientos de una ciudad

    ufos=om.get(catalog["cityIndex"],ciudad)["value"]
    listaAvistamiento=lt.newList("ARRAY_LIST")
    for indice in lt.iterator(ufos):
        lt.addLast(listaAvistamiento,lt.getElement(catalog["ufos"],indice))
    listaAvistamiento=selection.sortEdit(listaAvistamiento,compareUFObyDate,3,
                                        ordenarInicio=True,ordenarFinal=True) #Lista editada con selection

    listaCiudades=om.keySet(catalog["cityIndex"])
    listaCiudades=lt.subList(listaCiudades,1,lt.size(listaCiudades))

    listaCiudadesUFO=lt.newList("ARRAY_LIST")

    for num in range(5):
        cont=1
        maxi=0
        nombre_max=""
        indice_borrar=0
        for ciudad in lt.iterator(listaCiudades):
            tam=lt.size(om.get(catalog["cityIndex"],ciudad)["value"])
            if tam>maxi:
                maxi=tam
                nombre_max=ciudad
                indice_borrar=cont
            cont+=1
        if(indice_borrar>0):
            lt.deleteElement(listaCiudades,indice_borrar)
            lt.addLast(listaCiudadesUFO,{"city":nombre_max,"tam":maxi})

    return listaAvistamiento, listaCiudadesUFO


def avistamientoRangoFechas(catalog,fechaInicial,fechaFinal):
    #fechaInicialHora=fechaInicial+" 00:00:00" #se agrega la hora de inicio de día para coincidir con el formato del csv
    #fechaFinalHora=fechaFinal+" 23:59:59"
    #print(fechaFinalHora,fechaInicialHora)
    date1=(datetime.datetime.strptime(fechaInicial, '%Y-%m-%d')).date()
    date2=(datetime.datetime.strptime(fechaFinal, '%Y-%m-%d')).date()

    listaFechasArbol=om.keySet(catalog["dateIndex"])

    #Ultimas fechas
    keysUltimasFechas=lt.subList(listaFechasArbol,1,5)
    respuestaUltimasFechas=lt.newList("ARRAY_LIST")
    for fechaUltima in lt.iterator(keysUltimasFechas):
        infoFecha=om.get(catalog["dateIndex"],fechaUltima)
        fechaStr=fechaUltima.strftime('%Y-%m-%d') #se convierte de datetime a str
        elemento={"date":fechaStr,"count":infoFecha["value"]["size"]}
        lt.addLast(respuestaUltimasFechas,elemento)
    
    #Fechas dentro del rango brindado por el usuario
    listaFechasAvistamientos=lt.newList("ARRAY_LIST")
    listaRespuestaView=lt.newList("ARRAY_LIST")
    n=0
    for fecha in lt.iterator(listaFechasArbol):
        if fecha>date1 and fecha<date2:
            lt.addLast(listaFechasAvistamientos,fecha)
        if n<6: #Número de avistamientos en el view
            pass #implementar despuésssssss

    return respuestaUltimasFechas, listaFechasAvistamientos,listaFechasAvistamientos["size"]

#Funciones de consulta para el lab 8
def infoTreeUFOS(catalog):
    sizeUFOs=lt.size(catalog["ufos"])
    alturaCityIndex=om.height(catalog['cityIndex'])
    nElementosCityIndex= om.size(catalog['cityIndex'])
    return sizeUFOs,alturaCityIndex,nElementosCityIndex

# Funciones utilizadas para comparar elementos dentro de una lista

def compareDates(date1, date2):
    """
    Compara dos fechas
    """
    if (date1 == date2):
        return 0
    elif (date1 > date2):
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


# Funciones de ordenamiento

def sortList(lista,cmpFunction,sortType=3):
    """
    ####### FUNCIÓN MODIFICADA PARA HACER PRUEBAS #####
    Función de ordenamiento que se usará en distintos requerimientos dependiendo
    del ordenamiento deseado
    Parámetros: 
        lista: lista que se ordenara
        cmpFunction: función de comparación
        sortType: tipo de ordenamiento (1)Insertion - (2)Selection - (3)Merge - (4)Quick
    Retorno:
        lista ordenada por insertion
    """
    if sortType == 1:
        sorted_list= selection.sort(lista,cmpFunction) 
    elif sortType == 2:
        sorted_list= sa.sort(lista,cmpFunction)
    elif sortType == 3:
        sorted_list= ms.sort(lista,cmpFunction)
    else:
        sorted_list= ms.sort(lista,cmpFunction)
    return sorted_list
