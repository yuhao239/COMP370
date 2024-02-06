from pathlib import Path
import pandas as pd
import argparse
import json
import os

df = None
article_count = dict()

def load_data(filename):
    global df
    df = pd.read_csv(filename, encoding="ISO-8859-1")
    df = df[df['topic open coding 3'].notna()]


def getUniqueCategories(column_name, num_articles):
    arr = list(df[column_name][0:num_articles].unique())
    # print(arr)
    return arr


def save_counts_to_file(input_filename, column_name):
    global df, article_count

    article_count = dict()
    load_data(input_filename)
    num_articles = len(df)
    all_articles_categories = list(df[column_name][0:num_articles])

    for article_category in all_articles_categories:
        if article_category not in article_count.keys():
            article_count[article_category] = 1
        else:
            article_count[article_category] += 1

    sorted_by_descending_count = sorted(article_count.items(), key=lambda kv:(kv[1]), reverse=True)
    article_count = dict(sorted_by_descending_count)
    
    output_filename = "../results/num_articles_by_category_for_"+str(num_articles)+"_articles.json"
    fpath = Path(output_filename)
    json_list = json.dumps(article_count, indent=4)

    path = os.path.dirname(fpath)
    if not os.path.isdir(path):
        os.makedirs(path)

    with open(fpath, "w") as f:
        f.write(json_list)

    print("See "+output_filename+" for annotation stats")


def main():
    parser = argparse.ArgumentParser()
    
    parser.add_argument('-d', metavar='Input CSV file', type=str, required=True)
    
    args = parser.parse_args()

    input_filename = args.d

    save_counts_to_file(input_filename, 'topic open coding 3')


if __name__ == "__main__":
    main()
    