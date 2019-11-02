import argparse
import matplotlib.pyplot as plt
import numpy as np
import random


# Asignamos coordenadas aleatorias.

# for i,v in enumerate(grafo1[0]):
#     posx.append(random.random())
#     posy.append(random.random())
#     print(posx[i], posy[i]) 
    
# # Dibujo puntos:
# plt.scatter(posx, posy)

# # Dibujo aristas:
# for e in grafo1[1]:
#     plt.plot([posx[e[0]], posx[e[1]]], [posy[e[0]], posy[e[1]]])

# Parser

parser = argparse.ArgumentParser()
# Verbosidad
parser.add_argument(
        '-v', '--verbose', 
        action='store_true', 
        help='Muestra mas informacion al correr el programa'
    )
# Cantidad de iteraciones.
parser.add_argument(
        '--iters',
        type=int,
        help='Cantidad de iteraciones a efectuar', 
        default=50
    )
# Temperatura inicial.
parser.add_argument(
        '--temp',
        type=float, 
        help='Temperatura inicial', 
        default=100.0
    )
# Nombre del archivo
parser.add_argument(
        'file_name',
        help='Archivo del cual leer el grafo a dibujar'
    )

args = parser.parse_args()
#-----------------------------------------------------------

# Leemos el archivo de entrada que contiene el grafo.

def read_file(fileName):
    v = []
    e = []
    G = (v, e)
    n = 0 # Nro. de vértices.
    with open(fileName, 'r') as file:
        i = 1 # Linea en la que estamos.
        n = int(file.readline())
        for line in file.readlines():
            if i <= n:
                v.append(line[:len(line)-1:]) 
            else:
                line = line.split()
                e.append((line[0], line[1]))
            i += 1

    return G

# Define las posiciones aleatorias.
# (entender como funciona)

def randomize_positions(nodes):
    posx = []
    posy = []
    for i,v in enumerate(nodes):
        posx.append(random.random())
        posy.append(random.random())    
    return (posx,posy)

# def f_attraction(u, v):

# def f_repultion(u, v):
       

def Fruchterman-Reingold(graph,iterator):
    nodes = graph[0]
    edges = graph[1]
    randomize_positions(nodes)
    acumm = list()
    for i in range(1, iterator+1):
        for i in range(len(accum)):
            acumm[i] = 0
    for e in edges:
        f = f_attraction(e)
        accum[e(0)] += f
        accum[e(1)] -= f
    for n1 in nodes:
        for n2 in nodes:
            if n1 != n2:
                f = f_repultion(n1, n2)
                accum[n1] += f
                accum[n2] -= f
    return accum # no se si va esto jeje
    

# plt.show()
