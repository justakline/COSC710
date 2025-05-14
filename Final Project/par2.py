
from __future__ import annotations
import csv
import random
import re

import pymysql

# Sentiment
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer


sia = SentimentIntensityAnalyzer()




def get_all_drinks_names(path):
    drinks = list()
    with open(path, "r") as file:
        csv_file = csv.reader(file)
        for line in csv_file:
            cleaned_title = get_valid_starbucks_drink_name(line[0])
            drinks.append(cleaned_title)
    return drinks

# There were special charachters and some had the word drink or starbucks in it and those don't help with customization of
# The reccomendations... also there was mispellings due to the replacement of non-good letters
def get_valid_starbucks_drink_name(drink):

    return  ((re.sub("[^0-9a-zA-Z ]+", "",drink)).lower().replace("starbucks ", "")
             .replace("drink ", "").replace(" drink", "").replace("caff", "caffe" )
             .replace("crme", "creme"))


def get_all_suggestion_owners(path):
    owners = []

    with open(path, "r") as file:
        for line in file.readlines():
            owners.append(line)
    return owners

def get_all_suggestion_bodies(owner):
    conn = pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='12345',
        db='set_local',
        port=3306
    )

    cursor = conn.cursor()


    cursor.execute(f"""
        select body
        from sbf_suggestion
        where author like "%{owner}%"
    """)

    results = cursor.fetchall()
    finalized_result =  [ result[0] for result in results]

    return finalized_result


def get_all_comment_bodies(owner):
    conn = pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='12345',
        db='set_local',
        port=3306
    )

    cursor = conn.cursor()


    cursor.execute(f"""
        select body
        from sbf_comment
        where author like "%{owner}%"
    """)

    results = cursor.fetchall()

    finalized_result =  [ result[0] for result in results]

    return finalized_result

def validate_texts(texts):
    for i in range(len(texts)):
        texts[i] = get_valid_starbucks_drink_name(texts[i])
    return texts



def main():

    # Drinks were found here: https://web.archive.org/web/20130206005132/http://www.starbucks.com/menu/catalog/nutrition?drink=all&page=3
    # Using the way back machine
    all_drinks_names = get_all_drinks_names("drinks.csv")
    all_drinks_tokenized = [drink.split(" ") for drink in all_drinks_names]

    all_suggestion_owners = get_all_suggestion_owners("suggestions_owner.txt")



    author_to_drinks = dict()
    i  = 0
    for owner in all_suggestion_owners:
        if( i %20 == 0):
            print(i)
        i+=1
        # every text with an associated score of positivity
        all_texts = get_all_suggestion_bodies(owner) + get_all_comment_bodies(owner)
        all_texts = validate_texts(all_texts)
        all_scores = [sia.polarity_scores(text)["compound"] for text in all_texts]

        drink_attitudes = { drink:0 for drink in all_drinks_names}
        for text, score in zip(all_texts, all_scores):
            for word in text.split(" "):
                for i, drink in enumerate(all_drinks_tokenized):
                    if(word in drink):
                        drink_attitudes[" ".join(drink)] +=  score

        sorted_drink_attitudes =  dict(sorted(drink_attitudes.items(), key=lambda item: item[1], reverse=True))

        author_to_drinks[owner] = list(sorted_drink_attitudes.items())[:3]

    with open("drink_recomendations.csv", "w", newline='') as file:
        writer = csv.writer(file)
        for author, drink_list in author_to_drinks.items():
            row = [author] + [drink[0] for drink in drink_list]
            writer.writerow(row)



if __name__ == "__main__":
    main()
