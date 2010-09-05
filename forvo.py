import urllib
import json




class ForvoResponse:
    def __init__(self, jsonResp):
        self.num_recordings = jsonResp[u"attributes"][u"total"]

        self.recordings = [resp[u"pathogg"] for resp in jsonResp[u"items"]]

class ForvoLibrary:
    def __init__(self):
        self.api_key = "32afdf084bda652565de09c55de855e3"
        self.cache = {} # {"word":ForvoResponse(), ...}


    def queryWord(self, word):

        if self.cache.has_key(word):
            return self.cache[word]

        url_start = "http://apifree.forvo.com/action/word-pronunciations/format/json/word/"
        url_end = "/language/en/key/"

        url = url_start + word + url_end + self.api_key
        f = urllib.urlopen(url)

        resp = ForvoResponse(json.load(f))
        self.cache[word] = resp
        return resp

