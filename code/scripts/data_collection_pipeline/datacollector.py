import http.client, urllib.parse
import json
import pathlib
from pathlib import Path

#Script purpose: This script is used as a work around to the free developer tier limitations of the "mediastack" news article api. (i.e. limitation of 100 articles per request.)
#
#Script overview: This article loops through the total number of article hits divided by 100, rounded up to the nearest integer. Each 100 batch of articles is appended to the last and will require the use of manual edits using notepad (i.e. the 'replace all' feature) and some
#minor preparation using raw_data_prepartion.py. A fully automated version is in progress, time permitting. At the present time, the total number of hits is hard-coded and must be verified at each to use to make sure the entire set of articles is obtained.
#
#IMPORTANT: At the present moment, each single run of this script will use up 78 of the 1000 requests allotted per month to free developer tier accounts. Be careful running it!

def fetch_data(given_offset):

    conn = http.client.HTTPConnection('api.mediastack.com')

    #Build url with parameters.
    params = urllib.parse.urlencode({
        'access_key': '2d7a725a3ca7295cf7157c7f2b99c23d',
        'keywords': 'taylor swift',
        'languages': 'en,fr',
        'countries': 'us,ca',
        'offset': given_offset,
         'limit': 100,
        })

    conn.request('GET', '/v1/news?{}'.format(params))

    response = conn.getresponse()
    data = response.read().decode('utf-8')
    data = json.loads(data)

    return data

def write_data(given_data, given_filename):
    #Write JSON to file.
    with open(given_filename, 'w') as outfile:
        json.dump(given_data.decode('utf-8'), outfile)

    outfile.close()

def append_data(given_data, given_filename):
    #Append JSON to file.
    with open(given_filename, 'a') as outfile:
        json.dump(given_data, outfile)

    outfile.close()

def load_data(given_filename):
    fpath = Path(given_filename)

    if not fpath.exists():
        raise Exception(f"File {fpath} does not exist.")

    with open(fpath, encoding='UTF-8') as file:
        data = file.read()
        data = json.loads(data.replace('\\\\"', '\\"'))

    file.close()

    return data

def main():

    #Iteration by 100 articles.
    initial_offset = 0
    offset_increment = 100
    final_offset = 7868 #7868 is total number of articles

    for i in range(initial_offset, final_offset, offset_increment):
        response_data = fetch_data(i)
        append_data(response_data, "formatted_swift_data.json")

    #Manually replace pagination line with ,\n

if __name__ == "__main__":
    main()
