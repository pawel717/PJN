from lemmatizer import Lemmatizer
from tokenizer import tokenize


class SearchEngine:
    def __init__(self):
        self.indexes_path = "./indexes/"
        file = open("./stoplist.txt", "r", encoding="utf-8")
        self.stoplist = file.readlines()
        self.stoplist = [stopword.strip() for stopword in self.stoplist]
        self.lemmatizer = None

    def deleteStopWords(self, expression, count):
        expression_tokens = tokenize(expression)
        stop_list = self.stoplist[:count]
        filtered_tokens = [token for token in expression_tokens if token not in stop_list]
        filtered_expression = ' '.join(filtered_tokens)
        return filtered_expression


    def search_lemmatized(self, search_expression, result_count):
        self.indexes_path = "./indexes_lemmatized/"
        lemmatized_expression = self.lemmatizer.lemmatize(search_expression)
        return self.search(lemmatized_expression, result_count)

    def search_unlemmatized(self, search_expression, result_count):
        self.indexes_path = "./indexes/"
        return self.search(search_expression, result_count)

    def search(self, search_expression, result_count):
        search_tokens = tokenize(search_expression)
        founded_urls = {}
        for search_token in search_tokens:
            file = open(self.indexes_path + search_token + ".txt", "r", encoding="utf-8")
            tf_idf_url = file.readlines()
            for line in tf_idf_url:
                line = line.replace("\n","")
                splited_line = line.split('|')
                try:
                    founded_urls[splited_line[0]] += [float(splited_line[1])]
                except KeyError:
                    founded_urls[splited_line[0]] = [float(splited_line[1])]

        search_tokens_len = search_tokens.__len__()
        results = {}
        for url, tf_idf_list in founded_urls.items():
            if (tf_idf_list.__len__() < search_tokens_len):
                continue

            else:
                results[url] = sum(founded_urls[url])

        results = sorted(results.items(), key=lambda item: (item[1], item[0]), reverse=True)
        if(results.__len__() > result_count):
            results = results[:result_count]

        return results

# def find_token_occurences(search_token, token_urls_tf_idf):
#     try:
#         tf_idf = token_urls_tf_idf[search_token]
#     except KeyError:
#         tf_idf = []
#
#     return tf_idf
#
# def load_indexes(catalog):
#     token_urls_tf_idf = {}
#     for filename in os.listdir(catalog):
#         if (filename == "files_indexes.txt"):
#             continue
#         file_index = open("{}{}".format(catalog, filename), "r", encoding="utf-8")
#         lines = file_index.read().split('\n')
#         lines = lines[0:-1]
#         for line in lines:
#             line_splitted = line.split("|")
#             try:
#                 token_urls_tf_idf[line_splitted[0]] += [{'file_index': line_splitted[2], 'tf_idf': line_splitted[1]}]
#             except KeyError:
#                 token_urls_tf_idf[line_splitted[0]] = [{'file_index': line_splitted[2], 'tf_idf': line_splitted[1]}]
#
#     return token_urls_tf_idf