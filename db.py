import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

_cliente: Client | None = None


def get_client() -> Client:
    """Devuelve un único cliente de Supabase para todo el proyecto."""
    global _cliente
    if _cliente is None:
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_KEY")
        if not url or not key:
            raise RuntimeError("Faltan SUPABASE_URL o SUPABASE_KEY en el .env")
        _cliente = create_client(url, key)
    return _cliente


def insertar_apunte(contenido: str, embedding: list[float],
                    tema: str | None = None, fuente: str | None = None) -> dict:
    """Guarda un fragmento de apunte con su embedding."""
    fila = {
        "contenido": contenido,
        "tema": tema,
        "fuente": fuente,
        "embedding": embedding,
    }
    respuesta = get_client().table("apuntes").insert(fila).execute()
    return respuesta.data[0]


def buscar_apuntes(embedding: list[float], cantidad: int = 4) -> list[dict]:
    """Busca los fragmentos más parecidos usando la función match_apuntes."""
    respuesta = get_client().rpc(
        "match_apuntes",
        {"query_embedding": embedding, "match_count": cantidad},
    ).execute()
    return respuesta.data


if __name__ == "__main__":
    # Prueba rápida con un vector de mentira (no gasta llamadas a OpenAI)
    vector_prueba = [0.1] * 1536

    fila = insertar_apunte(
        "Prueba: una variable guarda un valor.",
        vector_prueba,
        tema="variables",
        fuente="prueba",
    )
    print("Insertado con id:", fila["id"])

    resultados = buscar_apuntes(vector_prueba, cantidad=1)
    print("Búsqueda devolvió:", resultados)

    # Limpieza: borra la fila de prueba
    get_client().table("apuntes").delete().eq("id", fila["id"]).execute()
    print("Fila de prueba eliminada")