import json
import csv

turk_data = []
restaurants = set()

# Creates a set of restaurant's business_id's
with open('data/business.json', 'r', encoding='utf8') as file:
    for line in file:
        if json.loads(line)['categories'] is not None and 'Restaurants' in json.loads(line)['categories']:
            restaurants.add(json.loads(line)['business_id'])

# Adds reviews to a list if they belong to restaurants
# For now, just add the first 1000 reviews
with open('data/review.json', 'r', encoding='utf8') as file:
    for line in file:
        if len(turk_data) >= 1000:
            break;
        review = json.loads(line)['text'].replace('\n', ' ')
        if all(ord(c) < 128 for c in review) and json.loads(line)['business_id'] in restaurants:
            turk_data.append(review)
        print(len(turk_data))

# Outputs to CSV
with open('turk.csv', 'w') as file:
    writer = csv.DictWriter(file, lineterminator='\n', fieldnames=['review'])
    writer.writeheader()
    for review in turk_data:
        writer.writerow({'review': review})
