# COMP 370 Fall 2023 Project

## Roadmap

- [x] Question definition
- [x] Data collection
- [X] Data annotation
- [X] Data analysis
- [X] Interpretation
- [X] Communication

## DATA Files
* `annotation_swift_data.csv`
  - All articles and fields with MANUAL Annotation of Topics and Sentiment
* `prediction.csv` 
  - Naive Bayes Results
* `pos_tag_sentiment_analysis.csv` 
  - All Articles and fields with COMPUTATIONAL Sentiment Score
* `shuffled_untokenized_article_swift_data.json` 
  - Main Data file for 500 articles
* `formatted_swift_data.json` 
  - Original pull of 7.8K articles
* `10_most_distinctive_words_by_sentiment_by_category.json` 
  - TF-IDF Values

## SCRIPTS
* Each seperated by respective folders
### Data Collection Pipeline
* `data_collection_pipeline/datacollector.py` - Done by DONALD
  - Pulls articles from a web API (for initial data collection)
  - returns `data_collection_pipeline/formatted_swift_data.json`

* `data_collection_pipeline/raw_data_preparation.py` - Done by DONALD
  - Minor script to remove padding. Comments section describes manual process leading to how this script is used.
  - returns `data_collection_pipeline/formatted_swift_data.json

* `data_collection_pipeline/cleanfilter.py` - Done by CHELSEA
  - Removes URL duplicates and any articles without 'Taylor Swift' in the title
  - Returns 2984 valid articles
  - returns `data_collection_pipeline/formatted_swift_data.json`

* `data_collection_pipeline/priorityselector.py` - Done by CHELSEA
  - Generates two data files: (1) Articles on URL Reference List and (2) Remaining articles
  - Based on URL Reference List, we have:
    - 336 articles sourced from a hostname in the list
    - 2648 articles that are not sourced from a hostname in the list
  - returns `data_collection_pipeline/filtered_swift_data.json`

* `data_collection_pipeline/contentscraper.py` - Done by CHELSEA
  - Navigates into the URL to pull the content of the article for 500 articles
  - returns `shuffled_untokenized_article_swift_data.json`

* `data_collection_pipeline/createcsv.py` - Done by CHELSEA
 - returns `data_collection_pipeline/formatted_swift_data.json`
  - Creates a CSV file and individual text files for reading
  - returns `annotation_swift_data.csv`

* `data_collection_pipeline/amend.py` - Done by CHELSEA
  - Script to fix the missing content files, and amends data issues by resampling new article sources.


### Data Annotation Analysis
* `get_annotation_stats.py` - Done by SISSY
```
py get_annotation_stats.py -d ../data/annotation_swift_data.csv
```
  - Returns `num_articles_by_category_for_500_articles.json`
* `compile_word_counts.py` - Done by SISSY
```
py compile_word_counts.py -o ../results/word_count_with_frequency_threshold_of_5.json -d ../data/annotation_swift_data.csv -f 5
```
  - Returns `word_count_with_frequency_threshold_of_5.json` and `tokenized_words.txt`
* `compute_tfidf.py` - Done by SISSY
```
py compute_tfidf.py -c ../results/word_count_with_frequency_threshold_of_5.json -n 10
```
  - Returns `10_most_distinctive_words_by_sentiment_by_category.json`

### Naive Bayes Topic Analysis
* `journal.ipynb` - Done by YU HAO
  - computes Naive Baye's model for topics
  - returns `predictions.csv`

### SentiWordNet Sentiment Analysis
* `positional_tag_sentiment_analysis.ipynb` - Done by CHELSEA
  - computes the sentiment score for each article using smooth TF-IDF and SentiWordNet
  - returns `pos_tag_sentiment_analysis.csv`


## Contact
* For the purposes of this project, not all files were provided, only the main files.*
* Chelsea Chisholm - chelsea.chisholm2@mail.mcgill.ca
* Sissy Chen - xi.chen20@mail.mcgill.ca
* Yu Hao Tian - yu.h.tian@mail.mcgill.ca
* Donald Szeto - donald.szeto@mail.mcgill.ca
