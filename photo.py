import html
import json

from markupsafe import Markup


class Photo:
    def __init__(self, e):
        super().__init__()
        self.e = e
        try:
            self.description = json.loads(html.unescape(e['description']['_content']))
            print(self.description)
        except:
            self.description = None

    @property
    def original_url(self):
        url = "https://farm{farm}.staticflickr.com/{server}/{id}_{secret}_o.jpg"
        return url.format(farm=self.e['farm'],
                   server=self.e['server'],
                   id=self.e['id'],
                   secret=self.e['originalsecret'])

    @property
    def overlay(self):
        if self.description:
            return self.description.get('overlay')

    @property
    def content(self):
        if self.description:
            return Markup(self.description.get('content'))