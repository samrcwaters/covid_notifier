import requests
import json
from datetime import date, timedelta
from send_email import send_email

BASE_API_URL = 'https://covid19.mathdro.id/api/daily'
NOT_FOUND_EXCEPTION = "Not Found"

def lambda_handler(event, context):
  counties = ["Yolo", "Sacramento"]

  current_day = get_last_two_days_data()

  data = json.loads(current_day['text'])
  yday_data = json.loads(current_day['prev_day']['text'])

  statistics = get_statistics(
    list(filter(lambda x: x["admin2"] in counties, data)),
    list(filter(lambda x: x["admin2"] in counties, yday_data))
  )
  send_email(
    current_day['date'], 
    current_day['info'],
    statistics
  )

def get_statistics(today_data: dict, yesterday_data: dict) -> dict:
  stats = []
  for i in range(len(today_data)):
    stats.append({
      'county': today_data[i]['admin2'],
      'new_deaths': (int(today_data[i]['deaths']) - int(yesterday_data[i]['deaths'])),
      'new_cases': (int(today_data[i]['confirmed']) - int(yesterday_data[i]['confirmed'])),
      'total_cases': today_data[i]['confirmed'],
      'last_update': today_data[i]['lastUpdate'],
    })
  return stats

def get_day_data(day: date):
  today_fmt = day.strftime("%m-%d-%y")
  today_url = f'{BASE_API_URL}/{today_fmt}'
  return requests.get(today_url)

def get_last_two_days_data() -> dict:
  info = ""
  curr_day = date.today().strftime("%m-%d-%y")
  today_r = get_day_data(date.today())
  yesterday_r = get_day_data(date.today() - timedelta(days=1))

  if today_r.reason == NOT_FOUND_EXCEPTION:
    curr_day = (date.today() - timedelta(days=1)).strftime("%m-%d-%y")
    today_r, yesterday_r = yesterday_r, get_day_data(date.today() - timedelta(days=2))
    info = "PLEASE NOTE: Data has not yet been provided for today. This is yesterday's data."

  return {
    "text": today_r.text,
    "prev_day": {
      "text": yesterday_r.text
    },
    "info": info,
    "date": curr_day
  }

if __name__ == "__main__":
  lambda_handler(None, None)