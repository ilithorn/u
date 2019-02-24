#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 22 09:56:56 2019

@author: Agustin Goy
"""

from random import random
import matplotlib.pyplot as plt

FERTILIDAD  = 0.80    #Cuantos arboles nacen
VOLATILIDAD = 0.02    #Que tan probable es que se quemen

def generarProbs(tam, fertilidades):
    for i in range(tam):
        fertilidades.append(0.5)

def pasaProbabilidad(p):
    num = random()
    if num <= p: 
        return True
    else: 
        return False 

def generarBosque(tam):
    bosque = []
    for i in range(tam):
        bosque.append(0)

    return bosque

def primavera(bosque, dinamica):
    for i in range(len(bosque)):
        if not dinamica and pasaProbabilidad(FERTILIDAD): 
            bosque[i] = 1
        if dinamica and pasaProbabilidad(fertilidades[i]):
            bosque[i] = 1
            fertilidades[i] += 0.05

def verano(bosque):
    #Calculamos donde caen los rayos
    for i in range(len(bosque)):
        if bosque[i] == 1 and pasaProbabilidad(VOLATILIDAD):
            bosque[i] = -1

    #Propagamos el fuego
    for i in range(1, len(bosque)):
        if (bosque[i] == 1) and (bosque[i-1] == -1): #Mira si el de la izquierda esta prendido
            bosque[i] = -1
        elif bosque[i] == -1: #Si llega a un fuego, este se propaga hacia atras
            j = i - 1
            while j >= 0 and bosque[j] == 1: #Si encuentra un claro u otro fuego, para
                bosque[j] = -1
                j -= 1


def invierno(bosque, dinamica=False):
    for i in range(len(bosque)):
        if bosque[i] == -1: 
            if dinamica:
                fertilidades[i] -= 0.10 #Ya le habiamos sumado 0.05 (linea 34), asi que el efecto total es de restar 0.05
            bosque[i] = 0
        if fertilidades[i] >= 1:
            fertilidades[i] = 0.99
        if fertilidades[i] <= 0:
            fertilidades[i] = 0.01

def estacion(bosque, dinamica=False):
    primavera(bosque, dinamica)
    verano(bosque)
    invierno(bosque, dinamica)
    return sum(bosque) #Cada arbol es un 1, la suma de la lista da el total

def estaciones(bosque, tiempo):
    suma = 0.0
    for i in range(tiempo):
        vivos = estacion(bosque)
        suma += sum(bosque) 

    promedio = suma/tiempo
    return promedio


iteraciones = 1000
tam = 100

fertilidades = []
generarProbs(tam, fertilidades)

promedios = []
probs = [0.01 * n for n in range(1, 101)]

for i in probs:
    FERTILIDAD = i
    bosque = generarBosque(tam)
    promedio = estaciones(bosque, iteraciones)
    promedios.append(promedio)

#Utilizando dinamica
VOLATILIDAD = 0.1

vivos  = []
bosque = generarBosque(tam)
for i in range(1, 101):
    vivos.append(estacion(bosque, dinamica=True))

#Graficos
plt.figure(num='Bosque estático')
plt.plot(probs, promedios)
plt.xlabel('Fertilidad')
plt.ylabel('Promedio de sobrevivientes')

plt.figure(num='Bosque dinámico')
plt.plot(range(1, 101), vivos)
plt.xlabel('Tiempo')
plt.ylabel('Arboles vivos')

plt.show()
