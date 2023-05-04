#Modelo de planeacion agregada por capacidad constante

import gurobipy as gp
from gurobipy import *


#Listas de contadores para fuentes de produccion y periodos del horizonte de produccion
periodos=[1,2,3,4]
fuentes=[1,2,3]

#Parametros 
Demanda={1:200,2:300,3:1200,4:500}
Costo_hora_normal=20
Costo_hora_extra=25
Costo_subcobtratacion=30
Capacidad_normal=400
Capacidad_extra=100
Capacidad_subcontratacion=700
I_0=50
CM=5

m=gp.Model('Planeacion Agregada')

#Como son variables con contador, se deben especificar cuantas en el primer miembro de la funcion de variables
#la lista de periodos le ayudara a esta funcion a saber cuantas variables se deben crear
X=m.addVars(periodos,vtype=gp.GRB.CONTINUOUS,name="X")
Y=m.addVars(periodos,vtype=gp.GRB.CONTINUOUS,name="Y")
Z=m.addVars(periodos,vtype=gp.GRB.CONTINUOUS,name="Z")
I=m.addVars(periodos,vtype=gp.GRB.CONTINUOUS,name="I")


m.setObjective(sum(X[i]*Costo_hora_normal+Y[i]*Costo_hora_extra+Z[i]*Costo_subcobtratacion+I[i]*CM for i in periodos)),gp.GRB.MINIMIZE

#Como la primer restriccion liga un parametro a ella, se debe realizar de manera independiente para que los demas periodos no lo tomen
m.addConstr(X[1]+Y[1]+Z[1]+I_0 == Demanda[1]+I[1])

#del periodo dos en adelante no tomara el inventario iniciial, si no el inventario del periodo anterior dado por el modelo 
for i in range(2,len(periodos)+1):
        m.addConstrs(X[i]+Y[i]+Z[i]+I[i-1] == Demanda[i]+I[i] for j in fuentes)


m.addConstrs(X[i] <= Capacidad_normal  for i in periodos )
m.addConstrs(Y[i] <= Capacidad_extra  for i in periodos )
m.addConstrs(Z[i] <= Capacidad_subcontratacion for i in periodos )

m.optimize()

print()
print("El valor de la funcion objetivo es", m.ObjVal)
for i in m.getVars():
    print(str(i.Varname)+"="+str(i.x))
print()   