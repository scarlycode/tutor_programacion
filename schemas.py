from dataclasses import dataclass

MAX_PREGUNTA = 500
MAX_HISTORIAL = 6


class ErrorValidacion(ValueError):
    """Se lanza cuando la solicitud del navegador no es válida."""


@dataclass
class SolicitudPregunta:
    pregunta: str
    historial: list[tuple[str, str]]


def validar_solicitud(datos) -> SolicitudPregunta:
    if not isinstance(datos, dict):
        raise ErrorValidacion("La solicitud debe ser un JSON válido.")

    pregunta = datos.get("pregunta")
    if not isinstance(pregunta, str) or not pregunta.strip():
        raise ErrorValidacion("Escribe una pregunta.")
    pregunta = pregunta.strip()
    if len(pregunta) > MAX_PREGUNTA:
        raise ErrorValidacion(f"La pregunta no puede pasar de {MAX_PREGUNTA} caracteres.")

    historial = []
    mensajes = datos.get("historial", [])
    if isinstance(mensajes, list):
        for m in mensajes[-MAX_HISTORIAL:]:
            if not isinstance(m, dict):
                continue
            rol, texto = m.get("rol"), m.get("texto")
            if rol in ("usuario", "tutor") and isinstance(texto, str):
                historial.append(("human" if rol == "usuario" else "ai", texto))

    return SolicitudPregunta(pregunta=pregunta, historial=historial)