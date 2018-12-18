from search import SearchEngine

class SearchController:
    def __init__(self):
        self.searchEngine = SearchEngine()

    def search(self, params):
        print(params)
        search_input = params.get('search_input')
        stop_words = params.get('stop_words')
        lemmatize = bool(params.get('lemmatize'))

        if(stop_words != None):
            search_input = self.searchEngine.deleteStopWords(search_input, int(stop_words))

        if(lemmatize == True):
            result = self.searchEngine.search_lemmatized(search_input, 20)
        else:
            result = self.searchEngine.search_unlemmatized(search_input, 20)

        return result