from tokenizer import tokenize
import math

class Indexer:
    def __init__(self, database):
        self.database = database
        self.corpus_cursor = None
        self.freqency_dictionary_list = []
        self.total_articles_count = 0
        self.term_occurences_dict = {}
        self.idf_dictionary = {}
        self.output_catalog = "./indexes/"
        self.tf_idf_dict = {}

    def compute_tf(self):
        # iterate over articles and calculate term frequencies for each article and for each term
        for row in self.corpus_cursor:
            total_terms_count = 0
            self.total_articles_count += 1
            # dictionary {term : freqency} for single article
            tokens = tokenize(row['text'])

            for token in tokens:
                total_terms_count += 1
                try:
                    self.tf_idf_dict[token][row['url']] += 1
                except KeyError:
                    try:
                        self.tf_idf_dict[token][row['url']] = 1
                    except KeyError:
                        self.tf_idf_dict[token] = {}
                        self.tf_idf_dict[token][row['url']] = 1

        for token, url_tf in self.tf_idf_dict.items():
            for url, tf in url_tf.items():
                self.tf_idf_dict[token][url] = tf/total_terms_count

        print("tf calculated articles: {}".format(self.total_articles_count))
        print(self.tf_idf_dict.__len__())

    def compute_tf_idf(self):
        i=0
        print(self.tf_idf_dict.__len__())

        for token, url_tf in self.tf_idf_dict.items():
            i+=1
            print(i.__str__()+"\n")
            try:
                file = open(self.output_catalog + token + ".txt", "w", encoding="utf-8")
            except FileNotFoundError:
                continue
            # idf = ln( total number of articles / number of articles containing term )
            self.idf_dictionary[token] = math.log(self.total_articles_count / url_tf.__len__())

            for url, tf in url_tf.items():
                tf_idf = tf * self.idf_dictionary[token]
                self.tf_idf_dict[token][url] = tf_idf

            lines = sorted(self.tf_idf_dict[token].items(), reverse=True)
            for line in lines:
                file.write("{}|{}\n".format(line[0], line[1]))

            file.close()

        print("idf calculed rows: {}".format(i))

    def purge(self):
        self.corpus_cursor = None
        self.freqency_dictionary_list = []
        self.total_articles_count = 0
        self.term_occurences_dict = {}
        self.idf_dictionary = {}
        self.tf_idf_dict = {}