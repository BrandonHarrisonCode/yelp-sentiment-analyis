import spacy
from pathlib import Path

nlp = spacy.load(Path('./models'))

#text = "Went in for a lunch. The Steak sandwich was delicious, and the Caesar salad had an absolutely delicious dressing, with a perfect amount of dressing, and distributed perfectly across each leaf. I know I'm going on about the salad... But it was perfect. Drink prices were pretty good. The server, dawn was friendly and accomodating. Very happy with her. In summation, a great pub experience. Would go again!"
text = "We ordered the dim sum. I thought the dumplings were okay. The lo mein tasted try and the spring rolls were good."
for sentence in text.split('.'):
    doc = nlp(sentence.lower())
    for ent in doc.ents:
        print(ent.label_, ent.text)
