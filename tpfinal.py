import argparse
import matplotlib.pyplot as plt
import numpy as np
import random
import math

area = 100*100
cr = 0.05
ca = 10
eps = 0.05

# Asignamos coordenadas aleatorias.

# -----------------------------------------------------------

# Leemos el archivo de entrada que contiene el grafo.


def read_file(fileName):
    v = []
    e = []
    G = (v, e)
    n = 0  # Nro. de vértices.
    with open(fileName, 'r') as file:
        i = 1  # Linea en la que estamos.
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
        posx = random.random() * 100
        posy = random.random() * 100
        positions[v] = [posx, posy]
    return positions

# Recibe las coordenadas de los vértices u,v.


def f_attraction(d, nodes):
    # x1 = u[0]
    # y1 = u[1]
    # x2 = v[0]print("modfa: ", mod_fa)
    # y2 = v[1]
    # d = math.sqrt((x1-x2)**2 + (y1-y2)**2def)
    k = ca * math.sqrt(area/len(nodes))
    return (d**2)/k


def f_repultion(d, nodes):
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


def distancia(x1, x2, y1, y2):
    return math.sqrt((x1-x2)**2 + (y1-y2)**2)  # calcula distancia


def compute_atracction_forces(positions, accum_x, accum_y, graph):
    nodes = graph[0]
    edges = graph[1]
    for ni, nj in edges:
        x1 = positions[ni][0]
        y1 = positions[ni][1]
        x2 = positions[nj][0]
        y2 = positions[nj][1]
        dist = distancia(x1, x2, y1, y2)
        # Evitamos divisiones por cero.
        while dist < eps:
            f = random.random()
            positions[ni][0] += f
            positions[ni][1] += f
            positions[nj][0] -= f
            positions[nj][1] -= f

            x1 = positions[ni][0]
            y1 = positions[ni][1]
            x2 = positions[nj][0]
            y2 = positions[nj][1]
            dist = distancia(x1, x2, y1, y2)

        mod_fa = f_attraction(dist, nodes)
        # print("modfa: ", mod_fa)
        fx = ((mod_fa)*(x2-x1))/dist
        fy = ((mod_fa)*(y2-y1))/dist
        accum_x[ni] += fx
        accum_y[ni] += fy
        accum_x[nj] -= fx
        accum_y[nj] -= fy
    return (accum_x, accum_y, positions)


def compute_repultion_forces(nodes, accum_x, accum_y, positions):
    for i in range(0, len(nodes)):
        v1 = nodes[i]
        for j in range(i+1, len(nodes)):
            v2 = nodes[j]

            x1 = positions[v1][0]
            y1 = positions[v1][1]
            x2 = positions[v2][0]
            y2 = positions[v2][1]

            dist = distancia(x1, x2, y1, y2)

            while dist < eps:
                f = random.random()

                positions[v1][0] -= f
                positions[v1][1] -= f
                positions[v2][0] += f
                positions[v2][1] += f

                x1 = positions[v1][0]
                y1 = positions[v1][1]
                x2 = positions[v2][0]
                y2 = positions[v2][1]
                # print(x1,x2,y1,y2)
                dist = distancia(x1, x2, y1, y2)

            mod_fr = f_repultion(dist, nodes)
            # print("modfr: ", mod_fr)
            fx = ((mod_fr)*(x2-x1))/dist
            fy = ((mod_fr)*(y2-y1))/dist

            accum_x[v1] -= fx
            accum_y[v1] -= fy
            accum_x[v2] += fx
            accum_y[v2] += fy

    return (accum_x, accum_y, positions)


def compute_gravity_forces(nodes, accum_x, accum_y, positions):
    posx = 50
    posy = 50
    cg = 0.1
    for i in nodes:
        x1 = positions[i][0]
        y1 = positions[i][1]
        dist = distancia(x1, posx, y1, posy)
        # evitamos divisiones por cero
        fx = (cg*(posx-x1))/dist
        fy = (cg*(posy-y1))/dist
        accum_x[i] -= fx
        accum_y[i] -= fy
    return (accum_x, accum_y, positions)


