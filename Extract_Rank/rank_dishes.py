import os
import ujson
import spacy
import time
import jellyfish
import collections
from textblob import TextBlob
from pathlib import Path

similarity_threshold = 0.8

def rank_dishes(nlp, reviews):
    dish_polarities = collections.defaultdict(list)
    for user_id, stars, text in reviews:
        for sentence in text.split('.'):
            doc = nlp(sentence.lower())
            if not any(ent.label_ == 'DISH' for ent in doc.ents):
                continue
            polarity = TextBlob(sentence).sentiment.polarity
            for ent in doc.ents:
                if ent.label_ == 'DISH':
                    dish_polarities[ent.text.split(' and ')[0].split(' with ')[0]].append(polarity)

    # Combines dishes with a similarity score of at least similarity_threshold. Picks the shortest name
    for dish in list(dish_polarities):
        if dish in dish_polarities:
            name = dish
            polarities = dish_polarities[dish]
            similar = []
            for other in list(dish_polarities):
                if jellyfish.jaro_distance(dish, other) > similarity_threshold and other != dish:
                    similar.append(other)
            for other in similar:
                if len(other) < len(name):
                    name = other
                polarities += dish_polarities[other]
            for other in similar:
                if other != name:
                    del dish_polarities[other]
            if dish != name:
                del dish_polarities[dish]
            dish_polarities[name] = polarities

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
