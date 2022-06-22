from funciones_auxiliares.grilla import lectura_matriz, creacion_grilla
import random

random.seed(777)

dimension = 50            #Tamaño grilla

M = 21                    # Número materiales
I = dimension             # Número filas de la grilla
J = dimension             # Número columnas de la grilla
K = 4                     # Conjunto de los edificios
T = 15                    # Número de tipo de material

#########################
## P A R A M E T R O S ##
#########################

creacion_grilla(dimension)

matriz = lectura_matriz("archivos excel/matriz_opti.xlsx")
matriz_2 = lectura_matriz("archivos excel/contaminacion.xlsx")

c = 11              # Cantidad minima de area por habitante
C = dict()          # Contaminacion por kilo del material "m", utilizar como llave una tupla del indice m
N = dict()          # Validez de nodo para construcción. Parámetro P_ij
G = dict()          # Costo por kilo del material "m"
H = dict()          # Cantidad de pisos del edificio "k"
A_MAX = 400         # Area basal maxima
A_MIN = 100         # Area basal minima
P = 2*(10**5)       # Presupuesto
D = 500             # Cantidad de personas que deben ubicar
B = dict()          # Cantidad minima a utilizar del material del tipo "t" por piso de la edificacion "k"
BM = 1000000000**9  # BIG "M"
s = 13              #Variable de holgura de la restriccion 1

#Programa que instancia el parametro C   
for fila in range(1, len(matriz_2) + 1):
    C[(fila)] = matriz_2[fila - 1][1]

#Programa que instancia el parametro N  
for fila in range(1, len(matriz) + 1):
    for columna in range(1, len(matriz[0]) + 1):
        N[(fila, columna)] = matriz[fila - 1][columna - 1]

#Programa que instancia el parametro G
for fila in range(1, len(matriz_2) + 1):
    G[(fila)] = matriz_2[fila - 1][2]

#Programa que instancia el parametro H
for k in range(1, K + 1):
    H[(k)] = random.randint(5,15)

#Programa que instancia el parametro B
for t in range(1, T + 1):
    for k in range(1, K + 1):
        B[(t, k)] = random.randint(5*10**3, 5*10**4)


print("El archivo datos.py fue ejecutado")