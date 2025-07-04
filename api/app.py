import os
from flask import Flask, request, send_file, jsonify
import base64
from flask_cors import CORS
from io import BytesIO
from datetime import datetime
import pickle
from nearest_neighbour.ward_tree import WardTree  # Import the WardTree class
from image_processing import process_image, load_image_to_array

app = Flask(__name__)

ALGORITHM_TYPE = os.getenv("ALGORITHM_TYPE", "ward_tree")  # Specify the type of tree you are using

algo = pickle.load(open(f"{ALGORITHM_TYPE}.pkl", "rb"))

CORS(
    app,
    resources={
        r"/api/*": {
            "origins": ["http://localhost:3000"],  # Allow only your frontend origin
            "methods": ["GET", "POST", "OPTIONS"],  # Allowed methods
            "allow_headers": ["Content-Type"],  # Allowed headers
            "expose_headers": ["Content-Range", "X-Content-Range"],
            "supports_credentials": True,  # Enable if you need to send cookies
            "max_age": 120,  # Cache preflight requests
        }
    },
)

# Enable debug mode for development
app.config["DEBUG"] = True


@app.route("/api/health", methods=["GET"])
def health_check():
    """Basic health check endpoint"""
    return jsonify(
        {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "service": "Flask API",
        }
    )


@app.route("/api/create-mosaic", methods=["POST"])
def create_mosaic():
    """
    Accepts an image file in the request and returns the same image.
    The image should be sent as multipart/form-data with the key 'image'.
    """
    # Read the image data
    byte_string = request.json["image"].split(",")[-1]

    image_data = base64.b64decode(byte_string)

    # Load the image data into a numpy array
    img_array = load_image_to_array(image_data)

    # Process the image
    new_image = process_image(img_array, algo)

    # Create a BytesIO object to send the file back
    img_io = BytesIO(new_image)
    img_io.seek(0)

    # Get the original content type
    content_type = "image/jpeg"

    return send_file(img_io, mimetype=content_type)


@app.errorhandler(413)
def request_entity_too_large(error):
    return {"error": "File too large"}, 413


if __name__ == "__main__":
    app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024
    app.run(host="0.0.0.0", port=5000)
