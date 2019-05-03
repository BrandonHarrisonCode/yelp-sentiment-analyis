import csv
import random
import spacy
from spacy.util import minibatch, compounding
from pathlib import Path

data = []
verbose = True
iterations = 20

def debug(text):
    global verbose
    if verbose:
        print(text)

# Read in training data and put manually approved samples in a list
debug('Parsing training_data.csv')
with open('training_data.csv', 'r', encoding='utf8') as file:
    for row in csv.DictReader(file):
        if row['AssignmentStatus'] == 'Approved':
            review = row['Input.review']
            dishes = row['Answer.utterance'].lower().replace('.', '').split(',')
            if dishes[0] == 'none':
                data.append((review, {'entities': []}))
            else:
                indices = []
                for dish in dishes:
                    dish = dish.strip()
                    if dish in review and len(dish) > 0:
                        ind = review.index(dish)
                        indices.append((ind, ind + len(dish), 'DISH'))
                data.append((review, {'entities': indices}))

# A lot of the code below was taken from spacy.io's tutorial for training a custom NER model

# Create a blank model
debug('Creating blank model')
nlp = spacy.blank('en')
if 'ner' not in nlp.pipe_names:
    ner = nlp.create_pipe('ner')
    nlp.add_pipe(ner)
else:
    ner = nlp.get_pipe('ner')
ner.add_label('DISH')

# Train model
debug('Training model')
optimizer = nlp.begin_training()
pipes = [pipe for pipe in nlp.pipe_names if pipe != 'ner']
with nlp.disable_pipes(*pipes):
    for i in range(iterations):
        debug('Iteration: ' + str(i+1) + ' of ' + str(iterations))
        random.shuffle(data)
        losses = {}
        batches = minibatch(data, size=compounding(4., 32., 1.001))
        for batch in batches:
            texts, annotations = zip(*batch)
            nlp.update(texts, annotations, sgd=optimizer, drop=0.35, losses=losses)
        print('Losses', losses)

# Save model to disk
debug('Saving model to disk')
output_dir = Path('./models')
if not output_dir.exists():
    output_dir.mkdir()
nlp.meta['name'] = 'dishes'
nlp.to_disk(output_dir)


            
