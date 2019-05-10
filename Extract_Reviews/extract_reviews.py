import os
import time
import ujson
import boto3

bucket_name = os.environ['S3BUCKET']
business_key = os.environ['BUSINESS_KEY']
reviews_key = os.environ['REVIEWS_KEY']

s3 = boto3.client(
    's3',
    aws_access_key_id=os.environ['AWS_ACCESS_KEY'],
    aws_secret_access_key=os.environ['AWS_SECRET_KEY'],
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
    line_iter = get_s3_file_iter(bucket_name, business_key)
    restaurants = set()
    print('Loading restaurants from downloaded file...')
    for line in line_iter:
        jso = ujson.loads(line)
        if jso['categories'] and 'Restaurants' in jso['categories']:
            restaurants.add(jso['business_id'])
    print('Done getting restaurants.')
    return restaurants


def get_reviews_for_restaurants(restaurants):
    print('Getting reviews from AWS...')
    line_iter = get_s3_file_iter(bucket_name, reviews_key)
    reviews = {}
    print('Loading reviews from downloaded file...')
    for line in line_iter:
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

    dump = ujson.dumps(reviews)
    s3.put_object(
        ACL='public-read',
        Body=dump,
        Bucket=bucket_name,
        Key='restaurants-and-reviews.json',
    )

    print('Time to write dictionary into file:', time.time() - mid)
