import argparse
import matplotlib.pyplot as plt

# Guardamos el parser
parser = argparse.ArgumentParser()

# Agregamos los parámetros:

# Agregamos un parámetro obligatorio y posicional (nos referimos a él por la
# posición)

parser.add_argument(
    "file_name", help="El nombre del archivo desde donde leemos el grafo")

# Agregamos un parámetro opcional:

parser.add_argument("--verbosity", help="Incrementa el nivel de verbosidad de la ejecución", action="store_true")

parser.add_argument("-v", help="Incrementa el nivel de verbosidad de la ejecución", action="store_true")


args = parser.parse_args()
if args.verbosity:
    print("La verbosidad está activada.")
if args.v:
    print("La verbosidad está activada.")
    
def leer_grafo_archivo(nombre):
    vertices = []
    aristas = []
    grafo = (vertices,aristas)
    cantVertices = 0
    with open(nombre,'r') as archivo:
        nroLinea = 1
        cantVertices = int(archivo.readline())
        for line in archivo.readlines():
            if nroLinea <= cantVertices:
                vertices.append(line[:len(line)-1:])
            else:
                line = line.split()
                aristas.append((line[0], line[1]))
            nroLinea += 1
    return grafo
    
def main():
    file = args.file_name
    print(leer_grafo_archivo(file))

main() 
    
