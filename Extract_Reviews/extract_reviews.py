import os
import time
import ujson
import boto3
import copy
import collections
import spacy
import jellyfish
import itertools
from textblob import TextBlob
from pathlib import Path
from multiprocessing.pool import ThreadPool

pool = ThreadPool(4)

bucket_name = os.environ['S3BUCKET']
business_key = os.environ['BUSINESS_KEY']
reviews_key = os.environ['REVIEWS_KEY']
table = os.environ['DYNAMODB_TABLE']
similarity_threshold = 0.8

s3 = boto3.client(
    's3',
    aws_access_key_id=os.environ['AWS_ACCESS_KEY'],
    aws_secret_access_key=os.environ['AWS_SECRET_KEY'],
)

dynamodb = boto3.client(
    'dynamodb',
    aws_access_key_id=os.environ['AWS_ACCESS_KEY'],
    aws_secret_access_key=os.environ['AWS_SECRET_KEY'],
    region_name=os.environ['AWS_REGION'],
)

def get_s3_file_iter(bucket, key):
    response = s3.get_object(
        Bucket=bucket,
        Key=key,
    )
    if response and response.get('Body') is not None:
        return response['Body'].iter_lines(chunk_size=(2**20) * 100)
    raise IOError('Could not access {} at {}'.format(key, bucket))


def get_restaurants():
    print('Getting restaurants from AWS...')
    # line_iter = get_s3_file_iter(bucket_name, business_key)
    line_iter = open('business.json')
    restaurants = collections.defaultdict(dict)
    print('Loading restaurants from downloaded file...')
    for line in line_iter:
        jso = ujson.loads(line)
        if jso['categories'] and 'Restaurants' in jso['categories']:
            restaurants[jso['business_id']]['id'] = jso['business_id']
            restaurants[jso['business_id']]['name'] = jso['name']
            restaurants[jso['business_id']]['lat'] = jso['latitude']
            restaurants[jso['business_id']]['lng'] = jso['longitude']

    print('Done getting restaurants.')
    return restaurants


def get_reviews_for_restaurants(restaurants):
    print('Getting reviews from AWS...')
    # line_iter = get_s3_file_iter(bucket_name, reviews_key)
    line_iter = open('review.json')
    reviews = copy.deepcopy(restaurants)
    print('Loading reviews from downloaded file...')
    for line in line_iter:
        jso = ujson.loads(line)
        if jso['business_id'] in restaurants:
            if reviews[jso['business_id']].get('reviews') is None:
                reviews[jso['business_id']]['reviews'] = []

            review = (jso['user_id'], jso['stars'], jso['text'].replace('\n',' '))
            reviews[jso['business_id']]['reviews'].append(review)

    return reviews


def rank_dishes(nlp, business):
    reviews = business['reviews']
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

    business['dishes'] = sorted(dish_scores, key=lambda x: x[1], reverse=True)
    write_to_dynamo(business)

# Bayesian Average Ratings - http://www.evanmiller.org/bayesian-average-ratings.html
def score(polarities):
    votes = [2] * 11
    for polarity in polarities:
        votes[round(polarity * 5) + 5] += 1
    return sum(v * u for (v, u) in zip(votes, range(-5, 6))) / sum(votes)


def write_to_dynamo(business):
    print('Pushing {} to dynamo'.format(business['id']))
    dynamodb.put_item(
        TableName=table,
        Item={
            'RestaurantId': {
                'S': business['id'],
            },
            'Name': {
                'S': business['name'],
            },
            'Lat': {
                'N': str(business['lat']),
            },
            'Lng': {
                'N': str(business['lng']),
            },
            'Dishes': {
                'S': str(business['dishes']),
            },
            'Reviews': {
                'S': str(business['reviews']),
            },
        }
    )



if __name__ == '__main__':
    nlp = spacy.load(Path('../Dish_Model/models'))
    start = time.time()
    reviews = get_reviews_for_restaurants(get_restaurants())
    mid = time.time()
    print('Time to extract all reviews into dictionary:', mid - start)
    pool.starmap(rank_dishes, zip(itertools.repeat(nlp), reviews.values()))
    print('Time to extract and rank dishes:', time.time() - mid)
    print('Time to write dictionary into dynamo:', time.time() - mid)
