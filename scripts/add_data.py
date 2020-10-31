import json
import random
from datetime import datetime

from faker import Faker
import requests

stream_name = 'vendorstream2'
api_url="https://qh2chdqyne.execute-api.us-east-1.amazonaws.com/dev/streams/{}/record".format(stream_name)

fake = Faker()

items = [
    "Backpack",
    "Waterbottle",
    "Tent",
    "Watch",
    "Boots",
    "Compass"
]

price = {}
price["Backpack"] = 100
price["Waterbottle"] = 7
price["Tent"] = 200
price["Watch"] = 50
price["Boots"] = 75
price["Compass"] = 25

record = {}
while True:
    record['user'] = fake.name()
    record['address'] = fake.address()
    record['time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    item = random.choice(items)
    record['item'] = item
    record['price'] = price[item]

    req_body = {}
    req_body['Data'] = record
    req_body['PartitionKey'] = "some key"

    r = requests.put(api_url, json=req_body)
    print(json.dumps(record))
    print(r.content)