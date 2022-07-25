import os
import requests
from dotenv import load_dotenv
from datetime import datetime
from flask import Flask, render_template, jsonify
from flask_cors import CORS

load_dotenv()
app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'

CORS(app)

ENV = os.environ.get("env")
print(ENV);
PORT = 8080 if ENV == "PRODUCTION" else 5050
DEBUG = True if ENV == "DEVELOPMENT" else False

@app.route("/")
def index():
  return render_template("index.html")

@app.route("/users", methods=["GET"])
def users():
  return jsonify({
    "users": [
      {
        "name": "bob",
        "email": "bob@bobble.com"
      }    
    ]
  })

@app.route("/api/events", methods=["GET"])
def events():
  try:
    spreadsheetId = '16Nx4J93o5kNA22tLcIXEwGonr_t41tQC-4-7ZnFIhE8'

    fields = 'sheets(properties.title,data.rowData.values.formattedValue)'
    api_key = 'AIzaSyCoCQzgwvpEqdPIycVbvTH3mytxZRFc0bs'

    req = requests.get(f'https://sheets.googleapis.com/v4/spreadsheets/{spreadsheetId}?fields={fields}&key={api_key}')
    res = req.json()

    # dictionary that will be populated with lists
    # containing formatted events by month
    # {
    #  July 2022: [{"title": ...}, {"title": ...}],
    #  June 2022: [{"title": ...}]
    # }
    formatted_event_data = {}

    # spreadsheet shape
    event_fields = ['title', 'description', 'type', 'date', 'time', 'location', 'rsvp', 'checkin', 'contact', 'thumbnail']

    for sheet in res['sheets']:
      month_year = sheet['properties']['title']
      # Only parse events starting from June 2022
      if month_year == "May 2022": break

      # list that will be put into the formatted_event_data
      # dictionary with respective month like so:
      # [{"title": ...}, {"title": ...}]
      monthly_formatted_events = []

      # looking at the raw response will help
      # understand why this mess is necessary
      events_data_raw = sheet['data'][0]['rowData'][1:]

      for event_data_raw in events_data_raw:
        formatted_event = {}
        for field, event_value in zip(event_fields, event_data_raw['values']):

          # sometimes fields are blank
          try: formatted_event[field] = list(event_value.values())[0]
          except: formatted_event[field] = ''

        # date time parsing
        unformatted_time = formatted_event['time'].split('-')
        unformatted_date = formatted_event['date'].split('-')
        start_time = unformatted_time[0].strip()
        start_date = unformatted_date[0].strip()

        # sometimes there's no end time/date
        try: end_time = unformatted_time[1].strip()
        except: end_time = start_time

        try: end_date = unformatted_date[1].strip()
        except: end_date = start_date

        year = month_year.split()[1]

        # error handling for events with TBD times
        # assumes there is always at least a starting date
        try: start_epoch = datetime.strptime(f'{start_date}/{year} {start_time}', '%m/%d/%Y %I:%M %p').timestamp()
        except: start_epoch = datetime.strptime(f'{start_date}/{year}', '%m/%d/%Y').timestamp()

        try: end_epoch = datetime.strptime(f'{end_date}/{year} {end_time}', '%m/%d/%Y %I:%M %p').timestamp()
        except: end_epoch = datetime.strptime(f'{end_date}/{year}', '%m/%d/%Y').timestamp()

        formatted_event['startTime'] = start_epoch
        formatted_event['endTime'] = end_epoch

        formatted_event.pop('date')
        formatted_event.pop('time')

        # append single parsed event to current month's list of events
        monthly_formatted_events.append(formatted_event)

      # append an entire month's events to the response json
      formatted_event_data[f'{month_year}'] = monthly_formatted_events

    # if all goes well...
    return jsonify(formatted_event_data), 200
  except:
    # otherwise try to return error within initial request
    try: return res['error']['message'], 400
    # if that isn't wrong then there's a bug somewhere in this code
    except: return 'Something went wrong.', 500

if __name__ == "__main__":
  app.run(debug = DEBUG, port=PORT)