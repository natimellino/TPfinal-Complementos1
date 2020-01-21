import argparse
import matplotlib.pyplot as plt
import numpy as np
import random
import math

# -------------------------------------------------------------------------------
# Hacer:
# -) ReadMe
# -) Revisar todo por las dudas.
# -) Ver lo de los bordes de la pantalla en update_positions.
# -------------------------------------------------------------------------------

# Obs: las funciones que cambiaron con respecto a la versión anterior son la de
# compute_gravity_forces y update_positions. El resto de las funciones mantienen
# la misma idea que en la versión anterior, sólo que ahora todo fue implementado
# utilizando Clases.

# Leemos el archivo de entrada.


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

# Define las posiciones aleatorias de los vértices.


def randomize_positions(nodes):
    positions = {}
    for v in nodes:
        posx = random.random() * 100
        posy = random.random() * 100
        positions[v] = [posx, posy]
    return positions

# Calcula la distancia entre dos vertices.


def distance(clase, n1, n2):
    pos0 = clase.posiciones[n1]
    pos1 = clase.posiciones[n2]
    return ((pos0[0]-pos1[0])**2+(pos0[1]-pos1[1])**2)**(1/2)

# Fuerza de atracción.


def f_atracction(clase, dist):
    k = clase.c2*math.sqrt((clase.tam*clase.tam)/len(clase.grafo[0]))
    return (dist)**2/k

# Fuerza de repulsión.


def f_repultion(clase, dist):
    k = clase.c1*math.sqrt((clase.tam*clase.tam)/len(clase.grafo[0]))
    return k**2/dist

# Calculamos las fuerzas de atracción de todos los vértices.


def compute_atraction_forces(clase):
    for n1, n2 in clase.grafo[1]:
        d = distance(clase, n1, n2)
        # Evitamos divisiones por cero
        while d < 10**-4:
            f = random.random()
            clase.posiciones[n1][0] += f
            clase.posiciones[n1][1] += f
            clase.posiciones[n2][0] -= f
            clase.posiciones[n2][1] -= f
            d = distance(clase, n1, n2)

        mod_fa = f_atracction(clase, d)
        fx = (mod_fa*(clase.posiciones[n2][0] - clase.posiciones[n1][0]) / d)
        fy = (mod_fa*(clase.posiciones[n2][1] - clase.posiciones[n1][1]) / d)
        clase.accum_x[n1] += fx
        clase.accum_y[n1] += fy
        clase.accum_x[n2] -= fx
        clase.accum_y[n2] -= fy


# Calculamos las fuerzas de repulsión de todos los vértices.

def compute_repultion_forces(clase):
    for n1 in clase.grafo[0]:
        for n2 in clase.grafo[0]:
            if n1 != n2:
                d = distance(clase, n1, n2)

                # Evitamos divisiones por cero
                while d < 10**-4:
                    f = random.random()
                    clase.posiciones[n1][0] += f
                    clase.posiciones[n1][1] += f
                    clase.posiciones[n2][0] -= f
                    clase.posiciones[n2][1] -= f
                    d = distance(clase, n1, n2)

                mod_fa = f_repultion(clase, d)
                fx = (mod_fa*(clase.posiciones[n2]
                              [0] - clase.posiciones[n1][0])) / d
                fy = (mod_fa*(clase.posiciones[n2]
                              [1] - clase.posiciones[n1][1])) / d

                clase.accum_x[n1] -= fx
                clase.accum_y[n1] -= fy
                clase.accum_x[n2] += fx
                clase.accum_y[n2] += fy


# Calculamos las fuerzas de gravedad.

def compute_gravity_forces(clase):
    c = clase.grav
    for n in clase.grafo[0]:
        pos0 = clase.posiciones[n]
        d = math.sqrt((pos0[0] - clase.tam/2)**2 + (pos0[1] - clase.tam/2)**2)

        # Evitamos divisiones por cero:
    while d < 10**-4:
        f = random.random()
        clase.posiciones[n][0] += f
        clase.posiciones[n][1] += f
        d = math.sqrt((pos0[0] - clase.tam/2)**2 + (pos0[1] - clase.tam/2)**2)

    mod_fa = c
    fx = (mod_fa * (clase.posiciones[n][0] - clase.tam/2) / d)
    fy = (mod_fa * (clase.posiciones[n][1] - clase.tam/2) / d)
    clase.accum_x[n] -= fx
    clase.accum_y[n] -= fy

# Actualizamos las posiciones de los vértices.


# que pasa con los bordes de la pantalla?

def update_positions(clase):
    for n in clase.grafo[0]:
        f = [clase.accum_x[n], clase.accum_y[n]]
        mod = math.sqrt(f[0]**2 + f[1]**2)
        if mod > clase.temp:
            f[0] = f[0]/mod*clase.temp
            f[1] = f[1]/mod*clase.temp
            (clase.accum_x[n], clase.accum_y[n]) = f
        clase.posiciones[n][0] = clase.posiciones[n][0] + clase.accum_x[n]
        clase.posiciones[n][1] = clase.posiciones[n][1] + clase.accum_y[n]


# Función que dibuja el grafo.

