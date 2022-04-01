#Put text through NLP(Natural Language processing)
#Use data to train a bot/ai
#User sends message
#Message is sent throught intent detection
#bot responds with another message with a hopefully valid response for that intent
#
#Important terms:
#Position - this is used to get a position in a list or text(same for position 2)
#
#
import string
import spacy
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
nltk.download('wordnet')
nltk.download('omw-1.4')
nltk.download('averaged_perceptron_tagger')
nlp = spacy.load('en_core_web_sm')
lemmatizer = WordNetLemmatizer()

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
#seperates verbs into a list
text_verb = [token.lemma_ for token in nlptext if token.pos_ == "VERB"]
#seperates nouns into a list
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
#Repeats for each value in the noun list
for each in text_noun:
  #does the noun appear more than once in the list?
  if text_noun.count(text_noun[position]) >= 2:
    #Is not in the patterns list already? if so, append it to the patterns list
    if noun_patterns.count(text_noun[position]) < 1:
      noun_patterns.append(text_noun[position])
  position += 1


#Verb Patterns
position = 0
#Repeats for each value in the verb list
for each in text_verb:
  #does the verb appear more than once in the list?
  if text_verb.count(text_verb[position]) >= 2:
    #Is not in the patterns list already? if so, append it to the patterns list
    if verb_patterns.count(text_verb[position]) < 1:
      verb_patterns.append(text_verb[position])
  position += 1


#Entity Patterns
position = 0
#Repeats for each entity in the entity list
for each in text_entity:
  #does the entity appear more than once?
  if text_entity.count(text_entity[position]) >= 2:
    #Is it not alredly in the patterns list AND is it not a number of any type?
    if entity_patterns.count(text_entity[position]) < 1 and not (text_entity[position][1] == 'ORDINAL' or text_entity[position][1] == 'CARDINAL'):
      entity_patterns.append(text_entity[position])
  position += 1


#Lemmatize removes differnt words that means the same thing, i.e. 'Study',' Studying' => 'Study'
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
    break

names = []
position = 0
for each in entity_patterns:
  if entity_patterns[position][1] == "PERSON":
    names.append(entity_patterns[position][0].lower())
  position += 1

hello_words = ["hello"]
hello_keywords = []
bye_words = ["bye","goodbye","cya","see you","later","farewell","so long"]
bye_keywords = []
agree_words = ["exactly","yep","indeed","correct","definitely"]
agree_keywords = []
disagree_words = ["no","not","wrong"]
disagree_keywords = []
suggest_words = ["perhaps","maybe","what if"]
suggest_keywords = []
congrat_words = ["congratulations", "well done"]
congrats_keywords = []
question_words = ["what","why","who","when","where"]
question_keywords = []
#identifies various synonyms
def getSynonym(list):
  position = 0
  Synonymlist = []
  for each in list:
    for words in wordnet.synsets(list[position]):
      for lemma in words.lemmas():
        Synonymlist.append(lemma.name())
    position += 1
  Synonymlist.extend(list)
  return Synonymlist

hello_keywords = getSynonym(hello_words)
bye_keywords = getSynonym(bye_words)
agree_keywords = getSynonym(agree_words)
disagree_keywords = getSynonym(disagree_words)
suggest_keywords = getSynonym(suggest_words)
congrats_keywords = getSynonym(congrat_words)
question_keywords = getSynonym(question_words)


