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


ufosfile = 'UFOS//UFOS-utf8-small.csv'


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
    print("-"*50)
    print("Bienvenido")
    print("0. Cargar información en el catálogo (Avance Lab8)")
    print("1. Contar avistamientos en una ciudad (Avance Lab8) ")
    print("2. Contar los avistamientos por duración ")
    print("3. Contar los avistamientos por Hora/Minutos del día ")
    print("4. Contar los avistamientos en un rango de fechas ")
    print("5. Contar los avistamientos de una zona geográfica ")
    print("6. Visualizar los avistamientos de una zona geográfica")
    print("7. Salir")
    print("-"*50,"\n")

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

def printCarga(lista,infoArbol):
    print("En total se registraron "+ str(infoArbol[0])+" avistamientos de UFOs.") #LAB8 los datos característicos (altura y número de elementos)
    print("Altura Árbol CityIndex",infoArbol[1])
    print("Hay "+ str(infoArbol[2]) + " ciudades con avistamientos de UFOs\n")
    print("\nA continuación se presentan 3 primeros registros y 3 últimos registros")

    keys=["datetime","city","state","country","shape",
                        "duration (seconds)","comments","longitude","latitude"]
    fieldNames=["Fecha","Ciudad","Estado","País","Forma",
                        "Duración","Comentarios","Longitud","Latitud"]
    maxWidth = {"Fecha":10,"Ciudad":10,"Estado":10,"País":10,"Forma":10,
                        "Duración":10,"Comentarios":30,"Longitud":10,"Latitud":10}

    printPrettyTable(lista,keys,fieldNames,maxWidth,sample=3,ultimas=True)

def printAvistamientosPorCiudad(respuesta,ciudad):
    listaAvistamientos=respuesta[0]
    listaCiudades=respuesta[1]

    print("\nLas cinco ciudades con más avistamientos son:\n")
    keys=["city","tam"]
    fieldNames=["Ciudad","Cantidad"]
    maxWidth = {"Ciudad":10,"Cantidad":10}
    printPrettyTable(listaCiudades,keys,fieldNames,maxWidth,sample=5,ultimas=False)    

    print("\n\nEn total hay",lt.size(listaAvistamientos),"en",ciudad,"a continuación se presentan los tres primeros y tres últimos de las lista\n")
    keys=["datetime","city","state","country","shape",
                        "duration (seconds)","comments","longitude","latitude"]
    fieldNames=["Fecha","Ciudad","Estado","País","Forma",
                        "Duración","Comentarios","Longitud","Latitud"]
    maxWidth = {"Fecha":10,"Ciudad":10,"Estado":10,"País":10,"Forma":10,
                        "Duración":10,"Comentarios":30,"Longitud":10,"Latitud":10}

    printPrettyTable(listaAvistamientos,keys,fieldNames,maxWidth,sample=3,ultimas=True)


"""
Menu principal
"""
while True:
    printMenu()
    tiempoInicial=time.process_time()
    inputs = input('Seleccione una opción para continuar\n')

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
        printAvistamientosPorCiudad(respuesta,ciudad)
        pass

    elif int(inputs[0]) == 2:
        print("Por implementar ....")

    elif int(inputs[0]) == 3:
        print("Por implementar ....")

    elif int(inputs[0]) == 4:
        print("Por implementar ....")

    elif int(inputs[0]) == 5:
        print("Por implementar ....")

    elif int(inputs[0]) == 6:
        print("Por implementar ....")

    else:
        sys.exit(0)
    input("\nDuración: "+str((time.process_time()-tiempoInicial)*1000)+"ms\nPresione enter para continuar...")
    print("")
sys.exit(0)
