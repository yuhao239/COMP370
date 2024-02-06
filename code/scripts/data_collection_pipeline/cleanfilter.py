import json

def cleanfilter(input):
    # takes a JSON file "input"
    # returns NONE, but creates a JSON file with the filter requirements below
    # removes URL duplicates
    # removes any entries without Taylor Swift in the Title
    # 2984 valid articles!!!!
    jsonRaw = None
    with open(input, "r") as f:
        jsonRaw = json.load(f)
    data = jsonRaw['data']

    uniqueUrls = set()

    def filterfunc(element):
        # takes an element from dictionary
        # return boolean
        # if URL is unique -> check Taylor Swift in Title
        # returns False if URL already exists

        if element["url"] in uniqueUrls:
            return False
        uniqueUrls.add(element["url"])
        return "taylor swift" in element["title"].lower()
        
    filteredData = filter(filterfunc,data)
    # convert to list
    filteredData = list(filteredData)
    #print(len(filteredData))
    with open("filtered_swift_data.json" ,"w") as f:
        json.dump(filteredData, f, indent=2)

cleanfilter("formatted_swift_data.json")


