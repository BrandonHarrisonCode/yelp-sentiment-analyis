import os
import ujson
import spacy
import time
from collections import defaultdict
from textblob import TextBlob
from pathlib import Path

def rank_dishes(nlp, reviews):
    dish_polarities = defaultdict(list)
    for user_id, stars, text in reviews:
        for sentence in text.split('.'):
            doc = nlp(sentence.lower())
            if not any(ent.label_ == 'DISH' for ent in doc.ents):
                continue
            polarity = TextBlob(sentence).sentiment.polarity
            for ent in doc.ents:
                if ent.label_ == 'DISH':
                    dish_polarities[ent.text].append(polarity)

    pretend_votes = []
    dish_scores = []
    for dish in dish_polarities:
        dish_scores.append((dish, score(dish_polarities[dish])))

    return sorted(dish_scores, key=lambda x: x[1], reverse=True)

# Bayesian Average Ratings - http://www.evanmiller.org/bayesian-average-ratings.html
def score(polarities):
    votes = [2] * 11 
    for polarity in polarities:
        votes[round(polarity * 5) + 5] += 1
    return sum(v * u for (v, u) in zip(votes, range(-5, 6))) / sum(votes)

if __name__ == '__main__':
    start = time.time()
    with open('emerald_reviews.json', 'r') as f:
        reviews = ujson.loads(f.read())
    
    mid = time.time()
    print('Time to load reviews from emerald_reviews.json:', mid - start)
    
    nlp = spacy.load(Path('../Dish_Model/models'))
    dishes = rank_dishes(nlp, reviews)
    print('Time to extract and rank dishes:', time.time() - mid)

    for i in range(20):
        print(i+1, '-', dishes[i][0], round(dishes[i][1], 3))
