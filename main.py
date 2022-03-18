#import hannah

#Start with Greeting

#User inputs reply to greeting

#taking key nouns out of text to decipher see: https://spacy.io/ to decifer text patterns

#list of patterns 

#Reads the Character Text File
import string
import spacy
from spacy.matcher import Matcher
import nltk
from nltk.stem import WordNetLemmatizer
nltk.download('wordnet')
nltk.download('omw-1.4')
nltk.download('averaged_perceptron_tagger')
nlp = spacy.load('en_core_web_sm')
lemmatizer = WordNetLemmatizer()
nounmatcher  = Matcher(nlp.vocab)
verbmatcher = Matcher(nlp.vocab)

text_noun = []
text_entity = []
text_verb = []
#Opens the .txt file and puts it throught natural language processing (nlp)
#Also tokenises & tags text for later usage
txt = open('CharacterText.txt')
txt = txt.read()
nlp = spacy.load('en_core_web_sm')
text = txt
text = text.replace('\n', ' ')
nlptext = nlp(text)
text = text.split()
text = nltk.pos_tag(text)
#seperates nouns into a list
text_verb = [token.lemma_ for token in nlptext if token.pos_ == "VERB"]
text_noun = [chunk.text for chunk in nlptext.noun_chunks]

#seperates entities such as numbers or people into a seperate list and labels them
position = 0
for entity in nlptext.ents:
  text_entity.append([entity.text])
  text_entity[position].append(entity.label_)
  position += 1

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
  position += 1

print("Noun Patterns Detected:")
print(noun_patterns)

#Verb Patterns
position = 0
for each in text_verb:
  if text_verb.count(text_verb[position]) >= 2:
    if verb_patterns.count(text_verb[position]) < 1:
      verb_patterns.append(text_verb[position])
  position += 1

print("Verb Patterns Detected:")
print(verb_patterns)

#Entity Patterns
position = 0
for each in text_entity:
  if text_entity.count(text_entity[position]) >= 2:
    if entity_patterns.count(text_entity[position]) < 1 and not (text_entity[position][1] == 'ORDINAL' or text_entity[position][1] == 'CARDINAL'):
      entity_patterns.append(text_entity[position])
  position += 1

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
  position += 1

position = 0
for each in noun_patterns:
  if len(noun_patterns) > position:
    if noun_lemmatized.count(str.lower(lemmatizer.lemmatize(noun_patterns[position], pos = 'n'))) < 1:
      noun_lemmatized.append(str.lower(lemmatizer.lemmatize(noun_patterns[position], pos = 'n')))
  position += 1
  
print("Lemmatized Verbs:")
print(verb_lemmatized)
print("Lemmatized Nouns:")
print(noun_lemmatized)

#takes tokenised text and extracts meaningful phrases from it
#text_chunks = ''
#grammar = "NP : {<DT>?<JJ>*<NN> } "

#parser = nltk.RegexpParser(grammar)
#text_chunks = parser.parse(text)

#text_chinks = ''
#grammar = r""" NP: {<.*>+}
#                    }<JJ>+{"""
#parser = nltk.RegexpParser(grammar)
#text_chinks = parser.parse(text)


txtlist = []
dupetxt = txt
position = 0
#Turns the txt into a list of phrases
while True:
  try:
    if dupetxt[position] == '\n':
      txtlist.append(dupetxt[0:position].lower())
      dupetxt = dupetxt.strip(dupetxt[0:position])
      position = 0
    position += 1
  except:
    print('done')
    break

#Sets up the pattern matchers
names = []
position = 0
for each in entity_patterns:
  if entity_patterns[position][1] == "PERSON":
    names.append(entity_patterns[position][0].lower())
  position += 1
  print(names)

byes = ["bye","goodbye","cya","see you","later"]
noun_pattern = [{"LEMMA": {"IN": noun_lemmatized}}]
verb_pattern = [{"LEMMA": {"IN": verb_lemmatized}}]
nounmatcher.add("NOUN", [noun_pattern])
verbmatcher.add("VERB", [verb_pattern])

