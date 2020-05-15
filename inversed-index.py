import os
from bs4 import BeautifulSoup
import re
from nltk.stem import PorterStemmer
import json
import time
import pandas

# Kaeley:
# dev_directory = '/Users/kaeleylenard/Documents/CS121-Spring2020/SearchEngine/DEV'
# Areeta:
dev_directory = '/Users/AreetaW/Desktop/cs/cs-121/assignment3/DEV'
# Cristian:
# dev_directory = 'C:\Test\DEV'
# dev_directory = 'C:\Test\custom'


inverse_index = dict()
docid_counter = 0
index_count = 0
word_count = 0
total_docs = 0


def tokenizes(data):
    # tokenizes words given from website
    data = data.split()
    tokens = list()
    ps = PorterStemmer()

    for word in data:
        tokenized = re.sub('[^A-Za-z0-9]+', ' ', str(word))
        tokenized = tokenized.strip()
        if len(tokenized) >= 2:
            if len(ps.stem(tokenized)) >= 2:
                tokens.append(ps.stem(tokenized))
    return tokens


def write_to_file():
    global index_count
    global inverse_index
    global word_count
    global docid_counter
    global total_docs

    word_count += len(inverse_index)
    total_docs += docid_counter
    index_count += 1
    docid_counter = 0

    # Kaeley:
    #deliverable_text = open(f'/Users/kaeleylenard/Desktop/info{index_count}.txt', 'w')
    # Areeta:
    deliverable_text = open(f'/Users/AreetaW/Desktop/info{index_count}.txt', 'w')
    # Cristian:
    # deliverable_text = open(f'C:\Test\info{index_count}.txt', 'w')

    with deliverable_text as json_file:
        inverse_index = {k: list(v) for k, v in sorted(inverse_index.items())}  # Sorts dict by key
        json.dump(inverse_index, json_file)  # Pretty printing
    deliverable_text.close()
    inverse_index.clear()


def add_to_index(document_words, docid_counter):
    # splits indexes into different files
    if docid_counter % 11000 == 0:
        write_to_file()

    # adds each word to index with tf score
    for word in document_words:

        # calculates tf score for each word
        # freq_of_token = float(document_words.count(word))
        # amount_of_words = float(len(document_words))
        # tf_score = freq_of_token/amount_of_words
        # tf_score = round(tf_score, 5)

        tf_score = 0.0

        # decides whether word is unique or not
        if word not in inverse_index:
            first_appearance = (docid_counter, tf_score)
            inverse_index[word] = set()
            inverse_index[word].add(first_appearance)
        else:
            inverse_index[word].add((docid_counter, tf_score))


def partial_indexing():
    global index_count
    global inverse_index
    global word_count
    global docid_counter
    global total_docs

    # increments global information of index
    word_count += len(inverse_index)
    index_count += 1
    total_docs += docid_counter

    # Kaeley:
    # deliverable_text = open(f'/Users/kaeleylenard/Desktop/info{index_count}.txt', 'w')
    # Areeta:
    deliverable_text = open(f'/Users/AreetaW/Desktop/info{index_count}.txt', 'w')
    # Cristian
    # deliverable_text = open(f'C:\Test\info{index_count}.txt', 'w')

    with deliverable_text as json_file:
        inverse_index = {k: list(v) for k, v in sorted(inverse_index.items())}
        json.dump(inverse_index, json_file)
    deliverable_text.close()

    # Kaeley:
    # file_list = [f'/Users/kaeleylenard/Desktop/info{x+1}.txt' for x in range(index_count)]
    # Areeta:
    file_list = [f'/Users/AreetaW/Desktop/info{x+1}.txt' for x in range(index_count)]
    # Cristian:
    # file_list = [f'C:\Test\info{x+1}.txt' for x in range(index_count)]

    # pandas will merge all json files alphabetically
    bases = []  
    for file in file_list:
        temp = pandas.read_json(file, orient='index')
        bases.append(temp)

    # holds all json files as one big pandas dataframe    
    result = pandas.concat(bases)  

    # exports into excel
    # Kaeley:
    # result.to_csv()
    # Areeta:
    result.to_csv("/Users/AreetaW/Desktop/finalindex.csv")
    # Cristian:
    # result.to_csv("C:\Test\/finalindex.csv")


if __name__ == "__main__":
    # tracks time taken to complete indexing
    start_time = time.time()

    # loops through all files in DEV
    for subdir, dirs, files in os.walk(dev_directory):
        for file in files:
            json_file = os.path.join(subdir, file)
            docid_counter += 1
            alphanumeric_sequences = []
            print(f"current file {docid_counter} {index_count} {word_count} :", json_file)

            # tokenizes all important text from each file and adds to index
            try:
                soup = BeautifulSoup(open(json_file), 'html.parser')
                for text in soup.findAll(["title", "p", "b", re.compile('^h[1-6]$')]):

                    # gets only text from each tag element
                    data = text.get_text().strip()
                    alphanumeric_sequences += tokenizes(data)
                add_to_index(alphanumeric_sequences, docid_counter)
            except Exception as e:
                print("error at:", e)
    partial_indexing()

    # Statistics
    print("\nREPORT")
    print("Number of Indexed Documents:", total_docs)
    print("Number of Unique Words:", word_count)
    print("--- %s seconds ---" % (time.time() - start_time))