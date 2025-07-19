# Satellite OSINT Tracker

Track real-time satellite passes (like the ISS) over any location using Python, Flask, and the N2YO Satellite API.

> Built for cybersecurity researchers, red teamers, and OSINT analysts to simulate overhead reconnaissance windows and visualize satellite behavior.

---

##  Live Preview

The app fetches upcoming satellite passes over a chosen location and displays them along with a Leaflet.js map marking the observer's position.



---

## Features

- Real-time satellite pass tracking using N2YO API
-  Observer-defined location (latitude/longitude)
-  Pass details: Start/End times, Azimuth, Max Elevation
-  Live map (Leaflet + OpenStreetMap)
- API response logging in `/logs/ISS_passes.json`
- Secure error handling and graceful fallbacks

---

## Setup Instructions

### 1. Clone the repo

```bash
git clone https://github.com/your-username/satellite-osint-tracker.git
cd satellite-osint-tracker
