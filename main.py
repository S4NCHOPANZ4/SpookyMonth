import time
import tweepy
import os
from datetime import datetime
from dotenv import load_dotenv

# Cargar las claves desde el archivo .env
load_dotenv()

consumerKey = os.getenv("consumer_key")
consumerSecret = os.getenv("consumer_secret")
accessToken = os.getenv("access_token")
accessTokenSecret = os.getenv("access_token_secret")
bearer_token = os.getenv("bearer_token")  # Necesario para la API v2

# Autenticación con la API v2 (usando bearer token)
client = tweepy.Client(bearer_token=bearer_token, 
                       consumer_key=consumerKey, 
                       consumer_secret=consumerSecret, 
                       access_token=accessToken, 
                       access_token_secret=accessTokenSecret)

def is_it_spookymonth():
    spookyMonth = datetime(datetime.now().year, 10, 1)
    now = datetime.now()
    if now.month == spookyMonth.month:
        return(True, 0)
    if now > spookyMonth:
        spookyMonth = datetime(datetime.now().year + 1, 9, 1)    
    time_left = spookyMonth - now
    days_left = time_left.days
    return (False, days_left)

# Publicar un tweet usando API v2
def post_tweet(tweetContent):
    try:
        response = client.create_tweet(text=tweetContent)
        print(f"Tweet published succesfuly id: {response.data['id']}")
    except Exception as e:
        print(f"Error creating tweet: {e}")

def tweet_daily():
    tweet_count = 2
    spookyMont = is_it_spookymonth()
    while True: 
        try:
            if spookyMont[0]:
                tweet_content = f"It's Spooky month"
                post_tweet(tweet_content)
                tweet_count += 1
            else:
                tweet_content = f"Days left for Spooky Month {spookyMont[1]}"
            time.sleep(240)  # Pausar 240 segundos (4 minutos)
        except Exception as e:
            print(f"Error on tweet_daily: {e}")
            time.sleep(240)  

tweet_daily()



# def like_tweet(tweet_id):
#     try:
#         response = client.like(tweet_id)
#         print(f"Tweet likeado exitosamente. ID del tweet: {response.data}")
#     except Exception as e:
#         print(f"Error al publicar el tweet: {e}")


# Llamada para publicar un tweet

