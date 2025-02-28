

from flask import Flask, request, jsonify
import pandas as pd
import os

app = Flask(__name__)

# Load the CSV file
csv_file = "medium_scraped_data.csv"

# Check if the file exists
if os.path.exists(csv_file):
    df = pd.read_csv(csv_file)
else:
    df = pd.DataFrame(columns=["Title", "Author", "URL", "Claps", "Reading Time", "Image Sources"])
    print("⚠️ Warning: CSV file not found. API will return empty results.")

@app.route("/")
def home():
    return "Flask API is Running on Railway!"

@app.route("/search", methods=["GET"])
def search_articles():
    keyword = request.args.get("keyword", "").lower()

    if not keyword:
        return jsonify({"error": "Please provide a keyword"}), 400

    # Filter articles by title
    if not df.empty:
        results = df[df["Title"].str.lower().str.contains(keyword, na=False)]
    else:
        return jsonify({"error": "No data available"}), 500

    if results.empty:
        return jsonify({"message": "No articles found"}), 404

    return jsonify(results.to_dict(orient="records"))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))  # Use Railway's assigned port
    app.run(debug=True, host="0.0.0.0", port=port)
