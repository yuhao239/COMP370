from pathlib import Path
import argparse
import json
import math
import os

input_data = None
tfidf = dict()

def isKeyIn(key, dict):
    return key in dict.keys()


def load_input_data(filename):
    global input_data

    fpath = Path(filename)

    with open(fpath, 'r') as f:
        input_data = json.load(f)


def load_tf(w, s, c):
    # get term frequency aka word count
    global input_data

    return input_data[c][s][w]


def load_idf(w, c):
    # treat each category as its own dataset
    # ex. each category is a dataset of up to 3 ponies (for the 3 sentiments)
    global input_data

    num = 0
    total = 0

    c_dict = input_data[c]

    for s in c_dict.keys():
        s_dict = input_data[c][s]
        total += 1

        if isKeyIn(w, s_dict):
            num += 1

    #print(str(total)+'/'+str(num))
    return math.log(total/num)


def load_tfidf():
    global tfidf, input_data

    for c in input_data.keys():
        tfidf[c] = dict()
        c_dict = input_data[c]

        for s in c_dict.keys():
            tfidf[c][s] = dict()
            s_dict = input_data[c][s]

            for w in s_dict.keys():
                tfidf[c][s][w] = load_tf(w, s, c)*load_idf(w, c)

            sentiment_tfidf = tfidf[c][s]
            sorted_by_descending_count = sorted(sentiment_tfidf.items(), key=lambda kv:(kv[1]), reverse=True)
            tfidf[c][s] = dict(sorted_by_descending_count)


def store_tfidf_to_file(n):
    global tfidf
    
    tmp = dict()
    for c in tfidf.keys():
        tmp[c] = dict()

        for s in tfidf[c].keys():
            tmp[c][s] = dict()
            i = n
            
            for w in tfidf[c][s]:
                if (i == 0):
                    break
                tmp[c][s][w] = tfidf[c][s][w]
                i -= 1
            
    filename = "../results/"+str(n)+"_most_distinctive_words_by_sentiment_by_category.json"
    fpath = Path(filename)
    json_list = json.dumps(tmp, indent=4)

    path = os.path.dirname(fpath)
    if not os.path.isdir(path):
        os.makedirs(path)

    with open(fpath, "w") as f:
        f.write(json_list)

    print("See "+filename+" for TF-IDF scores of each word by sentiment by category")


def main():
    parser = argparse.ArgumentParser()
    
    parser.add_argument('-c', metavar='Input JSON file', type=str, required=True)
    parser.add_argument('-n', metavar='Number of words', type=str, required=True)
    
    args = parser.parse_args()

    input_filename = args.c
    num_words = int(args.n)

    load_input_data(input_filename)
    load_tfidf()
    store_tfidf_to_file(num_words)


if __name__ == "__main__":
    main()
