import json

#Script purpose: This is a very minor Python script that replaces the sections padded with # symbols before and after a number representing the offset after each batch as part of the data collection process.
#
#Required input: The intended input had been manually edited with notepad, using the 'replace all' feature, to remove a section (e.g. "]}{"pagination": {"limit": 100, "offset": 100, "count": 100, "total": 7868}, ") that represents the 'header' of each batch of article data request.
#
#Brief overall data collection process:
#1. For n number of total articles (found in request result header) matching the search criteria (e.g. 'taylor swift' keyword, article categories, and country specifications), repeat article request by n/100 times (at the free tier, each article request batch is limited to 100 articles).
#2. Append each request to the last in a text file.
#3. Use notepad to look for the section before offset (e.g. in "]}{"pagination": {"limit": 100, "offset": 100, "count": 100, "total": 7868}, " you would look for and replace "]}{"pagination": {"limit": 100, "offset": " with ######.
#4. Use notepad to look for the section before offset (e.g. in "]}{"pagination": {"limit": 100, "offset": 100, "count": 100, "total": 7868}, " you would look for and replace ", "count": 100, "total": 7868}, ": " with ######.
#5. If the final article request batch starts with 7800, as in the example, the final segment will have a different count and must be searched and replaced separately. For the example, it would be ", "count": 68, "total": 7868}, ".
#6. This script is then ran with the output from the datacollection.py script having undergone the above intermediate data cleaning steps to replace all ######NUMBER HERE###### segments with a new line.
#7. The data is now ready to be loaded as a proper json file and analyzed accordingly.
#Note: There may be unintended kinks with the script. The first initial run-through required manually running through and replace the lines with a new line 78 times. It was not fun. Work is ongoing to find and workout kinks to create an automated pipeline for other endeavours.

def replace_padding(given_filename):
    with open(given_filename, 'r') as file:
        data = file.read()

        #Replace the specified string with a comma
        #Iteration by 100 articles.
        initial_offset = 0
        offset_increment = 100
        final_offset = 7860 #7851 is total number of articles

        for i in range(initial_offset, final_offset, offset_increment):
            target = '######'+str(i)+'######'
            for line in data:
                if target in line:
                    line.replace(target, ',\n')
                    break

    with open('formatted_swift_data2.json', 'w') as file:
        file.write(data)

def load_json(given_filename):
    with open(given_filename, 'r', encoding='utf-8') as file:
        data = json.load(file)

    return data

def main():

    #replace_padding('formatted_swift_data.json')

    data = load_json('online_parser.json')
    counter = 0

    for i in range(0, 7868):
        if 'taylor swift' in data['data'][i]['title'].lower():
            print(data['data'][i]['title']) #Prints the title of the article
            counter += 1

    print(counter)

if __name__ == '__main__':
    main()
