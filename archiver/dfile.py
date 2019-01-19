class DarkFile:
    text = ""
    title = ""

    def __init__(self, text, title):
        self.text = text
        self.title = title

    @property
    def json_object(self):
        json_ob = dict()
        json_ob["txt"] = self.text
        json_ob["tl"] = self.title

        return json_ob

    @property
    def name(self):
        return self.title[:self.title.rindex(".")]
