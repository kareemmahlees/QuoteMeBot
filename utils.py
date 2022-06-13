import random
import os
import requests
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
from telethon.sync import TelegramClient
import constants


def gen_img(quote: str) -> None:
    """
    a function to write the quote on the given image , resize the font according to the size of image
    and break the quote into lines
    :param ```quote```:
        the text quote to be written on the image
    :return:
        None
    """
    img_author = get_image()["author"]
    img = Image.open("./temp.jpg")
    img = img.filter(ImageFilter.BoxBlur(7))

    # to reduce brightness by 50%
    enhancer = ImageEnhance.Brightness(img)
    img = enhancer.enhance(0.5)

    fontsize = 1  # starting font size
    d = ImageDraw.Draw(img)

    # portion of image width you want text width to be
    blank = Image.new("RGB", (img.width - 500, img.height - 500))

    fnt = ImageFont.truetype(
        random.choice([f"fonts/{fnt_name}" for fnt_name in os.listdir("fonts")]),
        fontsize,
    )
    # ------ find the suitable font size for the image----------
    while (fnt.getsize(quote)[0] < blank.size[0]) and (
        fnt.getsize(quote)[1] < blank.size[1]
    ):
        # iterate until the text size is just larger than the criteria
        fontsize += 1
        fnt = ImageFont.truetype(
            random.choice([f"fonts/{fnt_name}" for fnt_name in os.listdir("fonts")]),
            fontsize + 30,
        )

    # -------- break the quote into lines ---------
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
                fresh_sentence += " "
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
    credit_txt = f"Unsplash image by {img_author}"
    w, h = d.textsize(
        credit_txt, font=ImageFont.truetype("fonts/Odin Rounded - Regular.ttf", 60)
    )
    d.text(
        (img.width - w, img.height - h),
        text=credit_txt,
        font=ImageFont.truetype("fonts/Odin Rounded - Regular.ttf", 60),
    )

    img.save("./temp.jpg")


def send_quote(quote_img: Image) -> None:
    """
    function to send the final image to telegram channel
    :param ```quote_img```:
        image to be sent
    :return:
        None
    """
    client = TelegramClient(
        "mysess33", api_hash=constants.API_HASH, api_id=constants.API_ID
    )
    client.start()
    client.send_file("https://t.me/Quotee_Me", quote_img)


def get_image() -> dict:
    """
    function to get a random image for unsplash
    :return:
        dict containing width,height and author of the image
    """
    res = requests.get(constants.RANDOM_PHOTO_SCHEME(constants.UNSPLASH_ACESS_KEY))

    with open("./temp.jpg", "wb") as f:
        f.write(requests.get(res.json()["urls"]["full"]).content)
    return {
        "width": res.json()["width"],
        "height": res.json()["height"],
        "author": res.json()["user"]["name"],
    }
