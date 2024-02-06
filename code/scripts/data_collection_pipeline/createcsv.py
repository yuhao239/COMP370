import json
import random
import pandas as pd
def createCsv(data):
    # for each field within a json element, create a key-value 
    # where key is the json element and the value is a list
    csvDict = {key:[] for key in data[0].keys()}
    for element in data:
        for key, fields in csvDict.items():
            fields.append(element[key])
    
    df = pd.DataFrame(csvDict)
    df.to_csv('./annotation_swift_data.csv')
    

def createtxtfiles(data):
    for article in data:
        with open(f'./articletextfiles/{article["id"]}.txt' ,"w") as f:
            title = article['title']
            desc = article['description']
            content = article['content'].replace('/n', '\n')
            f.write(f'TITLE: {title}\n\nDESCRIPTION:\n{desc}\n\nCONTENT:\n{content}')

def main():
    with open('shuffled_untokenized_article_swift_data.json') as f:
        data = json.load(f)
    
    # create textfiles from the data.
    createtxtfiles(data)

    # create csv file from the data.
    createCsv(data)
    
    pass
if __name__ == "__main__":
    main()
        