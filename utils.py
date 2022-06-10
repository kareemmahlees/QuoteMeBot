import random
import os
from PIL import Image, ImageDraw, ImageFont
from telethon.sync import TelegramClient
import constants


def gen_img(quote):
    img = Image.open("./temp.jpg")
    fnt = ImageFont.truetype(
        random.choice([f"fonts/{fnt_name}" for fnt_name in os.listdir("fonts")]), 40
    )
    d = ImageDraw.Draw(img)
    # w, h = d.textsize(quote, font=fnt)
    # h += int(h * 0.21)
    # d.text(
    #     ((img.width - w) / 2, (img.height - h) / 2),
    #     text=quote,
    #     fill="white",
    #     font=fnt,
    # )
    # find the average size of the letter
    sum = 0
    for letter in quote:
        sum += d.textsize(letter, font=fnt)[0]

    average_length_of_letter = sum / len(quote)

    # find the number of letters to be put on each line
    number_of_letters_for_each_line = (img.width / 1.618) / average_length_of_letter
    incrementer = 0
    fresh_sentence = ""

    # add some line breaks
    for letter in quote:
        if letter == "-":
            fresh_sentence += "\n\n" + letter
        elif incrementer < number_of_letters_for_each_line:
            fresh_sentence += letter
        else:
            if letter == " ":
                fresh_sentence += "\n"
                incrementer = 0
            else:
                fresh_sentence += letter
        incrementer += 1

    # render the text in the center of the box
    dim = d.textsize(fresh_sentence, font=fnt)
    x2 = dim[0]
    y2 = dim[1]

    qx = img.width / 2 - x2 / 2
    qy = img.height / 2 - y2 / 2

    d.text((qx, qy), fresh_sentence, align="center", font=fnt, fill=(255, 255, 255))

    img.save("./temp.jpg")


def send_quote(quote_img):
    client = TelegramClient(
        "mysess33", api_hash=constants.API_HASH, api_id=constants.API_ID
    )
    client.start()
    client.send_file("https://t.me/Quotee_Me", quote_img)
