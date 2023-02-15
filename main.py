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


class InstantUpload:

    def __init__(self):
        self.bot = Bot()

    def upload(self):

        if self.canPost():  # Returns the file location, removes config, finds out if right time to post

            photo_location = self.getPhoto()
            file_name = photo_location.replace("F:/Progress - Python Projects/InstagramBot/Photos/Original Post/", "")
            caption = self.writeCaption()

            print(f"This file: {file_name} will be uploaded")
            shutil.copyfile(photo_location,
                            f"F:/Progress - Python Projects/InstagramBot/Photos/Already Posted/{file_name}")

            print('Connection initiated, Uploading started...')

            self.bot.login(username=backend.info.get('username'), password=backend.info.get('password'))
            print('Posting of the picture initiated...')
            self.bot.upload_photo(photo_location, caption=caption)
            
        else:  # Exists, as not the right time to post
            exit()
            
    def getPhoto(self):

        remaining_photos = os.listdir(f"F:/Progress - Python Projects/InstagramBot/Photos/Original Post")

        # Selecting a picture
        file_upload = random.choice(remaining_photos)
        base_location_picture = f"F:/Progress - Python Projects/InstagramBot/Photos/Original Post/{file_upload}"

        base_location_picture = self.fixDimension(base_location_picture)

        return base_location_picture

    def writeCaption(self):

        with open('F:/Progress - Python Projects/InstagramBot/Script/Evening Quotes.txt', 'r', encoding="utf8") as q:
            caption = ''

            for _ in range(2):
                caption += q.readline()

        caption = f'''
        {caption}
        Good {self.canPost(get_greeting=True)} have a great rest of your day!

        ---Tags---
        {random.choice(backend.tags)}

        (Please feel free to DM for picture removal or picture credit)

        - with love from @livelikezen
        posted by Python

        Day - {date.today()}
        '''.strip()

        # Deleting the used quote from the text file --> Evening Quotes
        with open("F:/Progress - Python Projects/InstagramBot/Script/Evening Quotes.txt", "r", encoding="utf8") as q:
            lines = q.read().splitlines(True)
        with open("Evening Quotes.txt", "w", encoding="utf8") as q_new:
            q_new.writelines(lines[2:])

        return caption

    @staticmethod
    def canPost(get_greeting=False):

        current_time = int(time.strftime('%H:%M:%S')[:2])
    
        # 'morning time' i.e 8:00 to 12:00
        if 8 < current_time < 12:
            greeting = 'Morning'

        # 'After Noon Time' i.e 12:00 to 16:00
        elif 12 <= current_time < 15:
            greeting = 'After Noon'

        # 'evening time' i.e 18:00 to 22:00
        elif 18 < current_time < 23:
            greeting = 'Evening'

        else:
            print('Not the right time to post, try again after some time')
            print(time.strftime('%H:%M:%S'))
            return False

        if get_greeting:
            return greeting

        return True

    @staticmethod  # This finds aspect ratio and resize the picture
    def fixDimension(picture_location):

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
            image.close()
            new_image.save(picture_location)

            return picture_location


def deleteConfig():
    
    global dir_path
    try:
        dir_path = Path('F:/Progress - Python Projects/InstagramBot/Script/', 'config')
        if dir_path.exists() and dir_path.is_dir():
            print("Removing Config")
            shutil.rmtree(dir_path)

    except OSError as e:
        print("Error: %s : %s" % (dir_path, e.strerror))


if __name__ == '__main__':

    try:
        deleteConfig()
        bot = InstantUpload()
        bot.upload()

    except FileNotFoundError:
        print('File not found, try again')

    except KeyError:
        print('Delete config folder first')
