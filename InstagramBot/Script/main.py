import random
import time
import backend
import shutil
import os
import cv2
from instabot import Bot
from datetime import date
from PIL import Image
from pathlib import Path


# Config is created everytime the script runs, if not removed causes KeyError: "DS user"
def delete_config():
    dir_path = Path('F:/Progress - Python Projects/InstagramBot/Script/', 'config')

    if dir_path.exists() and dir_path.is_dir():
        shutil.rmtree(dir_path)
        print('Config Folder is removed')
    else:
        print('No config folder...')
        pass


# Instagram only allow to post pictures of certain aspect ratio, this finds aspect ratio and resize the picture
def fix_dimension(picture_location):
    img = cv2.imread(picture_location)
    height, width, channels = img.shape
    aspect_ratio = float(width / height)

    print(f"Width: {width}, Height: {height}")
    print(f"Aspect ratio: {aspect_ratio}")

    if 1 <= aspect_ratio <= 1.777777777777778:
        return picture_location
    else:
        print('Fixing the dimensions')

        change = max(height, width)
        image = Image.open(picture_location)
        new_image = image.resize((change, change))
        new_image.save(picture_location)

        return picture_location


try:

    # Deletes the config folder if it exists
    delete_config()

    current_time = int(time.strftime('%H:%M:%S')[:2])
    greeting = ''

    # 'morning time' i.e 8:00 to 12:00
    if 8 < current_time < 12:
        greeting = 'Morning'

    # 'After Noon Time' i.e 12:00 to 16:00
    elif 12 < current_time < 16:
        greeting = 'After Noon'

    # 'evening time' i.e 18:00 to 22:00
    elif 18 < current_time < 22:
        greeting = 'Evening'

    else:
        print('Not the right time to post, try again after some time')
        print(time.strftime('%H:%M:%S'))
        exit()

    remaining_photos = os.listdir(f"F:/Progress - Python Projects/InstagramBot/Photos/Original Post")

    # Selecting a picture
    file_upload = random.choice(remaining_photos)
    base_location_picture = f"F:/Progress - Python Projects/InstagramBot/Photos/Original Post/{file_upload}"

    base_location_picture = fix_dimension(base_location_picture)

    print(f'Chosen Picture: {file_upload}')

    # Taking the quotes and adding it to the caption
    with open('F:/Progress - Python Projects/InstagramBot/Script/Evening Quotes.txt', 'r', encoding="utf8") as q:
        caption = ''

        for _ in range(2):
            caption += q.readline()

    caption = f'''
    {caption}
    Good {greeting} have a great rest of your day!
    
    ---Tags---
    {random.choice(backend.tags)}
    
    (Please feel free to DM for picture removal or picture credit)
    - with love from @livelikezen
    
    Day - {date.today()}
    '''.strip()

    # Deleting the used quote from the text file --> Evening Quotes
    with open("F:/Progress - Python Projects/InstagramBot/Script/Evening Quotes.txt", "r", encoding="utf8") as q:
        lines = q.read().splitlines(True)
    with open("Evening Quotes.txt", "w", encoding="utf8") as q_new:
        q_new.writelines(lines[2:])

    print('Connection initiated')

    bot = Bot()
    bot.login(username=backend.info.get('username'), password=backend.info.get('password'))
    print('Posting of the picture initiated...')

    bot.upload_photo(base_location_picture,
                     caption=caption)

    shutil.move(base_location_picture,
                f"F:/Progress - Python Projects/InstagramBot/Photos/Already Posted/{file_upload}")

except FileNotFoundError:
    print('File not found, try again')

except KeyError:
    print('Delete config folder first')
    exit()
