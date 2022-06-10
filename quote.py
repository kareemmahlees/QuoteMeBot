from dataclasses import dataclass
import requests
import json
from PIL import Image


@dataclass
class Quote(requests.Session):
    def __init__(self, quote=None, author=None, image=None) -> None:
        self.quote = quote
        self.author = author
        self.image = image
        super().__init__()

    def get_quote(self):
        res = self.get("https://quotes.rest/qod")
        # print(res.json())
        self.quote = res.json()["contents"]["quotes"][0]["quote"]
        self.author = res.json()["contents"]["quotes"][0]["author"]
        self.img = res.json()["contents"]["quotes"][0]["background"]
        with open("./temp.jpg", "wb") as f:
            f.write(self.get(self.img).content)


inst = Quote()
inst.get_quote()
