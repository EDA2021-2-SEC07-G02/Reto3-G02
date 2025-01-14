﻿"""
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
 """

import config as cf
import model
import csv


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros

def init():
    """
    Llama la funcion de inicializacion  del modelo.
    """
    # catalog es utilizado para interactuar con el modelo
    catalog = model.newCatalog()
    return catalog


# Funciones para la carga de datos

def loadData(catalog, ufosfile):
    """
    Carga los datos de los archivos CSV en el modelo
    """
    muestra="small" #input("Pruebas- muestra: ")
    #print("Catálogo con muestra: "+muestra)
    fileInput = cf.data_dir + ufosfile + muestra + ".csv"
    input_file = csv.DictReader(open(fileInput, encoding="utf-8"),
                                delimiter=",")
    for ufo in input_file:
        model.addUfo(catalog, ufo)
    return catalog

# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo
def infoTreeUFOS(catalog):
    return model.infoTreeUFOS(catalog)

def avistamientoRangoFechas(catalog,fechaInicial,fechaFinal):
    return model.avistamientoRangoFechas(catalog,fechaInicial,fechaFinal)

def avistamientosPorCiudad(catalog, ciudad):
    return model.avistamientosPorCiudad(catalog,ciudad)

def avistamientosPorDuracion(catalog, dur_min, dur_max):
    return model.avistamientosPorDuracion(catalog,dur_min,dur_max)

def avistamientosHoraMinuto(catalog,horaInicial,horaFinal):
    return model.avistamientosHoraMinuto(catalog,horaInicial,horaFinal)

def avistamientosZonaGeografica(catalog,long_min,long_max,lat_min,lat_max):
    return model.contarAvistamientosZonaGeografica(catalog,long_min,long_max,lat_min,lat_max)

def grafAvistamientosZonaGeografica(catalog,long_min,long_max,lat_min,lat_max,avistamientosCargados):
    return model.grafAvistamientosZonaGeografica(catalog,long_min,long_max,lat_min,lat_max,avistamientosCargados=avistamientosCargados)

