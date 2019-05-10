import os
import ujson
import spacy
import time
from collections import Counter
from pathlib import Path

def get_dishes(nlp, reviews):
    # for now just counts the number of times each dish is mentioned
    dishes = Counter()
    for user_id, stars, text in reviews:
        for sentence in text.split('.'):
            doc = nlp(sentence.lower())
            for ent in doc.ents:
                if ent.label_ == 'DISH':
                    dishes[ent.text] += 1
    return dishes

if __name__ == '__main__':
    start = time.time()

    max_bytes = 2**31 - 1
    file_path = 'reviews.json'
    input_size = os.path.getsize(file_path)
    with open(file_path, 'r') as f:
        load = [f.read(max_bytes) for _ in range(0, input_size, max_bytes)]
        reviews = ujson.loads(''.join(load))

    mid = time.time()
    print('Time to load reviews from file:', mid - start)
    
    restaurant_id = 'QXAEGFB4oINsVuTFxEYKFQ'
    nlp = spacy.load(Path('../Dish_Model/models'))
    dishes = get_dishes(nlp, reviews['QXAEGFB4oINsVuTFxEYKFQ'])
    print(dishes.most_common(10))

    print('Time to extract dishes from a restaurant:', time.time() - mid)
