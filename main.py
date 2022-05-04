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
import random
import string
import spacy
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize
nltk.download('wordnet')
nltk.download('omw-1.4')
nltk.download('averaged_perceptron_tagger')
nltk.download('punkt')
nltk.download('universal_tagset')
nlp = spacy.load('en_core_web_sm')
grammar = "NP: {<DT>?<JJ>*<NN>}"
Parser = nltk.RegexpParser(grammar)
lemmatizer = WordNetLemmatizer()

#Creates empty list
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


#Creates more empty list to store noun and verb and entity patterns
noun_patterns = []
verb_patterns = []
entity_patterns = []

#Identify speech patterns in nouns and verbs and entitys

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
  #Create two empty list
verb_lemmatized = []
noun_lemmatized = []

#Sets posititon to 0 then iterates through list to find verbs that appear more than once, then adds one to position and does the same thing again
position = 0
for each in verb_patterns:
  if len(verb_patterns) > position:
    if verb_lemmatized.count(str.lower(lemmatizer.lemmatize(verb_patterns[position], pos = 'v'))) < 1:
      verb_lemmatized.append(str.lower(lemmatizer.lemmatize(verb_patterns[position], pos = 'v')))
  position += 1

#Sets posititon to 0 then iterates through list to find nouns that appear more than once, then adds one to position and does the same thing again
position = 0
for each in noun_patterns:
  if len(noun_patterns) > position:
    if noun_lemmatized.count(str.lower(lemmatizer.lemmatize(noun_patterns[position], pos = 'n'))) < 1:
      noun_lemmatized.append(str.lower(lemmatizer.lemmatize(noun_patterns[position], pos = 'n')))
  position += 1

print(noun_lemmatized)

#Creates a dupelicate of text of a new chunked text list
txtlist = []
dupetxt = txt
position = 0
#Turns the txt into a list of phrases
txtlist = open("CharacterText.txt")
txtlist = txtlist.readlines()
position = 0
for each in txtlist:
  txtlist[position] = txtlist[position].lower()
  position += 1
print(txtlist)

#Finds likely candidates for ai character name in the greetings it has found
names = []
position = 0
for each in entity_patterns:
  if entity_patterns[position][1] == "PERSON":
    names.append(entity_patterns[position][0].lower())
  position += 1

#Creates list for keywords used in specific parts of speach
hello_words = ["hello", "greetings", "i am"]
bye_words = ["bye","goodbye","cya","see you","later","farewell","so long"]
agree_words = ["exactly","yep","indeed","correct","definitely","cool"]
disagree_words = ["no","not","wrong"]
suggest_words = ["perhaps","maybe","what if"]
congrat_words = ["congratulations", "well done","!","wow","yay","great","nice"]
question_words = ["what","why","who","when","where","?","how"]
insult_words = ["idiot","moron","cur","buffoon","knobhead","dork","stupid","bonehead","dingbat","airhead","scum","scumbag","geek","nerd","muppet"]

tokenlist = []
dupetxt = word_tokenize(txt)
dupetxt = nltk.pos_tag(dupetxt, tagset="universal")
print(dupetxt)

position = 0
for each in dupetxt:
  if tokenlist.count(dupetxt[position]) == 0 and not (dupetxt[position][1] == '.'):
    tokenlist.append(dupetxt[position])
  position += 1
  
print(tokenlist)

position = 0
nounlist = []
verblist = []
for each in tokenlist:
  if tokenlist[position][1] == 'NOUN':
    nounlist.append(tokenlist[position])
  if tokenlist[position][1] == 'VERB':
    verblist.append(tokenlist[position])
  position += 1

print(nounlist)
print(verblist)
#identifies various synonyms of any inserted word, then returns them in a list with the original words aswell
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

#Adds synonyms of known key words to key word list to increase the abilities of searching for these types of text
hello_words = getSynonym(hello_words)
bye_words = getSynonym(bye_words)
agree_words = getSynonym(agree_words)
disagree_words = getSynonym(disagree_words)
suggest_words = getSynonym(suggest_words)
congrats_words = getSynonym(congrat_words)
question_words = getSynonym(question_words)


