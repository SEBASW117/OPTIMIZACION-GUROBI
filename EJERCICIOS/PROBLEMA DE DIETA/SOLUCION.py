
import gurobipy as gp 
from gurobipy import * 

Categoria,Nutricion=gp.multidict({
    'Calorias':[500],
    'Chocolate':[6],
    'Azucar':[10],
    'Grasa':[8]})

comida,costo=gp.multidict({
   'BARRA DE CHOCOLATE':50,
   'HELADO DE CREMA DE CHOOCOLATE (1 BOLA)':20,
   'BEBIDA DE COLA (1 BOTELLA)':30,
   'PASTEL DE QUESO CON PINA (1 REBANADA)':80})

Valornutricional = {
    ('BARRA DE CHOCOLATE','Calorias'):400,
    ('BARRA DE CHOCOLATE','Chocolate'):3,
    ('BARRA DE CHOCOLATE','Azucar'):2,
    ('BARRA DE CHOCOLATE','Grasa'):2,
    ('HELADO DE CREMA DE CHOOCOLATE (1 BOLA)','Calorias'):200,
    ('HELADO DE CREMA DE CHOOCOLATE (1 BOLA)','Chocolate'):2,
    ('HELADO DE CREMA DE CHOOCOLATE (1 BOLA)','Azucar'):2,
    ('HELADO DE CREMA DE CHOOCOLATE (1 BOLA)','Grasa'):4,
    ('BEBIDA DE COLA (1 BOTELLA)','Calorias'):150,
    ('BEBIDA DE COLA (1 BOTELLA)','Chocolate'):0,
    ('BEBIDA DE COLA (1 BOTELLA)','Azucar'):4,
    ('BEBIDA DE COLA (1 BOTELLA)','Grasa'):1,
    ('PASTEL DE QUESO CON PINA (1 REBANADA)','Calorias'):500,
    ('PASTEL DE QUESO CON PINA (1 REBANADA)','Chocolate'):0,
    ('PASTEL DE QUESO CON PINA (1 REBANADA)','Azucar'):4,
    ('PASTEL DE QUESO CON PINA (1 REBANADA)','Grasa'):5,}


M=gp.Model("PROBLEMA DE DIETA")

X=M.addVars(comida,vtype=gp.GRB.CONTINUOUS,name="X")

M.setObjective(gp.quicksum(X[i]*costo[i] for i in comida), gp.GRB.MINIMIZE)

M.addConstrs((gp.quicksum(Valornutricional[i,j]*X[i] for i in comida)>= Nutricion[j] for j in Categoria))

M.optimize()

print()
print("El valor de la funcion objetivo es $",M.ObjVal)
for i in M.getVars():
    print(str(i.Varname)+"="+str(i.x))
print()    



