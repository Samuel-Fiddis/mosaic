import os
from flask import Flask, request, send_file, jsonify
import base64
from flask_cors import CORS
from io import BytesIO
from datetime import datetime
from nearest_neighbour.utils import unpickle
from nearest_neighbour.ward_tree import WardTree  # Required for unpickling
from nearest_neighbour.faiss_index import FAISS  # Required for unpickling
from image_processing import process_image, load_image_to_array

app = Flask(__name__)

ALGORITHM_TYPE = os.getenv("ALGORITHM_TYPE", "ward_tree")
MAX_IMAGE_SIZE = int(os.getenv("MAX_IMAGE_SIZE", 16 * 1024 * 1024)) #bytes
MAX_AGE = 120 #seconds

algo = unpickle(
    os.getenv("ALGORITHM_FILE", f"/app/{ALGORITHM_TYPE}.pkl"),
    encoding="ASCII",
)

CORS(
    app,
    resources={
        r"/api/*": {
            "origins": [os.getenv("FRONTEND_URL", "http://localhost:3000")],
            "methods": ["GET", "POST", "OPTIONS"],
            "allow_headers": ["Content-Type"],
            "expose_headers": ["Content-Range", "X-Content-Range"],
            "supports_credentials": True,
            "max_age": MAX_AGE,
        }
    },
)

app.config["DEBUG"] = os.getenv("FLASK_DEBUG", "0") == "1"


@app.route("/api/health", methods=["GET"])
def health_check():
    return jsonify(
        {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "service": "Mosaic API",
        }
    )


@app.route("/api/create-mosaic", methods=["POST"])
def create_mosaic():
    """
    Accepts an image file in the request and returns the mosaic image.
    The image should be sent as multipart/form-data with the key 'image'.
    """
    byte_string = request.json["image"].split(",")[-1]
    image_data = base64.b64decode(byte_string)
    img_array = load_image_to_array(image_data)
    new_image = process_image(img_array, algo)

    img_io = BytesIO(new_image)
    img_io.seek(0)

    content_type = "image/jpeg"
    return send_file(img_io, mimetype=content_type)


@app.errorhandler(413)
def request_entity_too_large(error):
    return {"error": "File too large"}, 413


if __name__ == "__main__":
    app.config["MAX_CONTENT_LENGTH"] = MAX_IMAGE_SIZE
    app.run(host="0.0.0.0", port=5000)