#Test phrases for various intents such as greeting or good bye type messages
position2 = 0
def IntentMatcher(string, intent):
  if intent == "greet":
    stringcontain = [ele for ele in names if(ele in string)]
    if bool(stringcontain) and ("i" in string or "me" in string or "hello" in string or "my name" in string or "im" in string or "i'm" in string):
      return bool(stringcontain)
    else:
      return False
  elif intent == "bye":
    stringcontain = [ele for ele in byes if(ele in string)]
    return bool(stringcontain)
  else:
    return False
          
#Checks the text for possible greeting and good bye phrases
greetlist = []
byelist = []
position = 0
for each in txtlist:
  if IntentMatcher(txtlist[position], "greet"):
    print("Greeting identified")
    greetlist.append(txtlist[position])
    print(txtlist[position])
  if IntentMatcher(txtlist[position], "bye"):
    print("Goodbye identified")
    byelist.append(txtlist[position])
    print(txtlist[position])
  position += 1

#Removes '\n' from the list inserted into the function
def nlineremover(list):
  position = 0
  newlist = []
  for each in list:
    if "\n" in list[position]:
      newlist.append(list[position].strip("\n"))
    else:
      newlist.append(list[position])
    position += 1
  return newlist

greetlist = nlineremover(greetlist)
byelist = nlineremover(byelist)

print("List of possible greetings:")
print(greetlist)

def puncremover(list):
  position = 0
  newlist = []
  for each in list:
    newlist.append(list[position].translate(str.maketrans('', '', string.punctuation)))
    position += 1
  return newlist

def Lemmatize(string):
  lemmatizedstring = ''
  lemmatizedstring += str.lower(lemmatizer.lemmatize(string, pos = 'n'))
  lemmatizedstring += str.lower(lemmatizer.lemmatize(string, pos = 'v'))
  lemmatizedstring += str.lower(lemmatizer.lemmatize(string, pos = 'a'))
  lemmatizedstring += str.lower(lemmatizer.lemmatize(string, pos = 'r'))
  lemmatizedstring += str.lower(lemmatizer.lemmatize(string, pos = 's'))
  return string

#Turns the text into a list of numbers
dupetxt = nlineremover(txt.lower().split())
dupetxt = puncremover(dupetxt)
txtcount = []
txtcountmatch = []
for each in dupetxt:
  countingtxt = dupetxt[0]
  txtcount.append(dupetxt.count(countingtxt))
  txtcountmatch.append(dupetxt[0])
  while dupetxt.count(countingtxt) > 0:
    dupetxt.remove(countingtxt)

print(txtcount)
print(txtcountmatch)

def matchcount(string):
  try:
    count = txtcount[txtcountmatch.index(string.lower())]
  except:
    return 0
  return count

print(matchcount("you"))
print(matchcount("to"))
print(matchcount("father"))

#Calculates the frequency of a word in the text
totalwords = 0
position = 0
for each in txtcount:
  totalwords += txtcount[position]
  position += 1
print(totalwords)
txtfreq = []
position = 0
for each in txtcount:
  txtfreq.append(float(txtcount[position] / totalwords))
  position += 1

print(txtfreq)

print(len(txtfreq))
print(len(txtcountmatch))
print(len(txtcount))

lemmatxt = Lemmatize(txt).lower().split()
lemmatxt = puncremover(lemmatxt)
dupelemmatxt = lemmatxt
position = 0
#Frequency of nouns and verbs
nouncount = []
position = 0
for each in noun_lemmatized:
  nouncount.append(dupelemmatxt.count(noun_lemmatized[position].lower()))
  position = position + 1

#txtcount[txtcountmatch.index(string.lower())]
while nouncount.count(0) > 0:
  position2 = nouncount.index(0)
  nouncount.pop(position2)
  noun_lemmatized.pop(position2)

position = 0
totalnoun = 0
for each in nouncount:
  totalnoun += nouncount[position]
  position += 1

print(totalnoun)

nounfreq = []
position = 0
for each in nouncount:
  nounfreq.append(nouncount[position] / totalnoun)
  position += 1 

print(nounfreq)

