from tokenizer import tokenize

class Lemmatizer:
    def __init__(self):
        self.dictionaryMap = {}


    def makeDictionaryMap(self):
        self.dictionaryMap = {}
        with open("./lematy-02-UTF-8.txt", "r", encoding="utf-8") as dictionaryFile:
            for line in dictionaryFile:
                lineSplitted = line.split("|")
                self.dictionaryMap[lineSplitted[0]] = lineSplitted[1]

        return self.dictionaryMap


    def lemmatize(self, text):
        # split text into word tokens
        tokens = tokenize(text)

        # replace all tokens occurrences in text by lemma
        for i in range(0,len(tokens)):
            try:
                lemma = self.dictionaryMap[tokens[i]]
            except KeyError:
                continue

            tokens[i] = lemma

        lemmatizedText = ' '.join(tokens)
        return lemmatizedText