import math


def cantidad_combinaciones(filas, columnas):
    iteraciones = filas * columnas
    total = 0
    for x in range(iteraciones):
        total += float((math.factorial(iteraciones) // (math.factorial(iteraciones - x) * math.factorial(x))))

    return total


C1 = cantidad_combinaciones(30, 30)

print(f"La cantidad de combinaciones posibles para C1 es {C1} combinaciones")
# 1 Exaflop son 10**18 operaciones
# El Capitan podrá hacer 2 exaflop de operaciones por segundo

EL_CAPITAN_OP_X_SEC = 2 * 10 ** 18
COMBINACIONES = 8.45 * 10 ** 270

segundos = COMBINACIONES / EL_CAPITAN_OP_X_SEC
minutos = segundos / 60
horas = minutos / 60
dias = horas / 24
anos = dias / 365

millones_de_anos = (anos * 10 **-6)
#1 año son 10-6 millones de años

print(f"La cantidad de segundos son {segundos}")
print(f"La cantidad de anos son {anos}")
print(f"La cantidad de millones de años son {millones_de_anos}")


#Edad del universo: 13.770 millones de años
#Si se hubiese puesto la restricción de los subloops, ni El Capitán lo podría resolver en un tiempo razonable.