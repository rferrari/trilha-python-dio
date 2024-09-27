# Filtrar lista
numeros = [1, 30, 21, 2, 9, 65, 34]
pares = [numero for numero in numeros if numero % 2 == 0]
print(pares)

# Modificar valores
numeros = [1, 30, 21, 2, 9, 65, 34]
quadrado = [numero**2 for numero in numeros]
print(quadrado)

# Modificar valores
numeros = [1, 30, 21, 2, 9, 65, 34]
quadrado_pares = [numero**2 for numero in numeros if numero % 2 == 0]
print()
print(numeros)
print(quadrado_pares)

# Modificar valores
impares = numeros.copy()
for par in numeros:
    if(par %2 == 0):
        impares.remove(par)

quadrado_impar = [numero**2 for numero in numeros if numero % 2 != 0]
print()
print(impares)
print(quadrado_impar)


impares.clear()
print(impares)