#Test phrases for various intents such as greeting or good bye type messages, or returns type if not given based on priority(this is the order they appear in in the function)
position2 = 0
def IntentMatcher(string, intent):
  if intent == "greet":
    stringcontain = [ele for ele in names if(ele in string)] and [ele for ele in hello_words if(ele in string)]
    return stringcontain
  elif intent == "bye":
    stringcontain = [ele for ele in bye_words if(ele in string)]
    return stringcontain
  elif intent == "agree":
    stringcontain = [ele for ele in agree_words if(ele in string)]
    return stringcontain
  elif intent == "disagree":
    stringcontain = [ele for ele in disagree_words if(ele in string)]
    return stringcontain
  elif intent == "suggest":
    stringcontain = [ele for ele in suggest_words if(ele in string)]
    return stringcontain
  elif intent == "congrat":
    stringcontain = [ele for ele in congrats_words if(ele in string)]
    return stringcontain
  elif intent == "question":
    stringcontain = [ele for ele in question_words if(ele in string)]
    return stringcontain
  elif intent == "insult":
    stringcontain = [ele for ele in insult_words if(ele in string)]
  else:
    stringcontain = [ele for ele in hello_words if(ele in string)]
    if stringcontain: return "greet"
    stringcontain = [ele for ele in bye_words if(ele in string)]
    if stringcontain: return "bye"
    stringcontain = [ele for ele in question_words if(ele in string)]
    if stringcontain: return "question"
    stringcontain = [ele for ele in suggest_words if(ele in string)]
    if stringcontain: return "suggest"
    stringcontain = [ele for ele in disagree_words if(ele in string)]
    if stringcontain: return "disagree"
    stringcontain = [ele for ele in agree_words if(ele in string)]
    if stringcontain: return "agree"
    stringcontain = [ele for ele in congrats_words if(ele in string)]
    if stringcontain: return "congrat"

#Checks the text for possible intent phrases
greetlist = []
byelist = []
agreelist = []
disagreelist = []
questionlist = []
suggestlist = []
congratlist = []
position = 0
for each in txtlist:
  if IntentMatcher(txtlist[position], "greet"):
    greetlist.append(txtlist[position])
    
  if IntentMatcher(txtlist[position], "bye"):
    byelist.append(txtlist[position])
    
  if IntentMatcher(txtlist[position], "agree"):
    agreelist.append(txtlist[position])
    
  if IntentMatcher(txtlist[position], "disagree"):
    disagreelist.append(txtlist[position])
    
  if IntentMatcher(txtlist[position], "suggest"):
    suggestlist.append(txtlist[position])
    
  if IntentMatcher(txtlist[position], "question"):
    questionlist.append(txtlist[position])
    
  if IntentMatcher(txtlist[position], "congrat"):
    congratlist.append(txtlist[position])
  position += 1

#Removes '\n' from the test lists inserted into the function
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

#Creates new list and set postion 1 & 2 to 0
namefreq = []
position = 0
position2 = 0
#Gets frequency of names and inserts in new list
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

#Remove all puntuation from inserted list
def puncremover(list):
  position = 0
  newlist = []
  for each in list:
    newlist.append(list[position].translate(str.maketrans('', '', string.punctuation)))
    position += 1
  return newlist

#Lemmatizes string inserted
def Lemmatize(string):
  lemmatizedstring = ''
  lemmatizedstring += str.lower(lemmatizer.lemmatize(string, pos = 'n'))
  lemmatizedstring += str.lower(lemmatizer.lemmatize(string, pos = 'v'))
  lemmatizedstring += str.lower(lemmatizer.lemmatize(string, pos = 'a'))
  lemmatizedstring += str.lower(lemmatizer.lemmatize(string, pos = 'r'))
  lemmatizedstring += str.lower(lemmatizer.lemmatize(string, pos = 's'))
  return string

#Turns the text into a list of numbers based on how many times they appear, and puts it into two new list
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

#
def matchcount(string):
  try:
    count = txtcount[txtcountmatch.index(string.lower())]
  except:
    return 0
  return count


#Calculates the frequency of a word in the text(amount of word in text / total words)
totalwords = 0
position = 0
#Counts total words
for each in txtcount:
  totalwords += txtcount[position]
  position += 1

#Creates a new list with the count of each word turned into a frequency
txtfreq = []
position = 0
for each in txtcount:
  txtfreq.append(float(txtcount[position] / totalwords))
  position += 1

#Creates a lemmatized verions of the entire text, then removes punctuatuion
lemmatxt = Lemmatize(txt).lower().split()
lemmatxt = puncremover(lemmatxt)
dupelemmatxt = lemmatxt
position = 0
#Frequency of nouns and verbs
#Counts number of times a noun is in text
nouncount = []
position = 0
for each in noun_lemmatized:
  nouncount.append(dupelemmatxt.count(noun_lemmatized[position].lower()))
  position += 1
