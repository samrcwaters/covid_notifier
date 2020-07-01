import requests
import json

r = requests.get('https://covid19.mathdro.id/api/daily/6-29-2020')
data = json.loads(r.text)

for o in data:
  if o["admin2"] == "Yolo":
    print(o)