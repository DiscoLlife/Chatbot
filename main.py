#import hannah

#Start with Greeting

#User inputs reply to greeting

#taking key nouns out of text to decipher see: https://spacy.io/ to decifer text patterns

#list of patterns 

#Reads the Character Text File
import spacy
textnouns = []
textentity = []
textverb = []
#Opens the .txt file and puts it throught natural language processing (nlp)
nlp = spacy.load('en_core_web_sm')
text_file = open('CharacterText.txt')
text = text_file.read().lower()
text = text.replace('\n', ' ')
text = nlp(text)
#seperates nouns into a list
textverb = [token.lemma_ for token in text if token.pos_ == "VERB"]
textnouns = [chunk.text for chunk in text.noun_chunks]

#seperates entities such as numbers or people into a seperate list and labels them
position = 0
for entity in text.ents:
  textentity.append([entity.text])
  textentity[position].append(entity.label_)
  position += 1

#prints the nouns and entities
print(textnouns)
print(textverb)
print(textentity)

#Identify speech patterns in nouns and verbs
nounpatterns = []
verbpatterns = []

position = 0
for each in textnouns:
  if textnouns.count(textnouns[position]) >= 2:
    if nounpatterns.count(textnouns[position]) < 1:
      nounpatterns.append(textnouns[position])
  position = position + 1

print("Noun Patterns Detected:")
print(nounpatterns)

position = 0
for each in textverb:
  if textverb.count(textverb[position]) >= 2:
    if verbpatterns.count(textverb[position]) < 1:
      verbpatterns.append(textverb[position])
  position = position + 1

print("Verb Patterns Detected:")
print(verbpatterns)
