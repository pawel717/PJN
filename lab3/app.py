from flask import Flask, render_template, request
from controller import SearchController
import time
from database import Database
from indexer import Indexer
import sys
from lemmatizer import Lemmatizer

app = Flask(__name__)
searchController = SearchController()

@app.route("/")
def main():
    return render_template('index.html')

@app.route("/search")
def search():
    t = time.process_time()
    search_results = searchController.search(request.args)
    elapsed_time = time.process_time() - t
    return render_template('index.html', search_results=search_results, elapsed_time=elapsed_time)

def _usage():
    print("usage: python app.py index")
    print("mode - gatherUrls, scrape")
    print("site - newonce, focus, national-geographic, filmweb")
    sys.exit(-1)

def lemmatizeCorpus(lemmatizer):
    # fetch all not lemmatized articles from database
    articlesCursor = database.fetch_data("SELECT * FROM articles")

    # for all rows in cursor lemmatize text and save to database
    for row in articlesCursor:
        lemmatizedText = lemmatizer.lemmatize(row['text'])
        database.insert_data("INSERT INTO articles_lemma (url, text) VALUES (%s, %s)", (row['url'], lemmatizedText))

def indexCorpus():
    indexer = Indexer(database)
    # index normal articles
    indexer.corpus_cursor = database.fetch_data("SELECT * FROM articles")
    indexer.compute_tf()
    indexer.compute_tf_idf()
    indexer.purge()
    # index lemmatized articles
    indexer.corpus_cursor = database.fetch_data("SELECT * FROM articles_lemma")
    indexer.output_catalog ="./indexes_lemmatized/"
    indexer.compute_tf()
    indexer.compute_tf_idf()
    indexer.purge()

if __name__ == "__main__":
    if (len(sys.argv) > 2):
        _usage()

    lemmatizer = Lemmatizer()
    lemmatizer.makeDictionaryMap()

    if (len(sys.argv) == 2):
        if(sys.argv[1] == 'index'):
            database = Database()
            lemmatizeCorpus(lemmatizer)
            indexCorpus()

    app.run()