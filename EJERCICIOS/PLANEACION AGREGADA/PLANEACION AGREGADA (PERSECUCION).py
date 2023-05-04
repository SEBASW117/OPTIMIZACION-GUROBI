import gurobipy as gp 

periodos=[1,2,3,4,5,6,7,8,9,10,11,12]
fuentes=[1,2,3]

Demanda=[0,3869,3674,5116,5742,5856,5949,6349,5424,6448,5868,4832,5143]

Costo_Deficit=10
Costo_Mantenimiento=8
Costo_Hora_Normal=45
Costo_Hora_Extra=55
Costo_Subcontratacion=80
Capacidad_Subcontratacion=800
I_0=1200
D_0=800
Restriccion_Inventario=240
Restriccion_Deficit=100

Trabajadores_Iniciales=20
Tasa_Produccion=1.2
Dias_Habiles=22
una_jornada=7.6
Costo_Contratar=120 
Costo_Despedir=230


m=gp.Model('Planeacion Agregada; Persecucion')


X=m.addVars(periodos,vtype=gp.GRB.CONTINUOUS,name="X")
Y=m.addVars(periodos,vtype=gp.GRB.CONTINUOUS,name="Y")
Z=m.addVars(periodos,vtype=gp.GRB.CONTINUOUS,name="Z")
I=m.addVars(periodos,vtype=gp.GRB.CONTINUOUS,name="I")
DE=m.addVars(periodos,vtype=gp.GRB.CONTINUOUS,name="DE")
E=m.addVars(periodos,vtype=gp.GRB.INTEGER,name="E")
EC=m.addVars(periodos,vtype=gp.GRB.INTEGER,name="EC")
ED=m.addVars(periodos,vtype=gp.GRB.INTEGER,name="ED")



m.setObjective(sum(X[i]*Costo_Hora_Normal+Y[i]*Costo_Hora_Extra+Z[i]*Costo_Subcontratacion+I[i]*Costo_Mantenimiento+DE[i]*Costo_Deficit+EC[i]*Costo_Contratar+ED[i]*Costo_Despedir for i in periodos)),gp.GRB.MINIMIZE

m.addConstr(X[1]+Y[1]+Z[1]+I_0 == Demanda[1]+I[1]+D_0-DE[1])

for i in range(2,len(periodos)+1):
        m.addConstrs(X[i]+Y[i]+Z[i]+I[i-1] == Demanda[i]+I[i]+DE[i-1]-DE[i] for j in fuentes)

m.addConstrs(X[i] <= (E[i]*Dias_Habiles*una_jornada*Tasa_Produccion)  for i in periodos)
m.addConstrs(Y[i] <= ((E[i]*Dias_Habiles*una_jornada*Tasa_Produccion)*0.25)  for i in periodos)
m.addConstrs(Z[i] <= Capacidad_Subcontratacion for i in periodos)

m.addConstrs(I[i] <= Restriccion_Inventario for i in periodos)

m.addConstrs(DE[i]<= Restriccion_Deficit for i in periodos)

m.addConstr(E[1]== Trabajadores_Iniciales+EC[1]-ED[1])

for i in range(2,len(periodos)+1):
        m.addConstrs(E[i]==E[i-1]+EC[i]-ED[i] for j in fuentes)

m.addConstrs(X[i] >= 0  for i in periodos)
m.addConstrs(Y[i] >= 0  for i in periodos)
m.addConstrs(Z[i] >= 0 for i in periodos)


#Optimialidad de enterios, modifica el parametro MIPGap, como si fuera optimalidad en excel 0% para optimos, mayor>0 para factibles

Gap=m.setParam('MIPGap',0)

m.optimize()

print()
print("El valor de la funcion objetivo es","$",m.ObjVal)
for i in m.getVars():
    print(str(i.Varname)+"="+str(i.x))
print()   
