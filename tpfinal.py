import argparse
import matplotlib.pyplot as plt
import numpy as np
import random
import math

area = 100*100
cr = 5
ca = 5


# Asignamos coordenadas aleatorias.

    

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
    positions = {}
    for v in nodes:
        posx = random.random()
        posy = random.random()
        positions[v] = (posx, posy)   
    return positions

# Recibe las coordenadas de los vértices u,v.

def f_attraction(d):
    # x1 = u[0]
    # y1 = u[1]
    # x2 = v[0]
    # y2 = v[1]
    # d = math.sqrt((x1-x2)**2 + (y1-y2)**2)
    k = ca * math.sqrt(area/len(nodes))
    return (d**2)/k

def f_repultion(d):
    # x1 = u[0]
    # y1 = u[1]
    # x2 = v[0]
    # y2 = v[1]
    # d = math.sqrt((x1-x2)**2 + (y1-y2)**2)
    k = cr * math.sqrt(area/len(nodes))
    return (k**2)/d

def initialize_accumulators(acum_x, acum_y, nodes):
    for n in nodes:
        acum_x[n] = 0
        acum_y[n] = 0
    return (acum_x, acum_y)

def compute_atracction_forces(positions, accum_x, accum_y, edges):
    for ni,nj in edges:
        x1 = positions[ni][0]
        y1 = positions[ni][1]
        x2 = positions[nj][0]
        y2 = positions[nj][1]
        dist  = math.sqrt((x1-x2)**2 + (y1-y2)**2)
        mod_fa = f_attraction(dist)        
        fx = ((mod_fa)*(x2-x1))/dist
        fy = ((mod_fa)*(y2-y1))/dist
        accum_x[ni] += fx
        accum_y[ni] += fy
        accum_x[nj] -= fx
        accum_y[nj] -= fy
    return (accum_x, accum_y)


def FruchtermanReingold(graph,iterator):
    nodes = graph[0]
    edges = graph[1]
    positions = randomize_positions(nodes)
    accum = dict()

    for i in range(1, iterator+1):
        for i in range(len(accum)):
            accum[i] = 0

    for e in edges:
        v = positions[e[0]]
        u = positions[e[1]]
        f = f_attraction(nodes, u, v)
        accum[e(0)] += f
        accum[e(1)] -= f

    for n1 in nodes:
        for n2 in nodes:
            if n1 != n2:
                f = f_repultion(nodes, n1, n2)
                accum[n1] += f
                accum[n2] -= f
    for i in s
    


def main():
    G = (['a', 'b', 'c', 'd'], [('a', 'b'), ('b', 'c'), ('b', 'd')])
    #positions = randomize_positions(G[0])

    posx = []
    posy = []

    for i,v in enumerate(G[0]):
        posx.append(random.random())
        posy.append(random.random())
        #print(posx[i], posy[i]) 

    # Dibujo puntos:
    plt.scatter(posx, posy)

    #Dibujo aristas:
    for e in G[1]:
        i1 = G[0].index(e[0])
        i2 = G[0].index(e[1])
        plt.plot([posx[i1], posx[i2]], [posy[i1], posy[i2]])
    plt.show()

main()