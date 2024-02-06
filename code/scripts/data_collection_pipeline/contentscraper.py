import bs4
import json
import requests
import random

USER_AGENT= "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
def contentscraper(input, start=0, end=None):
    # takes in a JSON file
    # returns NONE but create a JSON file with extra field "content" and "id"
    data = None
    with open(input, "r") as f:
        data = json.load(f)
    
    if end is None:
        end = len(data)

    scrapedArticles = []
    for element in enumerate(data):
        if len(scrapedArticles) == end:
            break
        scrapedArticle = fetchcontent(element)
        if scrapedArticle is not None:
            scrapedArticles.append(element[1])
    
    return scrapedArticles

def fetchcontent(tupleelement):
    id,element = tupleelement
    print('fetching element: '+str(id))
    try:
        session = requests.session()
        session.cookies.clear()
        response = session.get(url=element["url"], headers={'User-Agent':USER_AGENT})
        
        if not response.ok:
            return None
        
        soup = bs4.BeautifulSoup(response.text,"html.parser")
        bodytag = soup.find("body")
        maintag = bodytag.find("main")
        if maintag:
            element["hasMain"] = True    
            ptags = maintag.findAll("p")
        else:
            element["hasMain"] = False
            ptags = bodytag.findAll("p")
        
        content = "/n".join(map(lambda p: p.getText(),ptags))

        element["id"] = id
        element["content"] = content
        return element
    except:
        print("error encountered at "+str(id))

def main():
    # run scraper for all articles in priority list 
    # number < 500 so we test them all. 
    # 500 - contentscraped_priority articles = num of articles to scrape randomly from
    # non-prio list
    finalArticles = contentscraper("priority_filtered_swift_data.json")

    # no checking for negative count since I know the number of finalArticles < 500
    nonPrioArticleCount = 500 - len(finalArticles)
    finalArticles.extend(contentscraper("non_priority_filtered_swift_data.json", 0, nonPrioArticleCount))

    # shuffle final articles
    random.Random(6).shuffle(finalArticles)
    # rename id's 0-499
    for i, article in enumerate(finalArticles):
        article["id"] = i
        article.pop("image")
        article.pop("language")
   
    # dump final file
    with open("shuffled_untokenized_article_swift_data.json" ,"w") as f:
        json.dump(finalArticles, f, indent=2)

if __name__ == "__main__":
    main()


    



