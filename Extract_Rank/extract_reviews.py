import time
import ujson

def get_restaurants():
    f = open('../../yelp_dataset/business.json', 'r', encoding='utf8')
    restaurants = set()
    for line in f:
        jso = ujson.loads(line)
        if jso['categories'] and 'Restaurants' in jso['categories']:
            restaurants.add(jso['business_id'])
    return restaurants

def get_reviews_for_restaurants(restaurants):
    f = open('../../yelp_dataset/review.json', 'r', encoding='utf8')
    reviews = {}
    for line in f:
        jso = ujson.loads(line)
        if jso['business_id'] in restaurants:
            if jso['business_id'] not in reviews:
                reviews[jso['business_id']] = []

            review = (jso['user_id'], jso['stars'], jso['text'].replace('\n',' '))
            reviews[jso['business_id']].append(review)

    return reviews

if __name__ == '__main__':
    start = time.time()
    reviews = get_reviews_for_restaurants(get_restaurants())
    mid = time.time()
    print('Time to extract all reviews into dictionary:', mid - start)

    max_bytes = 2**31 - 1
    dump = ujson.dumps(reviews)
    with open("reviews.json","w") as f:
        for i in range(0, len(dump), max_bytes):
            f.write(dump[i:i + max_bytes])

    print('Time to write dictionary into file:', time.time() - mid)
