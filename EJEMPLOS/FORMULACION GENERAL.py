#FORMULAR UN CASO DE PYHTHON CON GUROBI EN FORMATO GENERAL 


#Importo el motor sus componentes 
import gurobipy as gp
from gurobipy import *


#Como son Variables Bidimensionales se debe crear un par de listas que nos ayude a crear los contadores X_ij 
#una lista para cada subindice 
partes=[1,2,3]
maquinas=[1,2]

#Con un generador dentro de la lista generamos las parejas X_11,X_21.....
Arco=[(i,j) for i in partes for j in maquinas]

#Como son parejas se crea un diccionario que contenga el parametro A_ij para cada pareja, similar a una matriz 2x2 
Tiempos={(1,1):0.02,(1,2):0.05,(2,1):0.03,(2,2):0.02,(3,1):0.05,(3,2):0.04}
#Diccionario para utilizadad C:ij 
utilidad={1:300,2:250,3:200}

#Inicializo el modelo creando una variable que lo contenga
m=gp.Model('segundo modelo ')

#Añado las variables, Var para una sola Vars para mas de una 

X=m.addVars(Arco,vtype=gp.GRB.CONTINUOUS,name="X")

#Ingreso la funcion objetivo 

m.setObjective(gp.quicksum(utilidad[i]*X[i,j] for i in partes for j in maquinas), gp.GRB.MAXIMIZE)

#Añado las restricciones, cuando es una sola Constr para mas de una estilo sumatoria Constr

m.addConstrs(gp.quicksum(Tiempos[i,j]*X[i,j] for i in partes)<=40 for j in maquinas) #gp.quicksum es una funcion de gurobi puede usarse sum de python tambien 
#m.addConstrs(sum(Tiempos[i,j]*X[i,j] for i in partes)<=40 for j in maquinas) 
m.addConstrs(X[i,j]>=0 for i in partes for j in maquinas)

#Le solciito que solucione 

m.optimize()

#Imprimo la solucion por consola 

print()
print("El valor de la funcion objetivo es", m.ObjVal)
for i in m.getVars():
    print(str(i.Varname)+"="+str(i.x))
print()    



