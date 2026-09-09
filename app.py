from flask import Flask, request, jsonify, send_file
from flask_cors import CORS

import pandas as pd
import os

app = Flask(__name__)
CORS(app)

FILE_NAME = "bmi_records.xlsx"


@app.route("/download")
def download():

    return send_file(
        FILE_NAME,
        as_attachment=True
    )


@app.route("/")
def home():
    return "BMI Backend Running"
@app.route("/test")
def test():
    return jsonify({
        "status": "working"
    })

@app.route("/calculate", methods=["POST"])
def calculate():

    data = request.json

    name = data["name"]

    height = float(data["height"])
    weight = float(data["weight"])

    bmi = weight / ((height / 100) ** 2)

    bmi = round(bmi, 2)

    if bmi < 18.5:
        category = "Underweight"
        advice = """
    You are below the recommended weight range.

    Guidelines:
    • Eat nutritious foods regularly
    • Increase protein intake
    • Include nuts and dairy products
    • Consult a doctor if weight loss is unexplained
    """

    elif bmi < 25:
        category = "Normal Weight"
        advice = """
    Your BMI is within the healthy range.

    Guidelines:
    • Continue a balanced diet
    • Exercise regularly
    • Drink enough water
    • Maintain healthy sleep habits
    """

    elif bmi < 30:

        category = "Overweight"
        advice = """
    You are above the recommended weight range.

    Guidelines:
    • Reduce sugary foods
    • Walk or exercise daily
    • Increase fruits and vegetables
    • Limit junk food
    """

    else:
        category = "Obese"
        advice = """
    Your BMI is significantly above the healthy range.

    Guidelines:
    • Consult a healthcare professional
    • Follow a structured diet plan
    • Exercise regularly
    • Monitor weight progress
    """
    record = {

        "Name": name,
        "Height(cm)": height,
        "Weight(kg)": weight,
        "BMI": bmi,
        "Category": category
    }

    if os.path.exists(FILE_NAME):

        df = pd.read_excel(FILE_NAME)

        df = pd.concat(
            [df, pd.DataFrame([record])],
            ignore_index=True
        )

    else:

        df = pd.DataFrame([record])

    df.to_excel(FILE_NAME, index=False)

    return jsonify({

    "bmi": bmi,
    "category": category,
    "advice": advice

})

if __name__ == "__main__":
    app.run(debug=True)
