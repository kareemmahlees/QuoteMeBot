import requests


class Quote(requests.Session):
    """
    Class for getting quote of the day
    """

    def __init__(self, quote=None, author=None) -> None:
        self.quote = quote
        self.author = author
        super().__init__()

    def get_quote(self):
        res = self.get("https://quotes.rest/qod")
        self.quote = res.json()["contents"]["quotes"][0]["quote"]
        self.author = res.json()["contents"]["quotes"][0]["author"]
