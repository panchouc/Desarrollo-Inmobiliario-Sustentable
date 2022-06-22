from gurobipy import Model, GRB, quicksum
from funciones_auxiliares.tensor import tensor, matriz
import datos as p
import pandas as pd
from math import sqrt
from subprocess import call
import os


def pasar_a_excel(matriz, archivo):
    Array = pd.DataFrame(matriz)
    Array.to_excel(archivo, index=False)

#Funciones que ayudan a visualizar las bases de los edificios modelados
#printea cada edificio en la terminal
def printear_cada_edificio():


    for k1 in K_:

        Matriz2 = matriz(p.I, p.J)

        for j1 in J_:
            for i1 in I_:
                valor = y[k1,j1,i1].x
                valor2 = x[k1,j1,i1].x

                if valor == 1:
                    #Nodos Interiores
                    Matriz2[j1-1][i1-1] = 2
                if valor2 == 1:
                    #Nodos Exteriores
                    Matriz2[j1-1][i1-1] = 3


#Matriz de todas las contrucciones a archivo de excel
def matriz_acumulada_a_excel(archivo):

    Matriz3 = matriz(p.I, p.J)

    for k1 in K_:

        for j1 in J_:
            for i1 in I_:
                valor = y[k1,j1,i1].x
                valor2 = x[k1,j1,i1].x

                if valor == 1:
                    #Nodos Interiores
                    Matriz3[j1 - 1][i1 - 1] = 2
                if valor2 == 1:
                    #Nodos Exteriores
                    Matriz3[j1 - 1][i1 - 1] = 3


    pasar_a_excel(Matriz3, archivo)

#Edificio deseado a excel
def matriz_deseada_a_excel(edificio, archivo):

    Matriz3 = matriz(p.I, p.J)

    for j1 in J_:
        for i1 in I_:
            valor = y[edificio,j1,i1].x
            valor2 = x[edificio,j1,i1].x

            if valor == 1:
                #Nodos Interiores
                Matriz3[j1 - 1][i1 - 1] = 2
            if valor2 == 1:
                #Nodos Exteriores
                Matriz3[j1 - 1][i1 - 1] = 3

    pasar_a_excel(Matriz3, archivo)


#Las funciones de arriba lamentablemente las tuvimos que dejar ahí, ya que si las pasamos a otro archivo no funcionan bien

