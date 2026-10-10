import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings

from db import buscar_apuntes

load_dotenv()

MODELO_EMBEDDINGS = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")

_embeddings: OpenAIEmbeddings | None = None


def _get_embeddings() -> OpenAIEmbeddings:
    """Crea el generador de embeddings una sola vez."""
    global _embeddings
    if _embeddings is None:
        _embeddings = OpenAIEmbeddings(model=MODELO_EMBEDDINGS)
    return _embeddings


def generar_embedding(texto: str) -> list[float]:
    """Convierte una pregunta en un vector de 1536 números."""
    return _get_embeddings().embed_query(texto)


def generar_embeddings(textos: list[str]) -> list[list[float]]:
    """Convierte varios fragmentos de apuntes en vectores (para cargar apuntes)."""
    return _get_embeddings().embed_documents(textos)


def recuperar_contexto(pregunta: str, cantidad: int = 4,
                       similitud_minima: float = 0.4) -> list[dict]:
    """Devuelve los fragmentos de apuntes más parecidos a la pregunta."""
    vector = generar_embedding(pregunta)
    fragmentos = buscar_apuntes(vector, cantidad)
    return [f for f in fragmentos if f["similitud"] >= similitud_minima]


def formatear_contexto(fragmentos: list[dict]) -> str:
    """Une los fragmentos en un solo texto para pasarlo al modelo."""
    if not fragmentos:
        return ""
    return "\n\n".join(f["contenido"] for f in fragmentos)


if __name__ == "__main__":
    vector = generar_embedding("¿Qué es una variable?")
    print("Tamaño del vector:", len(vector))

    resultados = recuperar_contexto("¿Qué es una variable?")
    print("Fragmentos encontrados:", len(resultados))