from flask import Flask, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

# Directly stored API key (for dev/testing purposes only)
GRAPHOPPER_API_KEY = ""  # Replace with your key

@app.route("/api/render-route", methods=["GET"])
def render_route():
    # Hardcoded route: Times Square to Central Park
    start = (-73.9855, 40.7580)  # (lng, lat)
    end = (-73.9680, 40.7851)    # (lng, lat)
    profile = "car"

    lngA, latA = start
    lngB, latB = end

    url = (
        f"https://graphhopper.com/api/1/route"
        f"?point={latA},{lngA}&point={latB},{lngB}"
        f"&profile={profile}&points_encoded=false&key={GRAPHOPPER_API_KEY}"
    )

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        coordinates = data.get("paths", [{}])[0].get("points", {}).get("coordinates")

        if not coordinates:
            return jsonify({"error": "Could not retrieve route coordinates"}), 500

        return jsonify({
            "start": {"lat": latA, "lng": lngA},
            "end": {"lat": latB, "lng": lngB},
            "coordinates": coordinates
        })

    except Exception as e:
        print("GraphHopper error:", e)
        return jsonify({"error": "Routing failed"}), 500

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 3000))
    app.run(debug=True, host="0.0.0.0", port=port)
