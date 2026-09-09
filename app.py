from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

@app.route("/")
def home():
    return "BMI Backend Running"

@app.route("/calculate", methods=["POST"])
def calculate():
    data = request.get_json()

    name = data.get("name")
    height = float(data.get("height"))
    weight = float(data.get("weight"))

    bmi = round(weight / ((height / 100) ** 2), 2)

    if bmi < 18.5:
        category = "Underweight"
    elif bmi < 25:
        category = "Normal Weight"
    elif bmi < 30:
        category = "Overweight"
    else:
        category = "Obese"

    return jsonify({
        "name": name,
        "bmi": bmi,
        "category": category
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
