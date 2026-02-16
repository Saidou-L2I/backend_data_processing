from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
from services.data_processor import DataProcessor

app = Flask(__name__)
CORS(app)

processor = DataProcessor()
"""UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)"""
UPLOAD_FOLDER = "uploads"       # pour les fichiers uploadés temporairement
RESULT_FOLDER = "results"       # pour les fichiers finaux à télécharger
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

"""@app.route("/process", methods=["POST"])
def process():
    file = request.files.get("file")
    if not file:
        return jsonify({"error": "No file"}), 400

    path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(path)

    options = request.form.to_dict()
    result = processor.process(path, options)

    os.remove(path)
    return jsonify(result)
"""
@app.route("/process", methods=["POST"])
def process():
    file = request.files.get("file")
    if not file:
        return jsonify({"error": "No file"}), 400

    # Sauvegarde temporaire
    temp_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(temp_path)

    # Récupération des options Angular
    options = request.form.to_dict()

    # Traitement
    result = processor.process(temp_path, options, result_folder=RESULT_FOLDER)

    # Supprime le fichier uploadé temporaire
    os.remove(temp_path)

    return jsonify(result)

"""@app.route("/download/<filename>")
def download(filename):
    return send_file(os.path.join(UPLOAD_FOLDER, filename), as_attachment=True)"""
@app.route("/download/<filename>")
def download(filename):
    file_path = os.path.join(RESULT_FOLDER, filename)
    if not os.path.exists(file_path):
        return jsonify({"error": "Fichier introuvable"}), 404

    return send_file(file_path, as_attachment=True)

@app.route("/", methods=["GET"])
def home():
    return {"message": "API Flask OK 🚀"}


if __name__ == "__main__":
    #app.run(debug=True)
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
