import os
from pathlib import Path
import json

storageDir=str(Path.home())+os.sep+".nebulagui"
storagePath = storageDir+os.sep+"settings.json"
Path(storageDir).mkdir(parents=True, exist_ok=True)
if not os.path.exists(storagePath):
        f = open(storagePath, "w")
        f.write("{}")
        f.close()

class Storage():

    def add(self, key, value):
        values=self.getValues()
        values[key] = value
        self.storeValues(values)

    def get(self, key):
        values=self.getValues()
        return values[key]

    def getValues(self):
        f = open(storagePath, "r")
        return json.load(f)

    def storeValues(self, values):
        f = open(storagePath, "w")
        f.write(json.dumps(values))
        f.close()

    def exists(self, key):
        for jKey in self.getValues().keys():
            if key == jKey:
                return True 
        return False