def main():
    model = Model() 
    model.setParam("TimeLimit", 1800) #30 Minutos TimeLimit
    #######################
    ## C O N J U N T O S ##
    #######################
    global M_
    global I_
    global J_
    global K_
    global T_
    
    M_ = range(1, p.M + 1) 
    I_ = range(1, p.I + 1)
    J_ = range(1, p.J + 1)
    K_ = range(1, p.K + 1)
    T_ = range(1, p.T + 1)

    #######################
    ## V A R I A B L E S ##
    #######################
    global x
    global y
    global r
    global q
    global a
 
    
    x = model.addVars(K_,I_,J_, vtype = GRB.BINARY, name = "x_kij")
    y = model.addVars(K_,I_,J_, vtype = GRB.BINARY, name = "y_kij")
    r = model.addVars(K_, vtype = GRB.BINARY, name = "r_k")
    q = model.addVars(M_,T_,K_, vtype = GRB.CONTINUOUS, name = "q_mtk") 
    l = model.addVars(K_, vtype = GRB.INTEGER, name = "l_k")
    a = model.addVars(K_, vtype = GRB.INTEGER, name = "a_k")


    model.update()
    ###############################
    ## R E S T R I C C I O N E S ##
    ###############################

    #R1 - R2 Debe existir al menos cierta cantidad de nodos interiores y exteriores, esta cantidad esta determinada por los parametros elegidos.
    model.addConstrs(quicksum((y[k,i,j] for i in I_ for j in J_)) >= (int((sqrt(p.A_MAX) - 1)**2) - p.s)*r[k] for k in K_)
    model.addConstrs(quicksum((x[k,i,j] for i in I_ for j in J_)) >= 1*r[k] for k in K_)

    #R3 Debe existir al menos una edificación.
    model.addConstr(quicksum(r[k] for k in K_) >= 1)

    #R4 - R5 Los nodos frontera e interiores de un edificio que no se construye, deben ser cero
    model.addConstrs(quicksum(y[k,i,j] + x[k,i,j] for i in I_ for j in J_) >= 0 - p.BM * (1 - r[k]) for k in K_)
    model.addConstrs(quicksum(y[k,i,j] + x[k,i,j] for i in I_ for j in J_) <= 0 + p.BM * (1 - r[k]) for k in K_)

    #R6 La siguiente restriccion corresponde a la cantidad de area minima por cada habitante
    model.addConstr((1 / p.D) * quicksum(a[k] * p.H[(k)] for k in K_) >= p.c)

    #7 Solo se puede asignar personas en un edificio si este es construido
    model.addConstrs(l[k] <= r[k] * p.BM for k in K_)

    #R8 Se debe cumplir la cantidad de area minima por habitante, en cada piso de cada edificacion
    model.addConstrs(a[k] >= l[k] * p.c for k in K_)

    #R9 Se debe respetar el presupuesto disponible considerando los materiales comprados para construir los pisos de cada edificacion
    #model.addConstrs(p.P >= quicksum(p.G[(m)] * q[m,t,k] * p.H[(k)] * r[k] for k in K_ for m in M_) for t in T_)
    model.addConstr(p.P >= quicksum(p.G[(m)] * q[m,t,k] * p.H[(k)] for k in K_ for m in M_ for t in T_))


    #R10 Se debe cumplir con la demanda habitacional 
    model.addConstr(quicksum(l[k] * p.H[(k)] for k in K_) >= p.D)

    #R11 - 12 El area construida para cada edifcacion es:
    model.addConstrs(0.5 * quicksum(x[k,i,j] for i in I_ for j in J_) + quicksum(y[k,i,j] for i in I_ for j in J_) - 1 <= a[k] for k in K_)
    model.addConstrs(0.5 * quicksum(x[k,i,j] for i in I_ for j in J_) + quicksum(y[k,i,j] for i in I_ for j in J_) - 1 >= a[k] for k in K_)

    #R13 Cada planta no debe superar un area maxima
    model.addConstrs(a[k] <= p.A_MAX * r[k] for k in K_)

    #R14 Cada planta debe tener un area minima
    model.addConstrs(a[k] >= p.A_MIN * r[k] for k in K_)

    #R15 Cantidad minima de material por piso en cada edificacion
    model.addConstrs(quicksum(q[m,t,k] for m in M_) >= p.B[(t,k)]*r[k] for k in K_ for t in T_)

    #R16 La siguiente restriccion representa el hecho de que no puede haber un nodo frontera en un terreno invalido.
    model.addConstrs(quicksum(x[k,i,j] for k in K_) <= p.N[(i,j)] for i in I_ for j in J_)

    #R17 No puede haber un nodo interior en un terreno invalido
    model.addConstrs(quicksum(y[k,i,j] for k in K_) <= p.N[(i,j)] for i in I_ for j in J_)

    #R18 Un nodo puede ser frontera o interior, pero no ambos
    model.addConstrs(quicksum(x[k,i,j] + y[k,i,j] for k in K_) <= 1 for i in I_ for j in J_)

    #R19 Si un nodo es interno, estara rodeado de 9 nodos del edificio contandose a si mismo
    model.addConstrs(quicksum(x[k,i,j] + y[k,i,j] for i in range(a - 1, a + 2) for j in range(b - 1, b + 2)) >= 9 * y[k,a,b] for a in range(2, p.I) for b in range(2, p.J) for k in K_)

    #R20 - 21 Si un nodo es frontera, estara rodeado por otros dos nodos frontera
    model.addConstrs(x[k,a,b-1] + x[k,a-1,b] + x[k,a+1,b] + x[k,a,b+1] >= 2 - p.BM * (1 - x[k,a,b]) for a in range(2, p.I) for b in range(2, p.J) for k in K_)
    model.addConstrs(x[k,a,b-1] + x[k,a-1,b] + x[k,a+1,b] + x[k,a,b+1] <= 2 + p.BM * (1 - x[k,a,b]) for a in range(2, p.I) for b in range(2, p.J) for k in K_)
    #model.addConstrs(quicksum(x[k,i,j] for i in range(a - 1, a + 2) for j in range(b - 1, b + 2)) >= 3 * x[k,a,b] for a in range(2, p.I) for b in range(2, p.J) for k in K_)


    #R22 Naturaleza de variables
    model.addConstrs(q[m,t,k] >= 0 for m in M_ for t in T_ for k in K_)

    ####################################
    ## F U N C I Ó N  O B J E T I V O ##
    ####################################

    #Agregamos indice t a Qmtk, entonces hay que iterar sobre t también y cambió la F.O.
    funcion_objetivo = (1 / p.D) * quicksum(q[m,t,k] * p.H[(k)] * p.C[(m)] for t in T_ for m in M_ for k in K_ )
    model.setObjective(funcion_objetivo, GRB.MINIMIZE)
    model.optimize()

    ## VALOR OBJETIVO ##
    valor_objetivo = model.ObjVal
    print(f"El valor objetivo es {valor_objetivo}")

    ## Variables en el optimo ##

    def crear_txt(texto):
        archi1 = open("variables.txt", "a")
        archi1.write(texto)
        archi1.close()
        return texto

    
    for k in K_:
        print(
        crear_txt(f"""
        La variable r[{str(k)}] toma el valor de {r[k].x}
        La variable l[{str(k)}] toma el valor de {l[k].x}
        La variable a[{str(k)}] toma el valor de {a[k].x}
        La variable H[{str(k)}] toma el valor de {p.H[(k)]}
        """))

    
    
    model.write("Entrega3.lp")
    model.write("Entrega3.mps")

    try:
        matriz_acumulada_a_excel("archivos excel/resulta_2.xlsx")
        matriz_deseada_a_excel(2, "archivos excel/resulta_3.xlsx")
    except:
        pass 
    
    for v in model.getVars():
        archivo_1 = open("Valor_variables.txt", 'a')
        
        if v.x != 0:

            archivo_1.write(f"{v.varName}: {v.x}\n")
        archivo_1.close()

    print(f"El tiempo que demoró el modelo es de {model.runtime} segundos")


    cantidad_restricciones_activas = 0
    cantidad_total_restricciones = 0
    for c in model.getConstrs():
        if c.Slack == 0:
            cantidad_restricciones_activas += 1

        cantidad_total_restricciones += 1
    

    print(f"Existen {cantidad_total_restricciones} restricciones y de estas {cantidad_restricciones_activas} están activas.")

if __name__ == "__main__":
    try:
        
        if os.name == "posix":
            #Sistema operativo Linux/MACOS
            call('python3 funciones_auxiliares/grilla.py', shell=True)
            call('python3 datos.py', shell=True)
            call('python3 funciones_auxiliares/grilla.py', shell=True)
            call('python3 datos.py', shell=True)
        
            main()
        
        elif os.name == "nt":
            #Sistema operativo Windows
            call('python funciones_auxiliares/grilla.py', shell=True)
            call('python datos.py', shell=True)
            call('python funciones_auxiliares/grilla.py', shell=True)
            call('python datos.py', shell=True)
            main()

    except Exception as ex:
        print("Un error ha ocurrido")
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"   
        print(f"El error es {template.format(type(ex).__name__, ex.args)}")     
    
    