from flask import Flask, render_template, request, jsonify
from backend import tna, analytics

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/tna")
def tna_page():
    return render_template("tna.html")

@app.route("/analytics")
def analytics_page():
    return render_template("analytics.html")

@app.route("/submitTNA", methods=["POST"])
def submit_tna():
    data = request.json
    result = tna.save_tna(data)
    return jsonify(result)

@app.route("/getAnalytics")
def get_analytics():
    data = analytics.get_data()
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)