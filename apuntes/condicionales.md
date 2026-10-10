# Condicionales

Un condicional permite que el programa tome decisiones: ejecuta un bloque de código solo si se cumple una condición. En Python se escribe con if, seguido de la condición, dos puntos y un bloque indentado (con sangría).

Ejemplo de if:
```python
edad = 15
if edad >= 18:
    print("Eres mayor de edad")
```

El else se ejecuta cuando la condición del if no se cumple. Así el programa siempre tiene un camino alternativo.
```python
if edad >= 18:
    print("Mayor de edad")
else:
    print("Menor de edad")
```

El elif sirve para revisar varias condiciones en orden. Python evalúa de arriba hacia abajo y ejecuta solo el primer bloque cuya condición sea verdadera; si ninguna se cumple, ejecuta el else.
```python
nota = 8
if nota >= 9:
    print("Excelente")
elif nota >= 7:
    print("Bien")
else:
    print("A repasar")
```

Los operadores de comparación son == (igual), != (distinto), < (menor), > (mayor), <= (menor o igual) y >= (mayor o igual). Se pueden combinar con and (y), or (o) y not (no).

Error común: usar = en lugar de == para comparar. El signo = asigna un valor a una variable, mientras que == compara dos valores. Otro error frecuente es olvidar los dos puntos o la indentación después del if.
