# -*- coding: utf-8 -*-
import re

def tokenize(text):
    # lowercase
    text = text.lower()

    # split text into words, deletes all characters that are not letters
    tokens = re.findall(r"[a-ząćęłńóśźż]+", text)

    return tokens

def map_tokens(tokens):
    processed_words_count = 0
    founded_words_count = 0
    tokens_map = {}


    if tokens is not None:
        data_file = open("./data.txt", "w+", encoding="utf-8")

        for token in tokens:
            if token in tokens_map:
                tokens_map[token] = tokens_map[token] + 1
            else:
                founded_words_count = founded_words_count + 1
                tokens_map[token] = 1

            processed_words_count = processed_words_count + 1;

            if(processed_words_count%1000 == 0):
                data_file.write("{0:<15} {1:<15}\n".format(str(founded_words_count), str(processed_words_count)))

        data_file.write("{0:<15} {1:<15}\n".format(str(founded_words_count), str(processed_words_count)))
        data_file.close()

        return tokens_map
    else:

        return None


text_file = open("./text.txt", "r+", encoding="utf-8")

# read from file
text = text_file.read()

tokens = tokenize(text)

tokens_map = map_tokens(tokens)

tokens_freq_file = open("./tokens_freq.txt", "w+", encoding="utf-8")

for token in tokens_map:
    tokens_freq_file.write("{0:<40} {1:<15}\n".format(token, str(tokens_map[token])))

tokens_freq_file.close()

count_file = open("./count.txt", "w+", encoding="utf-8")
