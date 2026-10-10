import os
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request

from schemas import ErrorValidacion, validar_solicitud
from services.tutor_service import responder

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")


@app.get("/")
def inicio():
    return render_template("index.html")


@app.post("/api/preguntar")
def preguntar():
    try:
        solicitud = validar_solicitud(request.get_json(silent=True))
    except ErrorValidacion as e:
        return jsonify({"error": str(e)}), 400

    try:
        resultado = responder(solicitud.pregunta, solicitud.historial)
    except Exception:
        app.logger.exception("Error al responder")
        return jsonify({"error": "No pude responder ahora. Intenta de nuevo."}), 500

    return jsonify(resultado)


if __name__ == "__main__":
    app.run(debug=True)