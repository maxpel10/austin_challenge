import json


class JsonWriter:
    def write(self, filename, objects):
        json_file = open(filename, "w")
        json_string = json.dumps(
            list(map(lambda x: x.toJson(), objects)), indent=2)
        json_file.write(json_string)
        json_file.close()