def update_positions(nodes, positions, accum_x, accum_y):
    for n in nodes:
        positions[n][0] = positions[n][0] + accum_x[n]
        positions[n][1] = positions[n][1] + accum_y[n]
        # Verificamos los bordes de la pantalla para x.
        while positions[n][0] >= 100:
            positions[n][0] = positions[n][0] - random.random()
        while positions[n][0] <= 0:
            positions[n][0] = positions[n][0] + random.random()
        # Verificamos los bordes de la pantalla para y.
        while positions[n][1] >= 100:
            positions[n][1] = positions[n][1] - random.random()
        while positions[n][1] <= 0:
            positions[n][1] = positions[n][1] + random.random()
    return positions


def update_positions2(nodes, positions, accum_x, accum_y, t):
    for n in nodes:
        f = (accum_x[n], accum_y[n])
        norma = math.sqrt((f[0])**2 + (f[1])**2)
        if norma > t:
            f = ((f[0]/norma)*t, (f[1]/norma)*t)
        accum_x[n] = f[0]
        accum_y[n] = f[1]

        positions[n][0] = positions[n][0] + accum_x[n]
        positions[n][1] = positions[n][1] + accum_y[n]
        # Verificamos los bordes de la pantalla para x.
        while positions[n][0] >= 100:
            positions[n][0] = positions[n][0] - random.random()
        while positions[n][0] <= 0:
            positions[n][0] = positions[n][0] + random.random()
        # Verificamos los bordes de la pantalla para y.
        while positions[n][1] >= 100:
            positions[n][1] = positions[n][1] - random.random()
        while positions[n][1] <= 0:
            positions[n][1] = positions[n][1] + random.random()
        return positions

def show_graph(G, positions):

    posx = [positions[i][0] for i in G[0]]
    posy = [positions[i][1] for i in G[0]]
    plt.clf()
    # for i,v in enumerate(G[0]):
    #     posx.append(random.random())
    #     posy.append(random.random())
    #     #print(posx[i], posy[i])

    # Dibujo puntos:
    plt.scatter(posx, posy)

    # Dibujo aristas:
    for e in G[1]:
        i1 = G[0].index(e[0])
        i2 = G[0].index(e[1])
        plt.plot([posx[i1], posx[i2]], [posy[i1], posy[i2]])
    plt.pause(0.001)
    # plt.show()

def FruchtermanReingold(graph, iterator):
    nodes = graph[0]
    positions = randomize_positions(nodes)
    # print(positions)
    accum_x = dict()
    accum_y = dict()
    t = 1
    for i in range(1, iterator+1):
        plt.ion()

        acumm = initialize_accumulators(accum_x, accum_y, graph[0])
        accum_x = acumm[0]
        accum_y = acumm[1]
       #  print("inicia acumuladores: ", accum_x, accum_y)
        acumm = compute_atracction_forces(positions, accum_x, accum_y, graph)
        accum_x = acumm[0]
        accum_y = acumm[1]
        positions = acumm[2]
        # print("luego de f atracction: ", accum_x, accum_y)
        # print("fa: ", accum_x, accum_y)

        acumm = compute_repultion_forces(graph[0], accum_x, accum_y, positions)
        accum_x = acumm[0]
        accum_y = acumm[1]
        positions = acumm[2]
        # print("luego de f repultion: ", accum_x, accum_y)
        # print("fr: ", accum_x, accum_y)
        accum = compute_gravity_forces(graph[0], accum_x, accum_y, positions)
        accum_x = acumm[0]
        accum_y = acumm[1]
        positions = acumm[2]

        positions = update_positions(graph[0], positions, accum_x, accum_y)
        t = 1 * t
        show_graph(graph, positions)
        plt.show
        plt.ioff()

    # print(accum_x, accum_y, positions)
    return positions


def main():

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
    # G = (['a', 'b', 'c', 'd'], [('a', 'b'), ('b', 'c'), ('b', 'd')])
    #positions = randomize_positions(G[0])
    G = read_file(args.file_name)
    positions = FruchtermanReingold(G, 100)
    posx = [positions[i][0] for i in G[0]]
    posy = [positions[i][1] for i in G[0]]

    # for i,v in enumerate(G[0]):
    #     posx.append(random.random())
    #     posy.append(random.random())
    #     #print(posx[i], posy[i])

    # Dibujo puntos:
    plt.scatter(posx, posy)

    # Dibujo aristas:
    for e in G[1]:
        i1 = G[0].index(e[0])
        i2 = G[0].index(e[1])
        plt.plot([posx[i1], posx[i2]], [posy[i1], posy[i2]])
    plt.show()


main()
