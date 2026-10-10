from pathlib import Path

from db import get_client, insertar_apunte
from services.rag_service import generar_embeddings

CARPETA_APUNTES = Path(__file__).resolve().parent.parent / "apuntes"
EXTENSIONES = {".md", ".txt"}


def dividir_en_fragmentos(texto: str, max_caracteres: int = 800) -> list[str]:
    """Agrupa párrafos hasta llegar al límite de caracteres."""
    parrafos = [p.strip() for p in texto.split("\n\n") if p.strip()]
    fragmentos, actual = [], ""
    for parrafo in parrafos:
        if actual and len(actual) + len(parrafo) + 2 > max_caracteres:
            fragmentos.append(actual)
            actual = parrafo
        else:
            actual = f"{actual}\n\n{parrafo}" if actual else parrafo
    if actual:
        fragmentos.append(actual)
    return fragmentos


def cargar_archivo(ruta: Path) -> int:
    """Sube un archivo a Supabase. Devuelve cuántos fragmentos guardó."""
    texto = ruta.read_text(encoding="utf-8")
    fragmentos = dividir_en_fragmentos(texto)
    if not fragmentos:
        return 0

    embeddings = generar_embeddings(fragmentos)

    # Borra lo anterior de este archivo para no duplicar si lo cargas de nuevo
    get_client().table("apuntes").delete().eq("fuente", ruta.name).execute()

    for fragmento, embedding in zip(fragmentos, embeddings):
        insertar_apunte(fragmento, embedding, tema=ruta.stem, fuente=ruta.name)
    return len(fragmentos)


def main() -> None:
    archivos = sorted(
        r for r in CARPETA_APUNTES.iterdir() if r.suffix.lower() in EXTENSIONES
    )
    if not archivos:
        print("No hay archivos .md o .txt en la carpeta apuntes/")
        return

    total = 0
    for ruta in archivos:
        cantidad = cargar_archivo(ruta)
        print(f"{ruta.name}: {cantidad} fragmentos")
        total += cantidad
    print(f"Listo. Total de fragmentos cargados: {total}")


if __name__ == "__main__":
    main()