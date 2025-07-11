
from flask import Flask, render_template, request, redirect
import os
import requests

app = Flask(__name__)
app.config['DEBUG'] = True  # Add this line
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

TOYYIBPAY_SECRET_KEY = "yxeshtod-jksv-kfxh-ncn8-hgyvmlogor9l"
CATEGORY_CODE = "ealcq5p7"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/create-bill", methods=["POST"])
def create_bill():
    email = request.form["email"]
    payload = {
        "userSecretKey": TOYYIBPAY_SECRET_KEY,
        "categoryCode": CATEGORY_CODE,
        "billName": "AI + Similarity Checker",
        "billDescription": "RM1.50 for AI + Similarity Report",
        "billPriceSetting": 1,
        "billPayorInfo": 1,
        "billAmount": 150,
        "billReturnUrl": "https://schoolsolver.onrender.com/upload?email=" + email,
        "billTo": email,
        "billEmail": email,
        "billExternalReferenceNo": "AICHECK123",
        "billContentEmail": "Thank you for using our AI + Similarity service.",
        "billChargeToCustomer": 1,
    }

    r = requests.post("https://toyyibpay.com/index.php/api/createBill", data=payload)
    result = r.json()
    if "BillCode" in result[0]:
        billcode = result[0]["BillCode"]
        return redirect(f"https://toyyibpay.com/{billcode}")
    else:
        return "Error creating bill."

@app.route("/upload")
def upload_page():
    email = request.args.get("email", "")
    return render_template("upload.html", email=email)

@app.route("/upload", methods=["POST"])
def handle_upload():
    file = request.files["file"]
    email = request.form["email"]
    filename = file.filename
    file.save(os.path.join(UPLOAD_FOLDER, filename))
    print(f"Received from {email}: {filename}")
    return render_template("success.html")

if __name__ == "__main__":
    app.run(debug=True)
