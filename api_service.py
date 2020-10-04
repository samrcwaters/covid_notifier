import requests
import json
from datetime import date, timedelta

BASE_API_URL = 'https://covid19.mathdro.id/api/daily'
NOT_FOUND_EXCEPTION = "Not Found"

def lambda_handler(event, context):
  counties = ["Yolo", "Sacramento"]

  current_day = get_target_day()

  data = json.loads(current_day['text'])

  data = list(filter(lambda x: x["admin2"] in counties, data))
  print(data)

def get_day_data(day: date):
  today_fmt = day.strftime("%m-%d-%y")
  today_url = f'{BASE_API_URL}/{today_fmt}'
  return requests.get(today_url)

def get_target_day() -> object:
  info = ""
  r = get_day_data(date.today())

  if r.reason == NOT_FOUND_EXCEPTION:
    r = get_day_data(date.today() - timedelta(days=1))
    info = "Data has not yet been provided for today. This is yesterday's data."

  return {
    "text": r.text,
    "info": info
  }

if __name__ == "__main__":
  lambda_handler(None, None)