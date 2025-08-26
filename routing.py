from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import requests

app = Flask(__name__)
CORS(app)

GRAPHOPPER_API_KEY = ""

@app.route("/api/render-route", methods=["POST"])
def render_route():
    data = request.get_json()
    start = data.get("start")
    end = data.get("end")
    profile = data.get("profile")

    if not start or not end or not profile:
        return jsonify({"error": "Missing required parameters"}), 400

    lngA, latA = start
    lngB, latB = end

    url = (
        f"https://graphhopper.com/api/1/route"
        f"?point={latA},{lngA}&point={latB},{lngB}"
        f"&profile={profile}&points_encoded=false&key={GRAPHOPPER_API_KEY}"
    )

    try:
        response = requests.get(url)
        data = response.json()
        print("GraphHopper response:", data)
        coordinates = data.get("paths", [{}])[0].get("points", {}).get("coordinates")
        time = data.get("paths", [{}])[0].get("time")
        if not coordinates:
            return jsonify({"error": "Could not retrieve route coordinates"}), 500

        return jsonify({"coordinates": coordinates, "time": time})

    except Exception as e:
        print("GraphHopper error:", e)
        return jsonify({"error": "Routing failed"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))
    app.run(debug=True, host="0.0.0.0", port=port)