#Test phrases for various intents such as greeting or good bye type messages
position2 = 0
def IntentMatcher(string, intent):
  if intent == "greet":
    stringcontain = [ele for ele in names if(ele in string)] and [ele for ele in hello_keywords if(ele in string)]
    return stringcontain
  elif intent == "bye":
    stringcontain = [ele for ele in bye_keywords if(ele in string)]
    return stringcontain
  elif intent == "agree":
    stringcontain = [ele for ele in agree_keywords if(ele in string)]
    return stringcontain
  elif intent == "disagree":
    stringcontain = [ele for ele in disagree_keywords if(ele in string)]
    return stringcontain
  elif intent == "suggest":
    stringcontain = [ele for ele in suggest_keywords if(ele in string)]
    return stringcontain
  elif intent == "congrats":
    stringcontain = [ele for ele in congrats_keywords if(ele in string)]
    return stringcontain
  elif intent == "question":
    stringcontain = [ele for ele in question_keywords if(ele in string)]
    return stringcontain
  else:
    stringcontain = [ele for ele in hello_keywords if(ele in string)]
    if stringcontain: return "greet"
    stringcontain = [ele for ele in bye_keywords if(ele in string)]
    if stringcontain: return "bye"
    stringcontain = [ele for ele in question_keywords if(ele in string)]
    if stringcontain: return "question"
    stringcontain = [ele for ele in suggest_keywords if(ele in string)]
    if stringcontain: return "suggest"
    stringcontain = [ele for ele in disagree_keywords if(ele in string)]
    if stringcontain: return "disagree"
    stringcontain = [ele for ele in agree_keywords if(ele in string)]
    if stringcontain: return "agree"
    stringcontain = [ele for ele in congrats_keywords if(ele in string)]
    if stringcontain: return "congrats"
          
#Checks the text for possible greeting and good bye phrases
greetlist = []
byelist = []
position = 0
for each in txtlist:
  if IntentMatcher(txtlist[position], "greet"):
    greetlist.append(txtlist[position])
  if IntentMatcher(txtlist[position], "bye"):
    byelist.append(txtlist[position])
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


namefreq = []
position = 0
position2 = 0
for each in greetlist:
  for each in names:
    if names[position] in greetlist[position2]:
      try:
        namefreq[position] += 1
      except:
        namefreq.append(1)
    position += 1
  position2 +=1
  position = 0

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


def matchcount(string):
  try:
    count = txtcount[txtcountmatch.index(string.lower())]
  except:
    return 0
  return count


#Calculates the frequency of a word in the text
totalwords = 0
position = 0
for each in txtcount:
  totalwords += txtcount[position]
  position += 1
txtfreq = []
position = 0
for each in txtcount:
  txtfreq.append(float(txtcount[position] / totalwords))
  position += 1


lemmatxt = Lemmatize(txt).lower().split()
lemmatxt = puncremover(lemmatxt)
dupelemmatxt = lemmatxt
position = 0
#Frequency of nouns and verbs
nouncount = []
position = 0
for each in noun_lemmatized:
  nouncount.append(dupelemmatxt.count(noun_lemmatized[position].lower()))
  position += 1

while nouncount.count(0) > 0:
  position2 = nouncount.index(0)
  nouncount.pop(position2)
  noun_lemmatized.pop(position2)

position = 0
totalnoun = 0
for each in nouncount:
  totalnoun += nouncount[position]
  position += 1


nounfreq = []
position = 0
for each in nouncount:
  nounfreq.append(nouncount[position] / totalnoun)
  position += 1 


def matchncount(noun):
  try:
    count = nouncount[noun_lemmatized.index(noun.lower())]
  except:
    return 0
  return count


lemmatxt = Lemmatize(txt).lower().split()
lemmatxt = puncremover(lemmatxt)
dupelemmatxt = lemmatxt
position = 0

verbcount = []
position = 0
for each in verb_lemmatized:
  verbcount.append(dupelemmatxt.count(verb_lemmatized[position].lower()))
  position += 1

while verbcount.count(0) > 0:
  position2 = verbcount.index(0)
  verbcount.pop(position2)
  verb_lemmatized.pop(position2)

position = 0
totalverb = 0
for each in verbcount:
  totalverb += verbcount[position]
  position += 1
  

verbfreq = []
position = 0
for each in verbcount:
  verbfreq.append(verbcount[position] / totalverb)
  position += 1 


def matchvcount(verb):
  try:
    count = verbcount[verb_lemmatized.index(verb.lower())]
  except:
    return 0
  return count

position = 0
position2 = 0
name = ""
for each in namefreq:
  try:
    if namefreq[position] > namefreq[names.index(name)]:
      name = names[position]
      position2 = position
  except:
    name = names[0]
  position += 1

clear = lambda : print('\n' * 150)
clear()

print("What is your name? ")
username = input()

print("Hello " + username + ", zote ai is now ready")

while True:
  #zote response
  userinput = input().lower()
  userintent = IntentMatcher(userinput, "")
  print(userintent)