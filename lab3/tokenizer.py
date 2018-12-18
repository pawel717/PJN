import re

def tokenize(text):
    # lowercase
    text = text.lower()

    # split text into words, deletes all characters that are not letters
    tokens = re.findall(r"[a-ząćęłńóśźż]+", text)

    return tokens