# Los generadores pueden ser creados de un aforam sencilla y en una sola linea de código. Su sintaxis es similar a las listas pero cambiando los [] por ().

# Este ejemplo con list comprehension sería:
lista = [2, 4, 6, 8, 10]
al_cuadrado = []
for x in lista:
    al_cuadrado.append(x**2)
print(al_cuadrado)     #se generan los valores de una lista elevaods al cuadrado

#lo mismo que: al_cuadrado = [x**2 for x in lista]

# Su equivalencia con generadores sería:
al_cuadrado_generador = (x**2 for x in lista)
print(al_cuadrado_generador)    #se genera un objeto generador

# Para los valores de nuestra lista iteramos sobre el generador:
for i in al_cuadrado_generador:
    print(i)