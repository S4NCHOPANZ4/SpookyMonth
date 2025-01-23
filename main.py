import tweepy
import os
from datetime import datetime
from dotenv import load_dotenv
from PIL import Image, ImageDraw, ImageFont
import math 
import asyncio

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
auth = tweepy.OAuth1UserHandler(consumerKey, consumerSecret, accessToken, accessTokenSecret)
api = tweepy.API(auth)

async def is_it_spookymonth():
    spookyMonth = datetime(datetime.now().year, 10, 1)
    now = datetime.now()
    if now.month == spookyMonth.month:
        return(True, now.day)
    if now > spookyMonth:
        spookyMonth = datetime(datetime.now().year + 1, 9, 1)    

    
    time_left = spookyMonth - now
    days_left = time_left.days

    await create_loading_bar(math.floor(((365-days_left)*100)/365))

    return(False, days_left)

async def create_loading_bar(percent, width=700, height=80, output_file="loading_bar.png"):
    # Validar el porcentaje (debe estar entre 0 y 100)
    percent = max(0, min(100, percent))

    # Crear una imagen en blanco
    img = Image.new("RGBA", (width, height),  (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Dibujar el contorno de la barra de carga
    margin = 1 # Margen interno
    bar_width = width - 1 * margin
    bar_height = height // 2
    bar_x1 = margin
    bar_y1 = (height - bar_height) // 2
    bar_x2 = bar_x1 + bar_width
    bar_y2 = bar_y1 + bar_height
    draw.rectangle([bar_x1, bar_y1, bar_x2, bar_y2], outline="black", width=2)

    # Dibujar la parte llena de la barra de carga
    filled_width = bar_width * (percent / 100)
    draw.rectangle([bar_x1, bar_y1, bar_x1 + filled_width, bar_y2], fill="green")

    # Añadir el texto del porcentaje
    try:
        font = ImageFont.truetype("arial.ttf", size=15)  # Fuente personalizada
    except IOError:
        font = ImageFont.load_default()  # Fuente predeterminada en caso de error
    
    text = f"{percent}%"
    text_bbox = draw.textbbox((0, 0), text, font=font)  # Obtener el tamaño del texto
    text_width = text_bbox[2] - text_bbox[0]  # Ancho del texto
    text_height = text_bbox[3] - text_bbox[1]  # Alto del texto
    text_x = (width - text_width) // 2  # Centrar el texto horizontalmente
    text_y = (height - text_height -5) // 2  # Centrar el texto verticalmente
    draw.text((text_x, text_y), text, fill="white", font=font)

    # Guardar la imagen en un archivo
    img.save(output_file)
    print(f"Loading bar saved as {output_file}")
# Publicar un tweet usando API v2
def post_tweet(tweetContent):
    try:
        response = client.create_tweet(text=tweetContent)
        print(f"Tweet published succesfuly id: {response.data['id']}")
    except Exception as e:
        print(f"Error creating tweet: {e}")

def upload_image(file_path):
    try:
        # Subir la imagen a la API de Twitter
        media = api.media_upload(file_path)
        print(f"Media uploaded successfully with media_id: {media.media_id}")
        return media.media_id
    except Exception as e:
        print(f"Error uploading image: {e}")
        return None
async def post_tweet_with_image(tweet_content, image_path):
    try:
        # Subir la imagen primero
        media_id = upload_image(image_path)
        if media_id:
            # Crear el tweet con la imagen asociada
            response = client.create_tweet(text=tweet_content, media_ids=[media_id])
            print(f"Tweet with image published successfully! ID: {response.data['id']}")
        else:
            print("Image upload failed. Tweet was not created.")
    except Exception as e:
        print(f"Error creating tweet with image: {e}")


# post_tweet_with_image('content', './loading_bar.png')


async def tweet_daily():
    spookyMonth = await is_it_spookymonth()
    while True: 
        try:
            if spookyMonth[0]:
                tweet_content = f"It's Spooky month! \n It's Spooky Day #{spookyMonth[1]}! \n \n #spookymonth #spookymonthoc"
                post_tweet(tweet_content)
            else:
                tweet_content = f"{365 - spookyMonth[1]} days left until Spooky Month!  \n \n We’re {365 - spookyMonth[1]}/365 through! 👻 \n  \n #spookymonth #spookymonthoc"
                await post_tweet_with_image(tweet_content, './loading_bar.png')
            await asyncio.sleep(240)
                # Pausar 240 segundos (4 minutos)
        except Exception as e:

            print(f"Error on tweet_daily: {e}")
            await asyncio.sleep(240)
  
asyncio.run(tweet_daily())




# def like_tweet(tweet_id):
#     try:
#         response = client.like(tweet_id)
#         print(f"Tweet likeado exitosamente. ID del tweet: {response.data}")
#     except Exception as e:
#         print(f"Error al publicar el tweet: {e}")


# Llamada para publicar un tweet

