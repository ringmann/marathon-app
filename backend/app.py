from flask import Flask, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}})

@app.route("/api/races")
def get_public_races():
    print("in api")
    url = "https://runsignup.com/rest/races"
    params = {
        "format": "json",
        "results_per_page": 10
    } 
    try:
        response = requests.get(url, params=params)
        data = response.json()
        #print("hello")
        #print(data)
        races = []
        for race in data.get("races", []):
        
            race = race.get("race", {})
            print(race)
            races.append({
                "id": race.get("race_id"),
                #"name": race.get("name"),
                "name": race.get("name", "").strip('"') 
                #"location": f"frace.get('city')}, trace.get ('state')?",
                # "date": race.get("race_date")
            })
        
        return jsonify(races)
    except Exception as e:
        print("error")
        print(str(e))
        return jsonify({"error": str(e)}), 500