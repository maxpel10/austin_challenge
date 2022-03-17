import json

class JsonWriter:
    def write(self, filename, objects):
        jsonFile = open(filename, "w")
        jsonString = json.dumps(list(map(lambda x: x.toJson(), objects)),indent=2)
        jsonFile.write(jsonString)
        jsonFile.close()