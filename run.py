import schedule
from quote import Quote
import utils
from keep_alive import keep_alive


def main():
    inst = Quote()
    inst.get_quote()
    utils.gen_img(
        inst.quote + "-" + inst.author if inst.author is not None else inst.quote
    )
    utils.send_quote("./temp.jpg")


if __name__ == "__main__":
    keep_alive()
    schedule.every().day.at("7:00").do(main)
