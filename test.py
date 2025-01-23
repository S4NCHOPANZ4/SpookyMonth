from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import math
import asyncio



# Generar una barra de carga al 75%

def is_it_spookymonth():
    spookyMonth = datetime(datetime.now().year, 10, 1)
    now = datetime(datetime.now().year, 9, 30)
    # now = datetime.now()
    if now.month == spookyMonth.month:
        print(now.day)
        return(True, 0)
    if now > spookyMonth:
        spookyMonth = datetime(datetime.now().year + 1, 9, 1)    
        

    time_left = spookyMonth - now
    days_left = time_left.days
    print(((365-days_left)*100)/365)
    create_loading_bar(math.floor(((365-days_left)*100)/365))

    return (False, days_left)

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
async def wait():
    print('a')

async def ruun():
    await create_loading_bar(20)
    await wait()

asyncio.run(ruun())

# print(is_it_spookymonth()[0])






