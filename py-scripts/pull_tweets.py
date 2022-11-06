#pip install tweepy
#pip install tweepy[async]

import pandas as pd
import numpy as np
import json
import tweepy
from tweepy import asynchronous
import asyncio
import time
from datetime import datetime, timedelta, date

config_path = "tweets\config.json"

with open(config_path) as json_file:
    config = json.load(json_file)

bearer_token = config["bearer-token"]
client = tweepy.asynchronous.AsyncClient(bearer_token=bearer_token)

keyword = 'elon'
no_tweets = 300

limit = int(np.ceil(no_tweets / 100))
data = []

async def fetch_tweet(keyword):
    response = await client.search_recent_tweets(keyword, 
                        tweet_fields=['created_at', 'lang','author_id'],max_results=100)
    return response

while limit > 0:
    response = asyncio.run(fetch_tweet(keyword))
    data.extend(response.data)
    time.sleep(30)
    limit -= 1

df = pd.DataFrame.from_dict(data)
df['keyword'] = keyword
df = df.drop_duplicates(['id'])
df = df.sort_values(by=['created_at'], ascending=False)
df = df.reset_index()

df.to_csv('tweets/'+keyword+'.csv', mode='a', index=False, header=False)
