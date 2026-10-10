import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser

from services.rag_service import recuperar_contexto, formatear_contexto

load_dotenv()

PROMPT_SISTEMA = """Eres un tutor de programación básica en Python para estudiantes principiantes.
Solo enseñas estos temas: variables, condicionales, bucles y funciones.

Reglas:
- Responde siempre en español, con un tono amable y paciente.
- Explica con palabras sencillas y agrega un ejemplo corto de código cuando ayude.
- Usa primero los apuntes del curso que aparecen abajo. Si no cubren la pregunta, puedes responder con conocimiento básico de Python, sin inventar datos.
- Si la pregunta no tiene que ver con programación básica, di amablemente que solo puedes ayudar con esos temas y sugiere una pregunta relacionada.
- No resuelvas tareas completas: guía al estudiante con pistas y explica el porqué.

Apuntes del curso:
{contexto}
"""

_prompt = ChatPromptTemplate.from_messages([
    ("system", PROMPT_SISTEMA),
    MessagesPlaceholder("historial"),
    ("human", "{pregunta}"),
])

_cadena = None


def _get_cadena():
    """Arma la cadena prompt -> modelo -> texto una sola vez."""
    global _cadena
    if _cadena is None:
        llm = ChatOpenAI(model=os.getenv("OPENAI_MODEL"))
        _cadena = _prompt | llm | StrOutputParser()
    return _cadena


def responder(pregunta: str, historial: list[tuple[str, str]] | None = None) -> dict:
    """Responde una duda usando los apuntes.

    historial: lista de tuplas como [("human", "..."), ("ai", "...")].
    Devuelve un diccionario con la respuesta y los archivos usados como fuente.
    """
    historial = (historial or [])[-6:]  # solo los últimos 6 mensajes
    fragmentos = recuperar_contexto(pregunta)
    contexto = formatear_contexto(fragmentos) or "(No se encontraron apuntes relacionados.)"

    respuesta = _get_cadena().invoke({
        "contexto": contexto,
        "historial": historial,
        "pregunta": pregunta,
    })
    fuentes = sorted({f["fuente"] for f in fragmentos if f.get("fuente")})
    return {"respuesta": respuesta, "fuentes": fuentes}


if __name__ == "__main__":
    for pregunta in ["¿Qué es una variable?", "¿Quién ganó el último mundial de fútbol?"]:
        resultado = responder(pregunta)
        print("PREGUNTA:", pregunta)
        print("RESPUESTA:", resultado["respuesta"])
        print("FUENTES:", resultado["fuentes"])
        print("-" * 40)