#If the noun is not found(returns 0) in lemmatized text it is removed
while nouncount.count(0) > 0:
  position2 = nouncount.index(0)
  nouncount.pop(position2)
  noun_lemmatized.pop(position2)

#Counts the total amount of nouns
position = 0
totalnoun = 0
for each in nouncount:
  totalnoun += nouncount[position]
  position += 1

#Divides amount of time a noun is in text by the total to get frequency, puts into new list
nounfreq = []
position = 0
for each in nouncount:
  nounfreq.append(nouncount[position] / totalnoun)
  position += 1 

#Creates a function that returns the amount of times a noun is in the text
def matchncount(noun):
  try:
    count = nouncount[noun_lemmatized.index(noun.lower())]
  except:
    return 0
  return count

#Counts the amount of times a verb appears in the text
verbcount = []
position = 0
for each in verb_lemmatized:
  verbcount.append(dupelemmatxt.count(verb_lemmatized[position].lower()))
  position += 1
#Remove verbs that did not appear in the lemmatized list
while verbcount.count(0) > 0:
  position2 = verbcount.index(0)
  verbcount.pop(position2)
  verb_lemmatized.pop(position2)

position = 0
totalverb = 0
#Counts the total amount of verbs
for each in verbcount:
  totalverb += verbcount[position]
  position += 1

#Divides amount of time a noun is in text by the total to get frequency, puts into new list
verbfreq = []
position = 0
for each in verbcount:
  verbfreq.append(verbcount[position] / totalverb)
  position += 1 

#Creates a function that returns the amount of times a verb is in the text
def matchvcount(verb):
  try:
    count = verbcount[verb_lemmatized.index(verb.lower())]
  except:
    return 0
  return count

position = 0
position2 = 0
name = ""
#Sets the most common name to the name of the ai
for each in namefreq:
  try:
    if namefreq[position] > namefreq[names.index(name)]:
      name = names[position]
      position2 = position
  except:
    name = names[0]
  position += 1

#This is a lambda function to make the console appear empty
clear = lambda : print('\n' * 150)
clear()

#This is how the bot generates a greeting
def Greeting():
  position = 0
  tokenisedlist = []
  for each in greetlist:
    tokenisedlist.append(word_tokenize(greetlist[position]))
    position += 1
  structurelist = []
  structurelist.append(nltk.pos_tag(tokenisedlist))
  
  greettext = ""  
  return greettext

print("What is your name? ")
username = input()

print("Hello " + username + ", Zote AI is now ready")

while True:
  #zote response
  
  try:
    userinput = input().lower()
  except:
    userinput = ""
  userintent = IntentMatcher(userinput, "")
  if userinput == "exit":
    print("Shuting down...")
    break
    
  if userintent == "greet" and len(greetlist) > 0:
    nametoken = word_tokenize(name)
    nametoken = nltk.pos_tag(nametoken, tagset="universal")
    dupetxt = word_tokenize(greetlist[random.randint(0, len(greetlist) - 1)])
    dupetxt = nltk.pos_tag(dupetxt, tagset="universal")

    try:
      dupetxt.index(nametoken[1])
      nameposition = dupetxt.index(nametoken[1])
    except: 
      nameposition = "N/A"
    for each in nametoken:
      try:
        dupetxt.pop(dupetxt.index(each))
      except:
        position += 1

    print(nameposition)
    print(nametoken)
    print(dupetxt)
    print(greetlist[random.randint(0, len(greetlist) - 1)])
    
  if userintent == "bye" and len(byelist) > 0:
    print(byelist[random.randint(0, len(byelist) - 1)])
    
  if userintent == "agree" and len(agreelist) > 0:
    print(agreelist[random.randint(0, len(agreelist) - 1)])
    
  if userintent == "disagree" and len(disagreelist) > 0:
    print(disagreelist[random.randint(0, len(disagreelist) - 1)])
    
  if userintent == "question" and len(questionlist) > 0:
    print(questionlist[random.randint(0, len(questionlist) - 1)])
    
  if userintent == "suggest" and len(suggestlist) > 0:
    print(suggestlist[random.randint(0, len(suggestlist) - 1)])
    
  if userintent == "congrat" and len(congratlist) > 0:
    print(congratlist[random.randint(0, len(congratlist) - 1)])