def draw(clase):
    plt.pause(0.0001)
    plt.clf()
    x = [clase.posiciones[i][0] for i in clase.grafo[0]]
    y = [clase.posiciones[i][1] for i in clase.grafo[0]]
    plt.scatter(x, y)
    for e in clase.grafo[1]:
        i1 = (clase.grafo[0]).index(e[0])
        i2 = (clase.grafo[0]).index(e[1])
        plt.plot((x[i1], x[i2]), (y[i1], y[i2]))


class LayoutGraph:

    # Al inicializar una clase 'LayoutGraph' en el main la inicializamos para
    # almacenar en ella los parámetros que recibe _init_ (ver en el main).
    def __init__(self, grafo, iters, refresh, c1, c2, verbose, tam, grav, temp, accum_x, accum_y):
        '''    
        Parametros de layout:
        iters: cantidad de iteraciones a realizar
        refresh: Numero de iteraciones entre actualizaciones de pantalla. 
        0 -> se grafica solo al final.
        c1: constante usada para calcular la repulsion entre nodos
        c2: constante usada para calcular la atraccion de aristas
        '''

        # Guardo el grafo
        self.grafo = grafo

        # Acá guardamos las posiciones de los vértices.
        self.posiciones = {}

        # Guardo opciones
        self.iters = iters
        # self.verbose = verbose
        self.verbose = verbose  # Cambiar despues!
        self.refresh = refresh
        self.c1 = c1  # Constante de repulsión.
        self.c2 = c2  # Constante de atracción.
        self.grav = grav
        self.temp = temp
        self.accum_x = accum_x
        self.accum_y = accum_y
        self.tam = tam

    # Algoritmo de Fruchtermann-Reingold:

    def layout(self):
        '''
        Aplica el algoritmo de Fruchtermann-Reingold para obtener (y mostrar) 
        un layout        
        '''
        if(self.verbose):
            print("Inicializamos posiciones aleatorias:")
        # Inicializamos posiciones aleatorias.
        self.posiciones = randomize_positions(self.grafo[0])

        if (self.verbose):
            for pos in self.posiciones:
                print(pos, self.posiciones[pos])
            print("Pulse enter para iniciar el graficado.")
            input()

        plt.ion()

        # Bucle principal
        for i in range(self.iters):

            if(self.verbose):
                print("Iteración: ", i)
                print("Inicializando acumuladores en 0.")
            # Inicializo acumuladores
            self.accum_x = {node: 0 for node in self.grafo[0]}
            self.accum_y = {node: 0 for node in self.grafo[0]}

            # Calculamos fuerzas de atracción:
            if(self.verbose):
                print("Calculando fuerzas de atracción.")
            compute_atraction_forces(self)

            # Calculamos fuerzas de repulsión:
            if(self.verbose):
                print("Calculando fuerzas de repulsión.")
            compute_repultion_forces(self)

            if(self.verbose):
                print("Calculando fuerzas de gravedad.")
            # Calculamos fuerzas de gravedad:
            compute_gravity_forces(self)

            # Actualizamos las posiciones:
            if(self.verbose):
                print("Actualizamos las posiciones\n")
            update_positions(self)

            # Actualizamos la temperatura:
            self.temp = 0.95 * self.temp  # 0.95 es nuestra constante para la temp

            # Graficamos:

            # Grafico según el parámetro 'refresh':
            if self.refresh != 0 and i % self.refresh == 0:
                draw(self)

        # Caso especial en el caso que refresh sea 0, dibujamos el grafo al
        # finalizar el bucle, es decir, sólo mostramos el resultado final.

        if self.refresh == 0:
            draw(self)
        print("Fin, ya puede cerrar la ventana de graficado.")
        plt.ioff()
        plt.show()


def main():
    # Definimos los argumentos de linea de comando que aceptamos
    parser = argparse.ArgumentParser()

    # Archivo del cual leer el grafo
    parser.add_argument(
        'file_name',
        help='Archivo del cual leer el grafo a dibujar'
    )
    # Verbosidad, opcional.
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Muestra mas informacion al correr el programa',
    )
    # Cantidad de iteraciones, opcional, 150 por defecto
    parser.add_argument(
        '--iters',
        type=int,
        help='Cantidad de iteraciones a efectuar',
        default=150
    )
    # Cada cuánto dibujamos el grafo.
    parser.add_argument(
        '-r', '--refresh',
        type=int,
        help='Cada cuanto redibujamos el grafo.',
        default=2
    )

    args = parser.parse_args()

    # Constantes:

    tam = 1000 # Define el area del recuadro donde graficaremos, en este caso
               # indica que utilizaremos un recuadro de 1000*1000.
    c1 = 5  # Constante de repulsión
    c2 = 0.1  # Constante de atracción
    grav = 0.05 # Constante para la gravedad
    temp = 200.0  # Temperatura inicial.

    # Leemos el grafo dado por el archivo de entrada.
    grafo = read_file(args.file_name)

    # Inicializamos los acumuladores ahora para pasarlos como parámetro para 
    # inicializar la clase.
    accum_x = {node: 0 for node in grafo[0]}
    accum_y = {node: 0 for node in grafo[0]}

    # Inicializamos la clase con todos los parametros especificados:

    layout_gr = LayoutGraph(grafo, args.iters, args.refresh,
                            c1, c2, args.verbose, tam, grav, temp, accum_x, accum_y)
    # Ejecutamos el algoritmo.

    layout_gr.layout()

    return

if __name__ == '__main__':
    main()
