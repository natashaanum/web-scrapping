from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)

# Load the scraped data
df = pd.read_csv("medium_scraped_data.csv")

@app.route("/search", methods=["GET"])
def search_articles():
    keyword = request.args.get("keyword", "").lower()

    if not keyword:
        return jsonify({"error": "Please provide a keyword"}), 400

    # Filter articles by title
    results = df[df["Title"].str.lower().str.contains(keyword, na=False)]

    if results.empty:
        return jsonify({"message": "No articles found"}), 404

    # Convert results to JSON
    articles = results.to_dict(orient="records")
    return jsonify(articles)

if __name__ == "__main__":
    app.run(debug=True)
