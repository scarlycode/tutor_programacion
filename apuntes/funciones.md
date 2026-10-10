# Funciones

Una función es un bloque de código con nombre que se puede reutilizar. Sirve para organizar el programa y evitar repetir código. En Python se crea con la palabra def, el nombre de la función, paréntesis y dos puntos.

Ejemplo de función sin parámetros:
```python
def saludar():
    print("Hola")
saludar()
```

Los parámetros son variables que la función recibe para trabajar con ellas. Se escriben dentro de los paréntesis al definir la función. Los valores concretos que se pasan al llamarla se llaman argumentos.
```python
def saludar(nombre):
    print("Hola", nombre)
saludar("Ana")
```

La palabra return devuelve un valor como resultado de la función, y ese valor se puede guardar en una variable. Cuando la función llega a un return, termina. Si una función no tiene return, devuelve None.
```python
def sumar(a, b):
    return a + b
resultado = sumar(2, 3)
print(resultado)
```

Diferencia entre print y return: print solo muestra algo en pantalla; return entrega un valor que el programa puede seguir usando.

Un parámetro puede tener un valor por defecto, que se usa si no se pasa ningún argumento al llamar la función. Ejemplo: def saludar(nombre="amigo").

Buenas prácticas: ponle a cada función un nombre claro, normalmente un verbo como calcular_total, y haz que cada función se encargue de una sola tarea.
