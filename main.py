import time
import tweepy
import os
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

# Publicar un tweet usando API v2
def post_tweet(tweetContent):
    try:
        response = client.create_tweet(text=tweetContent)
        print(f"Tweet publicado exitosamente. ID del tweet: {response.data['id']}")
    except Exception as e:
        print(f"Error al publicar el tweet: {e}")

def tweet_daily():
    tweet_count = 2
    while True: 
        try:
            tweet_content = f"Tweet #{tweet_count} Tweets"
            post_tweet(tweet_content)
            tweet_count += 1
            time.sleep(240)  # Pausar 240 segundos (4 minutos)
        except Exception as e:
            print(f"Error al intentar publicar el tweet: {e}")
            time.sleep(240)  

tweet_daily()



# def like_tweet(tweet_id):
#     try:
#         response = client.like(tweet_id)
#         print(f"Tweet likeado exitosamente. ID del tweet: {response.data}")
#     except Exception as e:
#         print(f"Error al publicar el tweet: {e}")


# Llamada para publicar un tweet

