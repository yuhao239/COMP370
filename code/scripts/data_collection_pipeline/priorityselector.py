import json
import random

UrlReferenceList = ["forbes.com",
"nytimes.com",
"wsj.com",
"washingtonpost.com",
"newyorker.com",
"ap.org",
"foreignaffairs.com",
"theatlantic.com",
"nbcnews.com",
"cbsnews.com",
"abcnews.go.com",
"cnn.com",
"usatoday.com",
"time.com",
"latimes.com",
"npr.org",
"bloomberg.com",
"usmagazine.com",
"people.com",
"ellecanada.com",
"glamour.com",
"intouchweekly.com",
"vanityfair.com",
"radaronline.com",
"tmz.com",
"etonline.com",
"cbc.ca",
"ctvnews.ca",
"eonline.com",
"perezhilton.com",
"variety.com",]

def priorityselector(input):
    # takes in a JSON file
    # returns NONE but create a JSON file of n unique different article elements
    # samples all articles from input
    data = None
    with open(input, "r") as f:
        data = json.load(f)
    
    # seperates articles into two lists:
    # if article is sourced from URL reference list
    # add to priorityArticle List
    # else add to nonPriorityArticle List
    priorityArticles = [] 
    nonPriorityArticles = []
    for element in data:
        element["isPriority"] = False
        for rUrl in UrlReferenceList:    
            if rUrl in element["url"]:
                element["isPriority"] = True
                priorityArticles.append(element)
                break
        if not element["isPriority"]:
            nonPriorityArticles.append(element) 
    
    # want to randomize the order or non-priority articles
    # so as not to change contentscraper.py, we shuffle list here
    random.Random(24).shuffle(nonPriorityArticles)

    with open("priority_filtered_swift_data.json" ,"w") as f:
        json.dump(priorityArticles, f, indent=2)

    with open("non_priority_filtered_swift_data.json" ,"w") as f:
        json.dump(nonPriorityArticles, f, indent=2)

priorityselector("filtered_swift_data.json")