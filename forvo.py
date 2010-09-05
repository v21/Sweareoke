import urllib
import json
import re
import os.path
from subprocess import call

class ForvoResponse:
    def __init__(self, jsonResp):
        self.num_recordings = jsonResp[u"attributes"][u"total"]

        self.recordings = [{"ogg":resp[u"pathogg"], "id": resp[u"id"]} for resp in jsonResp[u"items"]]
        self.json = jsonResp


class ForvoLibrary:
    def __init__(self):
        self.api_key = "32afdf084bda652565de09c55de855e3"
        self.cache = {} # {"word":ForvoResponse(), ...}
        self.recording_loc = "sounds"

    def queryWord(self, word):

        if self.cache.has_key(word): #links will stop working after 2 hours. this aint a problem now.
            return self.cache[word]

        url_start = "http://apifree.forvo.com/action/word-pronunciations/format/json/word/"
        url_end = "/language/en/order/rate-desc/key/"

        url = url_start + word + url_end + self.api_key
        f = urllib.urlopen(url)

        resp = ForvoResponse(json.load(f))
        self.cache[word] = resp
        return resp

    def fetchRecording(self, resp, which):
        if (resp.num_recordings == 0) :
            raise NoRecordingsError
        url = resp.recordings[which]["ogg"]
        filename = self.recording_loc + "/" + resp.recordings[which]["id"] + ".ogg"
        if os.path.exists(filename):
            return filename
        else:
            urllib.urlretrieve(url, filename)
            return filename

    def queryAndFetchMultiple(self, words):
        words = list(set(words)) #uniquify
        default_which = 0
        filenames = {}
        for word in words:
            resp = self.queryWord(word)
            try:
                filename = self.fetchRecording(resp,default_which)
                filenames[word] = filename
            except NoRecordingsError:
                print "Couldn't find: " + word

        return filenames

    def postprocessAudio(self, filename):
        new_dir = "sounds/processed/"
        base_filename = filename.split("/")[-1]
        retcode = call(["sox", filename, new_dir + base_filename, "silence", "1", "0.1", "3%"])
        return new_dir + filename

class NoRecordingsError(Exception):
    pass
