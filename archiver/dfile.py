class DarkFile:
    text = ""
    title = ""

    def __init__(self, text, title):
        self.text = text
        self.title = title

    @property
    def json_object(self):
        json_ob = dict()
        json_ob["text"] = self.text
        json_ob["title"] = self.title

        return json_ob
