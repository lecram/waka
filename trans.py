import os
import os.path

class Trans:

    def __init__(self, def_lang="en"):
        self.def_lang = def_lang

    def scan_langs(self, path="lang"):
        fnames = [fname for fname in os.listdir(path) if fname.endswith(".txt")]
        langs = {}
        for fname in fnames:
            code = os.path.splitext(fname)[0]
            with open(os.path.join(path, fname), "r") as f:
                lang = {}
                key = f.readline().strip()
                while key:
                    val = f.readline().strip()
                    sep = f.readline()
                    lang[key] = val
                    key = f.readline().strip()
            langs[code] = lang
        self.langs = langs

    def get_underline(self, code):
        if code == self.def_lang:
            return lambda key: key
        else:
            return lambda key: self.langs[code].get(key, key)
