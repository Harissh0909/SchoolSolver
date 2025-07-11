
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
    try:
        print("🔥 Creating bill...")

        email = request.form.get("email")
        print(f"📩 Email received: {email}")

        if not email:
            return "No email provided", 400

        payload = {
            "userSecretKey": TOYYIBPAY_SECRET_KEY,
            "categoryCode": CATEGORY_CODE,
            "billName": "AI + Similarity Checker",
            "billDescription": "RM1.50 for AI + Similarity Report",
            "billPriceSetting": 1,
            "billPayorInfo": 1,
            "billAmount": 150,  # 150 cents = RM1.50
            "billReturnUrl": f"https://schoolsolver.onrender.com/upload?email={email}",
            "billTo": email,
            "billEmail": email,
            "billPhone": "0177484311",
            "billExternalReferenceNo": "AICHECK123",
            "billContentEmail": "Thank you for using our AI + Similarity service.",
            "billChargeToCustomer": 1,
        }

        print("📤 Sending payload to ToyyibPay...")
        print(payload)

        response = requests.post("https://toyyibpay.com/index.php/api/createBill", data=payload)
        print(f"✅ HTTP status: {response.status_code}")
        print("🔁 Raw response text:", response.text)

        result = response.json()
        print("📦 Parsed JSON:", result)

        if isinstance(result, list) and "BillCode" in result[0]:
            billcode = result[0]["BillCode"]
            print(f"🔗 Redirecting to ToyyibPay with BillCode: {billcode}")
            return redirect(f"https://toyyibpay.com/{billcode}")
        else:
            return f"❌ Error creating bill: {result}", 500

    except Exception as e:
        print("🔥 Fatal Error in /create-bill:", str(e))
        return f"❗ Internal Server Error: {str(e)}", 500

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
