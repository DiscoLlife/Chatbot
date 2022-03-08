#import hannah

#Start with Greeting

#User inputs reply to greeting

#taking key nouns out of text to decipher see: https://spacy.io/ to decifer text patterns

#list of patterns 

#Reads the Character Text File
import spacy
import nltk
from nltk.stem import WordNetLemmatizer
nltk.download('wordnet')
nltk.download('omw-1.4')
lemmatizer = WordNetLemmatizer()

text_noun = []
text_entity = []
text_verb = []
#Opens the .txt file and puts it throught natural language processing (nlp)
nlp = spacy.load('en_core_web_sm')
text_file = open('CharacterText.txt')
text = text_file.read()
text = text.replace('\n', ' ')
text = nlp(text)
#seperates nouns into a list
text_verb = [token.lemma_ for token in text if token.pos_ == "VERB"]
text_noun = [chunk.text for chunk in text.noun_chunks]

#seperates entities such as numbers or people into a seperate list and labels them
position = 0
for entity in text.ents:
  text_entity.append([entity.text])
  text_entity[position].append(entity.label_)
  position += 1

#prints the nouns and entities
print("Nouns:")
print(text_noun)

print("Verbs:")
print(text_verb)

print("Entitys:")
print(text_entity)

#Identify speech patterns in nouns and verbs and entitys
noun_patterns = []
verb_patterns = []
entity_patterns = []

#Nouns Patterns
position = 0
for each in text_noun:
  if text_noun.count(text_noun[position]) >= 2:
    if noun_patterns.count(text_noun[position]) < 1:
      noun_patterns.append(text_noun[position])
  position = position + 1

print("Noun Patterns Detected:")
print(noun_patterns)

#Verb Patterns
position = 0
for each in text_verb:
  if text_verb.count(text_verb[position]) >= 2:
    if verb_patterns.count(text_verb[position]) < 1:
      verb_patterns.append(text_verb[position])
  position = position + 1

print("Verb Patterns Detected:")
print(verb_patterns)

#Entity Patterns
position = 0
for each in text_entity:
  if text_entity.count(text_entity[position]) >= 2:
    if entity_patterns.count(text_entity[position]) < 1 and not (text_entity[position][1] == 'ORDINAL' or text_entity[position][1] == 'CARDINAL'):
      entity_patterns.append(text_entity[position])
  position = position + 1

print("Entity Patterns Detected:")
print(entity_patterns)

#Removes differnt words that means the same thing, i.e. 'Study',' Studying' => 'Study'
verb_lemmatized = []
noun_lemmatized = []

position = 0
for each in verb_patterns:
  if len(verb_patterns) > position:
    if verb_lemmatized.count(str.lower(lemmatizer.lemmatize(verb_patterns[position], pos = 'v'))) < 1:
      verb_lemmatized.append(str.lower(lemmatizer.lemmatize(verb_patterns[position], pos = 'v')))
  position = position + 1

position = 0
for each in noun_patterns:
  if len(noun_patterns) > position:
    if noun_lemmatized.count(str.lower(lemmatizer.lemmatize(noun_patterns[position], pos = 'n'))) < 1:
      noun_lemmatized.append(str.lower(lemmatizer.lemmatize(noun_patterns[position], pos = 'n')))
  position = position + 1
  
print("Lemmatized Verbs:")
print(verb_lemmatized)
print("Lemmatized Nouns:")
print(noun_lemmatized)






