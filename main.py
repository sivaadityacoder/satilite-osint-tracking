import requests
import json
import datetime
import matplotlib.pyplot as plt
import numpy as np
import os
from flask import Flask, render_template_string

API_KEY = '62YKNK-M4TZJX-5BB6WQ-5I6Q'  # Replace with your API key
LAT, LON, ALT = 28.6139, 77.2090, 0  # Your location (example: New Delhi)
SAT_ID = 25544  # ISS

# Flask app setup
app = Flask(__name__)

# Fetch satellite pass data
def fetch_passes():
    url = f"https://api.n2yo.com/rest/v1/satellite/radiopasses/{SAT_ID}/{LAT}/{LON}/{ALT}/1/45/&apiKey={API_KEY}"
    r = requests.get(url)
    if r.status_code == 200:
        data = r.json()

        # Ensure 'passes' key exists
        if 'passes' not in data:
            raise KeyError(f"API response does not contain 'passes'. Full response:\n{data}")

        os.makedirs("logs", exist_ok=True)
        with open("logs/ISS_passes.json", "w") as f:
            json.dump(data, f, indent=2)
        return data
    else:
        raise Exception(f"API request failed with status {r.status_code}: {r.text}")

# Convert UNIX timestamp to readable UTC string
def ts_to_utc(ts):
    return datetime.datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S UTC')

# Route: Live Satellite Passes
@app.route('/')
def index():
    try:
        data = fetch_passes()
        pass_list = []
        for i, p in enumerate(data['passes'], 1):
            pass_list.append({
                'id': i,
                'start': ts_to_utc(p['startUTC']),
                'startAz': p['startAz'],
                'startAzCompass': p['startAzCompass'],
                'maxUTC': ts_to_utc(p['maxUTC']),
                'maxEl': p['maxEl'],
                'maxAz': p['maxAz'],
                'maxAzCompass': p['maxAzCompass'],
                'end': ts_to_utc(p['endUTC']),
                'endAz': p['endAz'],
                'endAzCompass': p['endAzCompass']
            })

        return render_template_string("""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Satellite Tracker</title>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <link rel="stylesheet" href="https://unpkg.com/leaflet/dist/leaflet.css" />
            <style> #map { height: 80vh; } body { font-family: Arial; } </style>
        </head>
        <body>
            <h2>🛰️ ISS Passes over ({{ lat }}, {{ lon }})</h2>
            <ul>
                {% for p in passes %}
                <li>📡 Pass #{{ p.id }}: {{ p.start }} → {{ p.end }} | Max Elev: {{ p.maxEl }}°</li>
                {% endfor %}
            </ul>
            <div id="map"></div>

            <script src="https://unpkg.com/leaflet/dist/leaflet.js"></script>
            <script>
                var map = L.map('map').setView([{{ lat }}, {{ lon }}], 2);
                L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                    maxZoom: 18,
                    attribution: '© OpenStreetMap'
                }).addTo(map);
                L.marker([{{ lat }}, {{ lon }}]).addTo(map).bindPopup("Observer Location").openPopup();
            </script>
        </body>
        </html>
        """, lat=LAT, lon=LON, passes=pass_list)

    except Exception as e:
        return f"<h3>Error: {str(e)}</h3><p>Please check your API key, quota, or connection.</p>"

if __name__ == '__main__':
    app.run(debug=True)