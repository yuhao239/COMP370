from nltk.corpus import stopwords
from pathlib import Path
import pandas as pd
import argparse
import string
import json
import os

CATEGORIES = ['dating', 'achievements', 'unrelated', 'social impact', 'filmography', 'tour', 'gossip', 'discography']
SENTIMENTS = ['-1', '0', '1']
stop_words = stopwords.words('english')
punctuation = string.punctuation
word_count = dict()
all_words = []
df = None

def isKeyIn(key, dict):
    return key in dict.keys()


def load_df(filename):
    global df

    if df == None:
        fpath = Path(filename)
        df = pd.read_csv(fpath, encoding="ISO-8859-1")
        df = df.reset_index()
        df = df[df['topic open coding 3'].notna()]


def remove_punctuation(content):
    global punctuation

    no_punctuation = ""
    content = content.strip().lower()
    for c in content:
        if c not in punctuation:
            no_punctuation += c
        else:
            no_punctuation += " "
    return no_punctuation


def remove_stop_words(content):
    global stop_words

    content = content.split(' ')
    no_stopwords = []
    for word in content:
        if word.isalpha() and word.replace(" ", "") != "" and word not in stop_words and len(word) > 1:
            no_stopwords.append(word)
    return no_stopwords


def clean(content):
    content = remove_punctuation(content)
    return remove_stop_words(content)


def need_to_be_removed(category, word, frequency_threshold):
    global word_count

    count = 0

    c_dict = word_count[category]
    for sentiment in c_dict.keys():
        if isKeyIn(word, word_count[category][sentiment]):
            count += word_count[category][sentiment][word]

    return (count < frequency_threshold)


def mark_to_remove(category, word):
    global word_count, all_words

    c_dict = word_count[category]
    for sentiment in c_dict.keys():
        if isKeyIn(word, word_count[category][sentiment]):
            word_count[category][sentiment][word] = -1

    if word in all_words:
        all_words.remove(word)


def remove_words_appearing_less_than(frequency_threshold):
    global CATEGORIES, SENTIMENTS, word_count, all_words

    print("Removing words appearing less than "+str(frequency_threshold)+"x in its category across all sentiments (<= 3)")
    
    for category in CATEGORIES:
        if isKeyIn(category, word_count):

            for sentiment in SENTIMENTS:
                if isKeyIn(sentiment, word_count[category]):

                    sentiment_dict = word_count[category][sentiment]

                    for word in sentiment_dict.keys():
                        if need_to_be_removed(category, word, frequency_threshold):
                            mark_to_remove(category, word)

                    tmp = {x:y for x,y in sentiment_dict.items() if y!=-1}
                    
                    if len(tmp) > 0:
                        sorted_by_descending_count = sorted(tmp.items(), key=lambda kv:(kv[1]), reverse=True)
                        word_count[category][sentiment] = dict(sorted_by_descending_count)
    
    with open('../results/tokenized_words.txt', 'a', encoding='utf-8') as f:
        for word in all_words:
            f.write(word+'\n')


def load_word_count_dict(filename, frequency_threshold):
    global word_count, df, stop_words, all_words, CATEGORIES, SENTIMENTS

    all_words = []

    if df == None:
        load_df(filename)
    
    num_articles = len(df)

    for i, row in df.iloc[:num_articles].iterrows():
        category = str(row['topic open coding 3']).strip().lower()
        if category in CATEGORIES:
            sentiment = str(row['sentiment open coding'])
            if sentiment in SENTIMENTS:
                content = str(row['title'])+str(row['description'])+str(row['content'])
                content = clean(content)

                if len(content) > 0:

                    for word in content:
                        if not isKeyIn(category, word_count):
                            word_count[category] = dict()

                        if not isKeyIn(sentiment, word_count[category]):
                            word_count[category][sentiment] = dict()

                        if not isKeyIn(word, word_count[category][sentiment]):
                            word_count[category][sentiment][word] = 1
                        else:
                            word_count[category][sentiment][word] += 1
                            
                        if word not in all_words:
                            all_words.append(word)

    remove_words_appearing_less_than(frequency_threshold)


def load_dict_to_file(filename):
    global word_count

    fpath = Path(filename)
    json_list = json.dumps(word_count, indent=4)

    path = os.path.dirname(fpath)
    if not os.path.isdir(path):
        os.makedirs(path)

    with open(fpath, "w") as f:
        f.write(json_list)

    print("See "+filename+" for word count by sentiment by category")


def main():
    parser = argparse.ArgumentParser()
    
    parser.add_argument('-o', metavar='Output JSON file', type=str, required=True)
    parser.add_argument('-d', metavar='Input dialog file', type=str, required=True)
    parser.add_argument('-f', metavar='Frequency threshold', type=int, required=True)
    
    args = parser.parse_args()

    output_filename = args.o
    input_filename = args.d
    frequency_threshold = args.f

    load_word_count_dict(input_filename, frequency_threshold)
    load_dict_to_file(output_filename)


if __name__ == "__main__":
    main()
