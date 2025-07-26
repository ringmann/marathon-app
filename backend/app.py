from flask import Flask, jsonify
from flask_cors import CORS
import requests
from flasgger import Swagger, swag_from

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}})

swagger = Swagger(app)
# swagger link is http://127.0.0.1:5000/apidocs/#/

@app.route("/api/races")
def get_public_races():
    """
    Get public races from RunSignup
    ---
    tags:
      - Races
    responses:
      200:
        description: A list of races
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
              name:
                type: string
              open:
                type: boolean
              link:
                type: string
              address:
                type: object
              city:
                type: string
              country:
                type: string
              state:
                type: string
    """
    url = "https://runsignup.com/rest/races"
    params = {
        "format": "json",
        "results_per_page": 10
    } 
    try:
        response = requests.get(url, params=params)
        data = response.json()
        races = []
        #Race keys: dict_keys(['race_id', 'name', 'last_date', 'last_end_date', 'next_date', 'next_end_date', 'is_draft_race', 'is_private_race', 'is_registration_open', 'created', 'last_modified', 'description', 'url', 'external_race_url', 'external_results_url', 'fb_page_id', 'fb_event_id', 'address', 'timezone', 'logo_url', 'real_time_notifications_enabled'])

        for race in data.get("races", []):
        
            race = race.get("race", {})
            print(race)
            races.append({
                "id": race.get("race_id"),
                "name": race.get("name", "").strip('"'), 
                "open": race.get("is_registration_open"),
                "link": race.get("external_race_url"),
                "address" : race.get("address"),
                "city": race.get("address").get("city"),
                "country": race.get("address").get("country_code"),
                "state": race.get("address").get("state")
            })
        
        return jsonify(races)
    except Exception as e:
        print("error")
        print(str(e))
        return jsonify({"error": str(e)}), 500



#   Todo:
# Get