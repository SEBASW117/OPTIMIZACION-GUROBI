from pydoc import apropos
import string
import gurobipy as gp
from gurobipy import *

minas=['Mina 1','Mina 2']
minerales=['Oro','Plata']

arco=[(i) for i in minas]

aporte={('Mina 1','Oro'):2,('Mina 1','Plata'):2,('Mina 2','Oro'):1,('Mina 2','Plata'):3}

requerimiento={'Oro':12,'Plata':18}

M=gp.Model("EJERCICIO MINA")

X=M.addVars(arco,vtype=gp.GRB.CONTINUOUS,name="X")

M.setObjective(gp.quicksum(X[i] for i in minas),gp.GRB.MINIMIZE)
    
M.addConstrs(gp.quicksum(X[i]*aporte[i,j] for i in minas)==requerimiento[j] for j in minerales)

M.optimize()

print()
print("La cantidad de dias que debe pasar en las minas es",M.ObjVal)
for i in M.getVars():
    print(str(i.Varname)+"="+str(i.x))
print()  



