class DarkFolder:
    def __init__(self, files, folders, title):
        self.files = files
        self.folders = folders
        self.title = title

    @property
    def json_object(self):
        json_ob = dict()
        json_ob["tl"] = self.title
        json_ob["fis"] = []
        for file in self.files:
            json_ob["fis"].append(file.json_object)
        json_ob["fos"] = []
        for folder in self.folders:
            json_ob["fos"].append(folder.json_object)

        return json_ob
