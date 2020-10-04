import requests
import json
from datetime import date, timedelta

BASE_API_URL = 'https://covid19.mathdro.id/api/daily'
NOT_FOUND_EXCEPTION = "Not Found"

def lambda_handler(event, context):
  today = date.today()
  today_fmt = today.strftime("%m-%d-%y")
  today_url = f'{BASE_API_URL}/{today_fmt}'
  r = requests.get(today_url)

  if r.reason == NOT_FOUND_EXCEPTION:
    yesterday = today - timedelta(days=1)
    yesterday_fmt = yesterday.strftime("%m-%d-%y")
    yesterday_url = f'{BASE_API_URL}/{yesterday_fmt}'
    r = requests.get(yesterday_url)

  data = json.loads(r.text)

  for o in data:
    if o["admin2"] == "Sacramento":
      print(o)

if __name__ == "__main__":
  lambda_handler(None, None)