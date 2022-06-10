from PIL import Image, ImageDraw, ImageFont


def gen_img(quote):
    img = Image.open("./temp.jpg")
    fnt = ImageFont.truetype("./Arial 2.ttf", 50)
    d = ImageDraw.Draw(img)
    w, h = d.textsize(quote, font=fnt)
    h += int(h * 0.21)
    d.text(
        ((img.width - w) / 2, (img.height - h) / 2),
        text=quote,
        fill="white",
        font=fnt,
    )
    img.save("./saved_img.jpg")
