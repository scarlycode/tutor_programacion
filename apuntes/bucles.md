# Bucles

Un bucle repite un bloque de código varias veces, para no escribir lo mismo muchas veces. Python tiene dos tipos principales: for y while.

El bucle for recorre una secuencia, como una lista, un texto o un rango de números. La función range(n) genera los números desde 0 hasta n-1. Para repetir algo 10 veces se usa for con range(10).
```python
for i in range(10):
    print("Hola")
```

También se puede recorrer una lista elemento por elemento:
```python
frutas = ["manzana", "pera", "uva"]
for fruta in frutas:
    print(fruta)
```

El bucle while repite el bloque mientras una condición sea verdadera. Es útil cuando no sabes cuántas veces hay que repetir.
```python
contador = 0
while contador < 3:
    print(contador)
    contador = contador + 1
```

Diferencia entre for y while: usa for cuando sabes cuántas veces o sobre qué elementos vas a repetir; usa while cuando la repetición depende de una condición que puede cambiar en cualquier momento.

Cuidado con el bucle infinito: si en un while la condición nunca deja de ser verdadera, el programa no termina. Asegúrate de modificar la variable de la condición dentro del bucle.

La instrucción break termina el bucle de inmediato, y continue salta a la siguiente repetición sin ejecutar el resto del bloque.
