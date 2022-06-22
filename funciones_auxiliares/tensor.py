import datos as p

I_ = range(0,4)
J_ = range(0,3)
K_ = range(0,3)


lista_X = []



def fila_de_ceros(tamaño):
    l = []
    for i in range(0, tamaño):
        l.append(0)

    return l

def matriz(filas, columnas):
    m = []
    for a in range(filas):
        m.append(fila_de_ceros(columnas))

    return m


def tensor(profundidad, filas, columnas):
    t = []
    for a in range(profundidad):
        t.append(matriz(filas, columnas))

    return t


t = tensor(2, 3, 4)
