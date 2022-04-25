import json
import requests
from flask import Flask, render_template, jsonify

app = Flask(__name__)

@app.route("/")
def index():
  return render_template("index.html")

@app.route("/users")
def users():
  return jsonify({
    "users": [
      {
        "name": "bob",
        "email": "bob@bobble.com"
      }    
    ]
  })

@app.route("/api/events")
def events():
  spreadsheetId = '1MQ5wMn7Q3AKmXnpxcXyh5yPAPwhUCkNEvQAAczZurEU'
  fields = 'sheets(properties.title,data.rowData.values.formattedValue)'
  ranges = '*!A2:H20'
  api_key = ''
  # Can't specify range because it would only return first spreadsheet.
  req = requests.get(f'https://sheets.googleapis.com/v4/spreadsheets/{spreadsheetId}?fields={fields}&key={api_key}')
  res = req.json()
  formatted_event_data = {}
  for sheet in res['sheets']:
    month = sheet['properties']['title']
    # Event data from specified fields
    events_data_raw = sheet['data'][0]['rowData'][1:]
    monthly_formatted_events = []
    for event_data_raw in events_data_raw:
      formatted_event = []
      for event_value in event_data_raw['values']:
        formatted_event.extend(list(event_value.values()))
      monthly_formatted_events.append(formatted_event)
    formatted_event_data[month] = monthly_formatted_events
  return jsonify(formatted_event_data)

app.run(debug = True)