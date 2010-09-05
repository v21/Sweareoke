import urllib
import json
import re
import os.path
from subprocess import call
import pickle

class ForvoResponse:
    def __init__(self, jsonResp):
        self.num_recordings = jsonResp[u"attributes"][u"total"]

        self.recordings = [{"ogg":resp[u"pathogg"], "id": resp[u"id"]} for resp in jsonResp[u"items"]]
        self.json = jsonResp

class ForvoLibrary:
    def __init__(self):
        self.api_key = "32afdf084bda652565de09c55de855e3"
        self.cachePickled = "forvocache.pickle"
        try:
            with open(self.cachePickled) as f:
                self.cache = pickle.load(f)
                #print "loaded: " + self.cache
        except:
            self.cache = {}
            print "failed to load cache"
        self.recording_loc = "sounds/"
        self.recording_postproc_loc = "sounds/processed/"

    def queryWord(self, word):
        word = word.lower()
        m = re.match(r"\w+", word)
        if m:
            word = m.group(0)
        else:
            raise NoRecordingsError

        if self.cache.has_key(word): #links will stop working after 2 hours. this aint a problem now.
            #print "returning from cache"
            return self.cache[word]

        url_start = "http://apifree.forvo.com/action/word-pronunciations/format/json/word/"
        url_end = "/language/en/order/rate-desc/key/"

        url = url_start + word + url_end + self.api_key
        print "Opening url " + url
        f = urllib.urlopen(url)

        resp = ForvoResponse(json.load(f))
        resp.word = word
        self.cache[word] = resp
        with open(self.cachePickled, "wb") as f:
            pickle.dump(self.cache, f)
        #print "dumped to file"
        return resp

    def fetchRecording(self, resp, which, word):
        if (resp.num_recordings == 0) :
            raise NoRecordingsError
        url = resp.recordings[which]["ogg"]
        filename = self.recording_loc + "/" + word + "_" + resp.recordings[which]["id"] + ".ogg"
        if os.path.exists(filename):
            return filename
        else:
            urllib.urlretrieve(url, filename)
            return filename

    def queryAndFetchMultiple(self, words, postProcess=False):
        words = list(set(words)) #uniquify
        default_which = 0
        filenames = {}
        for word in words:
            try:
                resp = self.queryWord(word)
            except NoRecordingsError:
                continue
            try:
                filename = self.fetchRecording(resp,default_which, resp.word)
                if postProcess:
                    filename = self.postprocessAudio(filename)
                filenames[word] = filename
            except NoRecordingsError:
                print "Couldn't find: " + word

        print filenames
        return filenames

    def postprocessAudio(self, filename, force_reprocess=False):
        base_filename = filename.split("/")[-1]
        new_filename = self.recording_postproc_loc + base_filename
        if os.path.exists(new_filename) and not force_reprocess:
            return new_filename
        else:
            retcode = call(["sox", filename, new_filename, "silence", "1", "0.1", "3%"])
            return new_filename

class NoRecordingsError(Exception):
    pass
