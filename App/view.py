"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
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
 """

import config as cf
import sys
import controller
from DISClib.ADT import list as lt
assert cf
import time
import prettytable
from prettytable import PrettyTable
from IPython.display import display


ufosfile = 'UFOS//UFOS-utf8-'


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
    print("-"*50)
    print("Bienvenido")
    print("0. Cargar información en el catálogo")
    print("1. Contar avistamientos en una ciudad")
    print("2. Contar los avistamientos por duración ")
    print("3. Contar los avistamientos por Hora/Minutos del día ")
    print("4. Contar los avistamientos en un rango de fechas ")
    print("5. Contar los avistamientos de una zona geográfica ")
    print("6. Visualizar los avistamientos de una zona geográfica")
    print("7. Salir")
    print("-"*50,"\n")

def printInput(requerimiento,tipo):
    if tipo=="Input":
        print("-"*14 + "Requerimiento "+str(requerimiento)+" " + tipo+"s"+"-"*14)
    elif tipo=="Resultado":
        print("\n"+"-"*12 + "Requerimiento "+str(requerimiento)+" " + tipo+"s"+"-"*12)


catalog = None

def printPrettyTable(lista, keys, field_names, max_width, sample=3, ultimas=False):
    artPretty=PrettyTable(hrules=prettytable.ALL)
    artPretty.field_names=field_names
    artPretty._max_width = max_width

    cont=1

    for elemento in lt.iterator(lista):
        valoresFila=[]
        for key in keys:
            valoresFila.append(elemento[key])
        artPretty.add_row(tuple(valoresFila))
        if cont>=sample:
            break
        cont+=1
    
    if ultimas:
        ultimo_index=lt.size(lista) # aRRAY LIST
        cont2=1
        while cont2<=sample:
            indice=ultimo_index-sample+cont2
            if indice>cont and indice>=0 and lt.size(lista)>=indice:
                elemento=lt.getElement(lista,indice)
                valoresFila=[]
                for key in keys:
                    valoresFila.append(elemento[key])
                artPretty.add_row(valoresFila)
            cont2+=1
    
    print(artPretty)

def printCarga(lista,infoArbol=None,requerimiento=0):
    samplePrint=3 #3 para el resto de reqs, 5 para la carga
    if requerimiento==0:
        print("Se han cargado "+ str(infoArbol[0])+" avistamientos de UFOs al catálogo.") #LAB8 los datos característicos (altura y número de elementos)
        # print("Altura Árbol CityIndex",infoArbol[1])
        # print("Hay "+ str(infoArbol[2]) + " ciudades con avistamientos de UFOs\n")
        samplePrint=5

    print("\nA continuación se presentan "+str(samplePrint)+" primeros registros y "+str(samplePrint)+" últimos registros")

    keys=["datetime","city","state","country","shape",
                        "duration (seconds)","comments","longitude","latitude"]
    fieldNames=["Fecha","Ciudad","Estado","País","Forma",
                        "Duración","Comentarios","Longitud","Latitud"]
    maxWidth = {"Fecha":10,"Ciudad":10,"Estado":10,"País":10,"Forma":10,
                        "Duración":10,"Comentarios":30,"Longitud":10,"Latitud":10}

    printPrettyTable(lista,keys,fieldNames,maxWidth,sample=samplePrint,ultimas=True)

def printAvistamientosPorCiudad(respuesta,ciudad): #req1
    listaAvistamientos=respuesta[0]
    cantidadCiudades=respuesta[1]
    print("\nEn total hay",cantidadCiudades,"diferentes ciudades con avistamientos.")
    print("\nEn total hay",lt.size(listaAvistamientos),"avistamientos en",ciudad+","," a continuación se presentan los tres primeros y tres últimos de las lista\n")
    keys=["datetime","city","state","country","shape",
                        "duration (seconds)","comments","longitude","latitude"]
    fieldNames=["Fecha","Ciudad","Estado","País","Forma",
                        "Duración","Comentarios","Longitud","Latitud"]
    maxWidth = {"Fecha":10,"Ciudad":10,"Estado":10,"País":10,"Forma":10,
                        "Duración":10,"Comentarios":30,"Longitud":10,"Latitud":10}

    printPrettyTable(listaAvistamientos,keys,fieldNames,maxWidth,sample=3,ultimas=True)

def printAvistamientosPorDuracion(respuesta): #req 2
    listaAvistamientos=respuesta[0]
    cantidadDuraciones=respuesta[1]
    print("\nEn total hay",cantidadDuraciones,"diferentes duraciones de avistamientos. La duración más alta de un UFO se muestra en la siguiente tabla.")

    dic={"duration":respuesta[2],"count":respuesta[3]}
    dicL=lt.newList("ARRAY_LIST")
    lt.addLast(dicL,dic)
    printPrettyTable(dicL,["duration","count"],["Duración","Conteo"],{"Duración":10,"Conteo":10},sample=1,ultimas=False)




    print("\nEn total hay",lt.size(listaAvistamientos),"UFOS en el rango de duración seleccionado, a continuación se presentan los tres primeros y tres últimos de las lista\n")
    keys=["datetime","city","state","country","shape",
                        "duration (seconds)","comments","longitude","latitude"]
    fieldNames=["Fecha","Ciudad","Estado","País","Forma",
                        "Duración","Comentarios","Longitud","Latitud"]
    maxWidth = {"Fecha":10,"Ciudad":10,"Estado":10,"País":10,"Forma":10,
                        "Duración":10,"Comentarios":30,"Longitud":10,"Latitud":10}
    
    

    printPrettyTable(listaAvistamientos,keys,fieldNames,maxWidth,sample=3,ultimas=True)


def printAvistamientosPorHora(respuesta,hora1,hora2): #req3
    numeroAvistamientos=respuesta[2]
    listaAvistamientos=respuesta[1] #avistamientos orden cronologico
    respuestaUltimaHora=respuesta[3]

    print("\nLa última hora de avistamiento es: ") 
    keys=["hour","count"]
    maxWidth = {"hour":12,"count":10}
    fieldNames=["hour","count"]
    printPrettyTable(respuestaUltimaHora,keys,fieldNames,maxWidth,sample=1)

    print("\nEn total hay "+str(numeroAvistamientos)+" avistamientos de UFOs en el rango de horas: "+hora1+" - "+hora2)
    printCarga(listaAvistamientos,requerimiento=3)

def printAvistamientosFechas(respuesta,fechaInicial,fechaFinal): #req 4
    print("\n\nHay "+str(respuesta[4])+" avistamientos de UFOs registrados en fechas distintas")
    print("\nLas últimas fecha de avistamiento es: ") #print("\nLas últimas 5 fechas son: ")
    keys=["date","count"]
    maxWidth = {"date":12,"count":10}
    fieldNames=["date","count"]
    printPrettyTable(respuesta[0],keys,fieldNames,maxWidth,sample=1)

    print("Existen "+str(respuesta[5])+" avistamientos de UFOs en el rango de fechas: "+fechaInicial+" - "+fechaFinal)
    print("Existen "+str(respuesta[2]) + " días distintos con avistamientos en el rango de fechas: "+ fechaInicial+" - "+fechaFinal)
    print("A continuación se presentan los tres primeros y tres últimos avistamientos en este rango de fechas")
    printCarga(respuesta[3],requerimiento=4)

def printAvistamientosUbicacionGeografica(respuesta):
    listaAvistamientos=respuesta

    print("\nEn total hay",lt.size(listaAvistamientos)," en el rango de coordenadas geográfico seleccionado\n")
    keys=["datetime","city","state","country","shape",
                        "duration (seconds)","comments","longitude","latitude"]
    fieldNames=["Fecha","Ciudad","Estado","País","Forma",
                        "Duración","Comentarios","Longitud","Latitud"]
    maxWidth = {"Fecha":10,"Ciudad":10,"Estado":10,"País":10,"Forma":10,
                        "Duración":10,"Comentarios":30,"Longitud":10,"Latitud":10}

    printPrettyTable(listaAvistamientos,keys,fieldNames,maxWidth,sample=5,ultimas=True)

def visualizarMapa(catalog,longitudMimnima,longitudMaxima,latitudMinima,latitudMaxima,avistamientosCargados=None):
    mapa=controller.grafAvistamientosZonaGeografica(catalog,longitudMimnima,longitudMaxima,
                                                    latitudMinima,latitudMaxima,avistamientosCargados=avistamientosCargados)
    print("Mapa con avistamientos en el rango de longitud:" +longitudMimnima+" - "+longitudMaxima
         + " -- latitud:" + latitudMinima+" - "+latitudMaxima )
    display(mapa)

"""
Menu principal
"""
while True:
    printMenu()
    tiempoInicial=time.process_time()
    inputs = input('Seleccione una opción para continuar\n')
    if inputs!="0" and inputs!="7":
        printInput(inputs,"Input")

    # Requerimiento 0: Carga de datos
    if int(inputs[0]) == 0: #CARGA DE DATOS (Opción 3 según el LAB 8)
        catalog=controller.init()
        print("\nCargando información de los archivos ....\n")
        controller.loadData(catalog,ufosfile)
        infoArbol=controller.infoTreeUFOS(catalog)
        printCarga(catalog["ufos"],infoArbol)

    # Requerimiento 1: Avistamientos por ciudad
    elif int(inputs[0]) == 1:
        ciudad=input("Ingrese el nombre de la ciudad: ")
        respuesta=controller.avistamientosPorCiudad(catalog,ciudad)
        printInput(inputs,"Resultado")
        printAvistamientosPorCiudad(respuesta,ciudad)
        pass

    elif int(inputs[0]) == 2:
        dur_min=input("Ingrese la duración mínima: ")
        dur_max=input("Ingrese la duración máxima: ")
        printInput(inputs,"Resultado")
        respuesta=controller.avistamientosPorDuracion(catalog,dur_min,dur_max)
        printAvistamientosPorDuracion(respuesta)

    elif int(inputs[0]) == 3:
        hora1=input("Ingrese la hora inicial (HH:MM): ")
        hora2=input("Ingrese la hora final (HH:MM): ")
        respuesta=controller.avistamientosHoraMinuto(catalog,hora1,hora2)
        printInput(inputs,"Resultado")
        printAvistamientosPorHora(respuesta,hora1,hora2)
        #print(respuesta)

    elif int(inputs[0]) == 4:
        fechaInicial=input("Ingrese la fecha inicial (AAAA-MM-DD): ")
        fechaFinal=input("Ingrese la fecha final (AAAA-MM-DD): ")
        respuesta=controller.avistamientoRangoFechas(catalog,fechaInicial,fechaFinal)
        printInput(inputs,"Resultado")
        printAvistamientosFechas(respuesta,fechaInicial,fechaFinal)

    elif int(inputs[0]) == 5:
        longitudMimnima=input("Ingrese una longitud mínima: ")
        longitudMaxima=input("Ingrese una longitud máxima: ")
        latitudMinima=input("Ingrese una latitud mínima: ")
        latitudMaxima=input("Ingrese una latitud máxima: ")
        respuesta = controller.avistamientosZonaGeografica(catalog,longitudMimnima,longitudMaxima,latitudMinima,latitudMaxima)
        printAvistamientosUbicacionGeografica(respuesta)
        visualizar=input("Visualizar resultados en folium: \n1 ) para visualizar el mapa. \n2 ) no ver el mapa")
        if visualizar=="1":
            visualizarMapa(catalog,longitudMimnima,longitudMaxima,latitudMinima,latitudMaxima,avistamientosCargados=respuesta)


    elif int(inputs[0]) == 6:
        longitudMimnima=input("Ingrese una longitud mínima: ")
        longitudMaxima=input("Ingrese una longitud máxima: ")
        latitudMinima=input("Ingrese una latitud mínima: ")
        latitudMaxima=input("Ingrese una latitud máxima: ")
        printInput(inputs,"Resultado")
        visualizarMapa(catalog,longitudMimnima,longitudMaxima,latitudMinima,latitudMaxima)

    else:
        sys.exit(0)
    input("\nDuración: "+str((time.process_time()-tiempoInicial)*1000)+"ms\nPresione enter para continuar...")
    print("")
sys.exit(0)
