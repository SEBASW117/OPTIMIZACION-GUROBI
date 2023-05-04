
# Caso de formulacion ampliada en gurobi


# importar gurobi, y del motor importar todo el contenido 

import gurobipy as gp
from gurobipy import *


#Inicializo el modelo creando una variable que lo contenga

m = gp.Model('Primermodelo')

#Añado las variables, Var para una sola Vars para mas de una 

xe=m.addVar(vtype=gp.GRB.CONTINUOUS,name='X1')
xi=m.addVar(vtype=gp.GRB.CONTINUOUS,name='X2')


#Ingreso la funcion objetivo 

m.setObjective(1*xe+2*xi,gp.GRB.MAXIMIZE)

#Añado las restricciones, cuando es una sola Constr para mas de una estilo sumatoria Constr

m.addConstr(xi<=60)
m.addConstr(2*xe+2*xi<=300)
m.addConstr(xe+3*xi<=200)
m.addConstr(xe>=0)
m.addConstr(xi>=0)


#Le solciito que solucione 
m.optimize()

#Imprimo la solucion por consola 

print()
print("El valor de la funcion objetivo es", m.ObjVal)
for i in m.getVars():
    print(str(i.Varname)+"="+str(i.x))
print()    

