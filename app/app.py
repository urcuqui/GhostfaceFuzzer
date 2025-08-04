from flask import Flask, render_template, request, jsonify
import joblib
import os
from attacks.cypher import stego
app = Flask(__name__)

#model_filename = os.path.join(os.path.dirname(__file__), 'full.joblib')

#loaded_model = joblib.load(model_filename)

def classify_message(text):    
    predictions = loaded_model.predict([text])
    if predictions[0] == 0:
        return "0-250000"
    elif predictions[0] == 1:
        return "250000-350000"
    elif predictions[0] == 2:
        return "350000-450000"
    elif predictions[0] == 3:
        return "450000-550000"
    else:
        return "650000+"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/classify", methods=["POST"])
def classify():
    data = request.get_json()
    message = data.get("message", "")   
    result = classify_message(message)    
    return jsonify({"result": result})

@app.route("/hide_message", methods=["POST"])
def stego_img():
    file = request.files["image"]
    if not file:
        return "No images uploaded", 400
    text_tohidden = request.values["texthidden"]
    file_stego = os.path.join(os.path.dirname(__file__), 'imagen_con_mensaje.png')
    result = stego.hide_message(file, text_tohidden, file_stego)    
    return render_template("index.html", result=result)   
    

@app.route('/ping')
def ping():
    import time
    time.sleep(0.1)  # Simula trabajo del servidor
    return 'pong'


if __name__ == "__main__":
    app.run(debug=False)
    