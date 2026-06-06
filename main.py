from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage
import requests
import os
import random

today = datetime.now()
start_date = os.environ['START_DATE']
city = os.environ['CITY']
birthday = os.environ['BIRTHDAY']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
template_id = os.environ["TEMPLATE_ID"]


def get_weather():
  url = "https://wttr.in/" + city + "?format=j1"
  res = requests.get(url).json()
  current = res['current_condition'][0]
  weather = current['weatherDesc'][0]['value']
  temp = int(current['temp_C'])
  return weather, temp

def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

def get_birthday():
  year = date.today().year
  next = datetime.strptime(str(year) + "-" + birthday, "%Y-%m-%d")
  if next < today:
    next = next.replace(year=year + 1)
  return (next - today).days

def get_words():
  try:
    words = requests.get("https://v1.hitokoto.cn/?c=d&c=e&c=k")
    if words.status_code == 200:
      return words.json()['hitokoto']
  except:
    pass
  return "又是美好的一天"

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(app_id, app_secret)
wm = WeChatMessage(client)
wea, temperature = get_weather()
data = {
  "weather": {"value": wea},
  "temperature": {"value": temperature},
  "love_days": {"value": get_count()},
  "birthday_left": {"value": get_birthday()},
  "words": {"value": get_words(), "color": get_random_color()}
}
res = wm.send_template(user_id, template_id, data)
print(res)
