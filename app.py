"""from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
from services.data_processor import DataProcessor

app = Flask(__name__)
CORS(app)

processor = DataProcessor()

UPLOAD_FOLDER = "uploads"
RESULT_FOLDER = "results"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)


@app.route("/process", methods=["POST"])
def process():
    try:
        file = request.files.get("file")
        if not file:
            return jsonify({"error": "No file"}), 400

        temp_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(temp_path)

        options = request.form.to_dict()

        result = processor.process(
            temp_path,
            options,
            result_folder=RESULT_FOLDER
        )

        os.remove(temp_path)

        return jsonify(result)

    except Exception as e:
        print("ERREUR PROCESS:", str(e))
        return jsonify({"error": str(e)}), 500


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
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)"""
###################" Nouveau
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
from services.data_processor import DataProcessor

app = Flask(__name__)
CORS(app)

processor = DataProcessor()
ALLOWED_EXTENSIONS = {"csv", "xlsx", "xls", "json", "xml"}
UPLOAD_FOLDER = "uploads"
RESULT_FOLDER = "results"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)


# 🔥 ROUTE PRINCIPALE
@app.route("/process", methods=["POST"])
def process():
    temp_path = None

    try:
        # 📥 Récupération fichier
        file = request.files.get("file")
        if not file:
            return jsonify({
                "success": False,
                "message": "Aucun fichier envoyé"
            }), 200   # 👈 pas de 500

        # 💾 Sauvegarde temporaire
        temp_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(temp_path)

        # ⚙️ Récupération options
        options = request.form.to_dict()

        # 🔥 Conversion types (IMPORTANT)
        options["normalize"] = options.get("normalize", "false") == "true"

        # ⚡ Traitement
        result = processor.process(
            temp_path,
            options,
            result_folder=RESULT_FOLDER
        )

        return jsonify(result)

    except Exception as e:
        print("🔥 ERREUR PROCESS:", str(e))

        # 🔥 Réponse safe (pas d'erreur 500 côté front)
        return jsonify({
            "success": False,
            "message": "Erreur interne serveur",
            "debug": str(e)  # ⚠️ à enlever en prod
        }), 200

    finally:
        # 🧹 Nettoyage fichier temporaire
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)


# 🔥 ROUTE DOWNLOAD
@app.route("/download/<filename>", methods=["GET"])
def download(filename):
    try:
        file_path = os.path.join(RESULT_FOLDER, filename)

        if not os.path.exists(file_path):
            return jsonify({
                "success": False,
                "message": "Fichier introuvable"
            }), 200

        return send_file(file_path, as_attachment=True)

    except Exception as e:
        print("🔥 ERREUR DOWNLOAD:", str(e))

        return jsonify({
            "success": False,
            "message": "Erreur lors du téléchargement",
            "debug": str(e)
        }), 200


# 🔥 ROUTE TEST
@app.route("/", methods=["GET"])
def home():
    return {
        "success": True,
        "message": "API Flask OK 🚀"
    }


# 🔥 LANCEMENT
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)