import pandas as pd
import json
from contentscraper import fetchcontent
import random
import createcsv
import argparse

def replaceArticles(idlist, json_data, df_csv):
    pass



def fetchContentOfEmpty(df, json_data, non_priority_json):
    """_summary_

    Args:
        df (_type_): _description_
        json_data (_type_): _description_
        non_priority_json (_type_): _description_
    """
    # get list of ids where the content is na
    empty_content_index = [(i, df[df['id'] == i].first_valid_index()) for i, j in enumerate(json_data) if j['id'] is not None and j['content'] == '']
    print("Fetching content for the following articles:\n", [i for i, _ in empty_content_index])
    for id, dfid in empty_content_index:
        new_json = json_data[id]
        
        new_json = fetchcontent((new_json['id'], new_json))
        
        while (new_json == None or new_json['content'] == ''):
            randint = random.randint(0, len(non_priority_json)-1)
            
            new_json = non_priority_json.pop(randint)
            
            if df[df['url'] == new_json['url']].size != 0:
                new_json = None
                continue
            
            new_json = fetchcontent((json_data[id]['id'], new_json))
            if new_json is not None and new_json['content'] == '':
                new_json = None
        
        if 'image' in new_json: new_json.pop('image')
        if 'language' in new_json: new_json.pop('language')
        
        json_data[id] = new_json
        for k in new_json.keys():
            try:
                df.at[dfid, k] = new_json[k]
                json_data[id][k] = new_json[k]
            except: 
                print(new_json)
                exit()
    
    return (df, json_data)


def main(args):
    # load in the annotation csv file, the json, and the non_priority_filtered data
    df = pd.read_csv(args.csv_data, index_col=0)
    
    with open(args.json_data, "r") as f:
        json_data = json.load(f)
    
    with open(args.non_priority_data, "r") as f:
        non_priority_json = json.load(f)
    
    # re fetch content of empty ones, if requests gives back nothing
    # we re sample from a non-priority article
    df, json_data = fetchContentOfEmpty(df, json_data, non_priority_json)
    createcsv.createtxtfiles(json_data)
    df.to_csv(args.csv_data, index=True)
    
    with open(args.json_data, "w") as f:
        json.dump(json_data, f, indent=2)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-j', '--json-data', required=True)
    parser.add_argument('-c', '--csv-data', required=True)
    parser.add_argument('-n', '--non-priority-data', required=True)
    args = parser.parse_args()
    main(args)