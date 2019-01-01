class DarkFolder:
    def __init__(self, files, folders, title):
        self.files = files
        self.folders = folders
        self.title = title

    @property
    def json_object(self):
        json_ob = dict()
        json_ob["title"] = self.title
        json_ob["files"] = []
        for file in self.files:
            json_ob["files"].append(file.json_object)
        json_ob["folders"] = []
        for folder in self.folders:
            json_ob["folders"].append(folder.json_object)

        return json_ob
