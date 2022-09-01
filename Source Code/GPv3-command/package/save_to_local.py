import json


class SaveToLocal:
    def save_to_json(self, data, file_name, path="../data/preprocessing/"):
        content = json.dumps(data)
        with open(path + file_name, "w") as file:
            file.write(content)

    def save_to_files(self, data, file_name, path="../data/preprocessing/"):
        with open(path + file_name, "w") as file:
            file.write(data)
