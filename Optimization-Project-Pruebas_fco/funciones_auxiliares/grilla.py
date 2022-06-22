import numpy as np
import pandas as pd
import random

np.random.seed(1)


def creacion_grilla(dimension: int):
    """
    Lo que hace esta función es crear una matriz de n x n, la cual se utilizará como mapa y cuyos valores [i,j], se le asignarán a la variable
    binaria P[i,j], es decir que si [i,j] = 1, entonces P[i,j] = 1. Además, es capaz de crear ciertas discontinu    y estrellas, además de ser capaz de combinar ambas formas. Luego, esta matriz se pasa a un archivo excel para ser leído.
    """
    
    n = dimension
    array = np.ones(shape=(n,n))
    cant_ceros = (n)*0.5
    
    for i in range(int(cant_ceros)):
        fila = random.randint(0, n-1)
        columna = random.randint(0, n-1)
        
        decision = random.randint(0, 1)
        
        
        #Con esto el código es capaz de crear cuadrados
        if decision == 2:
            if array[fila][columna] == 1:

                try:
                    i = random.randint(3, 5)
                    for k in range(0, i):
                        for j in range(k+1):
                            array[fila - k][columna - j] = 0
                            array[fila + k][columna + j] = 0
                            array[fila + j][columna + k] = 0
                            array[fila - j][columna - k] = 0

                            array[fila - k][columna + j] = 0
                            array[fila + k][columna - j] = 0
                            array[fila - j][columna + k] = 0
                            array[fila + j][columna - k] = 0
                except:
                    print("Hubo una celda que no se pudo cambiar")

        #Con esto el código es capaz de crear estrellas        
        elif decision == 2:
            if array[fila][columna] == 1:

                try:
                    i = random.randint(3, 5)

                    for j in range(i):
                        for k in range(i-j):
                            array[fila-j][columna-k] = 0
                            array[fila+j][columna+k] = 0

                            array[fila-j][columna +k] = 0
                            array[fila+j][columna-k] = 0

                except:
                    print("Hubo una celda que no se pudo cambiar")
            
            
    try:
        for i in range(n):
            array[0][i] = 0
            array[i][0] = 0
            array[n-1][i] = 0
            array[i][n-1] = 0
    except:
        print("Algo no funcionó bien")   
    


    df = pd.DataFrame(array)
    archivo = "archivos excel/matriz_opti.xlsx"
    try:
        df2 = pd.DataFrame(lectura_matriz("archivos excel/resulta_2.xlsx"))

    except:
        pass

    with pd.ExcelWriter(archivo) as writer:
        df.to_excel(writer, sheet_name= "Grilla de Validez", index=False)
        try:
            df2 = pd.DataFrame(lectura_matriz("archivos excel/resulta_2.xlsx"))
            df2.to_excel(writer, sheet_name= "Grilla de Construccion", index=False)
        except:
            pass

def lectura_matriz(archivo_excel):
    dataset = pd.read_excel(archivo_excel)
    lista = dataset.iloc[:, :].values
    lista = lista.tolist()
    return lista


print("El archivo grilla.py fue ejecutado")

if __name__ == "__main__":
    pass