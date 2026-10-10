from services.tutor_service import responder

# fuente: apunte que debería usarse (None = pregunta fuera de tema, sin fuentes)
# claves: la respuesta debe mencionar AL MENOS UNA de estas palabras
CASOS = [
    {"pregunta": "¿Qué es una variable?", "fuente": "variables.md", "claves": ["valor", "nombre"]},
    {"pregunta": "¿Qué tipos de datos básicos hay en Python?", "fuente": "variables.md", "claves": ["int", "str"]},
    {"pregunta": "¿Cómo uso un if y un else?", "fuente": "condicionales.md", "claves": ["if"]},
    {"pregunta": "¿Para qué sirve elif?", "fuente": "condicionales.md", "claves": ["elif"]},
    {"pregunta": "¿Cómo repito algo 10 veces?", "fuente": "bucles.md", "claves": ["for", "range"]},
    {"pregunta": "¿Qué diferencia hay entre for y while?", "fuente": "bucles.md", "claves": ["while"]},
    {"pregunta": "¿Cómo creo una función con parámetros?", "fuente": "funciones.md", "claves": ["def"]},
    {"pregunta": "¿Para qué sirve return?", "fuente": "funciones.md", "claves": ["return"]},
    {"pregunta": "¿Quién ganó el último mundial de fútbol?", "fuente": None, "claves": []},
    {"pregunta": "¿Cuál es la capital de Francia?", "fuente": None, "claves": []},
]


def evaluar_caso(caso: dict) -> tuple[bool, bool, list[str]]:
    resultado = responder(caso["pregunta"])
    fuentes = resultado["fuentes"]
    texto = resultado["respuesta"].lower()

    if caso["fuente"] is None:
        fuente_ok = fuentes == []
    else:
        fuente_ok = caso["fuente"] in fuentes

    claves_ok = True if not caso["claves"] else any(c.lower() in texto for c in caso["claves"])
    return fuente_ok, claves_ok, fuentes


def main() -> None:
    aprobados = fuentes_bien = claves_bien = 0

    for caso in CASOS:
        try:
            fuente_ok, claves_ok, fuentes = evaluar_caso(caso)
        except Exception as e:
            print(f"[ERROR] {caso['pregunta']} -> {type(e).__name__}")
            continue

        fuentes_bien += fuente_ok
        claves_bien += claves_ok
        aprobo = fuente_ok and claves_ok
        aprobados += aprobo

        estado = "OK   " if aprobo else "FALLA"
        print(f"[{estado}] {caso['pregunta']}")
        print(f"         fuente: {'ok' if fuente_ok else 'mal'} {fuentes} | claves: {'ok' if claves_ok else 'mal'}")

    total = len(CASOS)
    print("-" * 50)
    print(f"Casos aprobados:    {aprobados}/{total}")
    print(f"Fuente correcta:    {fuentes_bien}/{total}")
    print(f"Conceptos clave:    {claves_bien}/{total}")


if __name__ == "__main__":
    main()