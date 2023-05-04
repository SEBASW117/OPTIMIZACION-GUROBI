#Prueba Pulp-Gurobi

import gurobipy as gp

Plantas=["Bogota","Sopo"]
Destinos=["Tunja","Cartagena","Cucuta"]

Ofertas={"Bogota":1000,"Sopo":1400}

Demandas={"Tunja":800,"Cartagena":1000,"Cucuta":600}

Costos=[
        [226,193,85],
        [199,223,218]]

Arco=[(i,j) for i in Plantas for j in Destinos]

costos_asignados=dict()

for i in range(len(Plantas)):
    for j in range(len(Destinos)):
        costos_asignados[Plantas[i], Destinos[j]] = Costos[i][j]


M=gp.Model("Prueba de Pulp")

X=M.addVars(Arco,vtype=gp.GRB.CONTINUOUS,name="X")

M.setObjective(gp.quicksum(X[i,j]*costos_asignados[i,j] for i in Plantas for j in Destinos),gp.GRB.MINIMIZE)

M.addConstrs(gp.quicksum(X[i,j] for i in Plantas) ==Demandas[j]  for j in Destinos)
M.addConstrs(gp.quicksum(X[i,j] for j in Destinos) == Ofertas[i] for i in Plantas)

M.optimize()

print()

print("El valor de la funcion objetivo es", M.ObjVal)
for i in M.getVars():
    print(str(i.Varname)+"="+str(i.x))


