#Put text through NLP(Natural Language processing)
#Use data to train a bot/ai
#User sends message
#Message is sent throught intent detection
#bot responds with another message with a hopefully valid response for that intent
#
import random
import spacy
import language_check
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
lemmatizer = WordNetLemmatizer()
tool = language_check.LanguageTool('en-US')

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

#seperates entities such as numbers or people into a seperate list and labels them
position = 0
for entity in nlptext.ents:
  text_entity.append([entity.text])
  text_entity[position].append(entity.label_)
  position += 1

#Creates more empty list to store entity patterns
entity_patterns = []

#Entity Patterns
position = 0

#Repeats for each entity in the entity list
for entity in text_entity:
  #does the entity appear more than once?
  if text_entity.count(entity) >= 2:
    #Is it not alredly in the patterns list AND is it not a number of any type?
    if entity_patterns.count(entity) < 1 and not (entity[1] == 'ORDINAL' or entity[1] == 'CARDINAL'):
      entity_patterns.append(entity)

#Creates a dupelicate of text of a new chunked text list
txtlist = []
dupetxt = txt

#Turns the txt into a list of phrases
txtlist = open("CharacterText.txt")
txtlist = txtlist.readlines()

for sentence in txtlist:
  txtlist[txtlist.index(sentence)] = sentence.lower()

#Finds likely candidates for ai character name in the greetings it has found
names = []
position = 0
for entity in entity_patterns:
  if entity[1] == "PERSON":
    names.append(entity[0].lower())

#Creates list for keywords used in specific parts of speach
hello_words = ["hello", "greetings", "i am"]
bye_words = ["bye", "goodbye", "cya", "see you", "later", "farewell", "so long"]
agree_words = ["exactly", "yep", "indeed", "correct", "definitely", "cool", "agree", "yes"]
disagree_words = ["no", "not", "wrong", "disagree"]
suggest_words = ["perhaps", "maybe", "what if"]
congrat_words = ["congratulations", "well done", "wow", "yay", "great", "nice"]
question_words = ["what", "why", "who", "when", "where", "?", "how"]
insult_words = ["idiot", "moron", "cur", "buffoon", "knobhead", "dork", "stupid","bonehead", "dingbat", "airhead", "scum", "scumbag", "geek", "nerd","muppet"]

#Tokenizes text
tokenlist = []
dupetxt = word_tokenize(txt)
dupetxt = nltk.pos_tag(dupetxt, tagset="universal")

#Creates a list with every token, without punctuation
for token in dupetxt:
  if tokenlist.count(token) == 0 and not (token[1] == '.'):
    tokenlist.append(token)

nounlist = []
verblist = []
adverblist = []
adjectivelist = []
#Seperates Nouns, Verbs, Adverbs and Adjectives into seperate list
for token in tokenlist:
  if token[1] == 'NOUN':
    nounlist.append(token)
  if token[1] == 'VERB':
    verblist.append(token)
  if token[1] == 'ADV':
    adverblist.append(token)
  if token[1] == 'ADJ':
    adjectivelist.append(token)


#identifies various synonyms of any inserted word, then returns them in a list with the original words aswell
def getSynonym(list):
    Synonymlist = []
    for each in list:
        for words in wordnet.synsets(each):
            for lemma in words.lemmas():
                Synonymlist.append(lemma.name())
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
insult_words = getSynonym(insult_words)

#Test phrases for various intents such as greeting or good bye type messages, or returns type if not given based on priority(this is the order they appear in in the function)
def IntentMatcher(String, intent):
    if intent == "greet":
        stringcontain = [ele for ele in names if (ele in String)] and [ele for ele in hello_words if (ele in String)]
        return stringcontain
      
    elif intent == "bye":
        stringcontain = [ele for ele in bye_words if (ele in String)]
        return stringcontain
      
    elif intent == "agree":
        stringcontain = [ele for ele in agree_words if (ele in String)]
        return stringcontain
      
    elif intent == "disagree":
        stringcontain = [ele for ele in disagree_words if (ele in String)]
        return stringcontain
      
    elif intent == "suggest":
        stringcontain = [ele for ele in suggest_words if (ele in String)]
        return stringcontain
      
    elif intent == "congrat":
        stringcontain = [ele for ele in congrats_words if (ele in String)]
        return stringcontain
      
    elif intent == "question":
        stringcontain = [ele for ele in question_words if (ele in String)]
        return stringcontain
      
    elif intent == "insult":
        stringcontain = [ele for ele in insult_words if (ele in String)]

#Detects if an intent is found within the text
def IntentDetector(String):
    stringcontain = [ele for ele in hello_words if (ele in String)]
    if stringcontain: return "greet"
      
    stringcontain = [ele for ele in bye_words if (ele in String)]
    if stringcontain: return "bye"
      
    stringcontain = [ele for ele in question_words if (ele in String)]
    if stringcontain: return "question"
      
    stringcontain = [ele for ele in suggest_words if (ele in String)]
    if stringcontain: return "suggest"
      
    stringcontain = [ele for ele in disagree_words if (ele in String)]
    if stringcontain: return "disagree"
      
    stringcontain = [ele for ele in agree_words if (ele in String)]
    if stringcontain: return "agree"
      
    stringcontain = [ele for ele in congrats_words if (ele in String)]
    if stringcontain: return "congrat"
      
    stringcontain = [ele for ele in insult_words if (ele in String)]
    if stringcontain: return "insult"


greetlist = []
byelist = []
agreelist = []
disagreelist = []
questionlist = []
suggestlist = []
congratlist = []
insultlist = []
#Checks the text for possible intent phrases
for sentence in txtlist:
    if IntentMatcher(sentence, "greet"):
        greetlist.append(sentence)

    if IntentMatcher(sentence, "bye"):
        byelist.append(sentence)

    if IntentMatcher(sentence, "agree"):
        agreelist.append(sentence)

    if IntentMatcher(sentence, "disagree"):
        disagreelist.append(sentence)

    if IntentMatcher(sentence, "suggest"):
        suggestlist.append(sentence)
      
    if IntentMatcher(sentence, "question"):
        questionlist.append(sentence)

    if IntentMatcher(sentence, "congrat"):
        congratlist.append(sentence)
      
    if IntentMatcher(sentence, "insult"):
        insultlist.append(sentence)


#Gets frequency of names and inserts in new list
namefreq = []
for greet in greetlist:
  for name in names:
    if name in greet:
      try:
        namefreq[names.index(name)] += 1
      except:
        namefreq.append(1)

name = ""
#Sets the most common name to the name of the ai
for each in namefreq:
  try:
    if each > namefreq[names.index(name)]:
      name = each
  except:
    name = names[0]

#This is a lambda function to make the console appear empty
clear = lambda: print('\n' * 150)
clear()

print("Hello, Zote AI is now ready\n")


def Generate(List):
  newsentence = []
  nametoken = word_tokenize(name)
  nametoken = nltk.pos_tag(nametoken, tagset="universal")
  dupetxt = word_tokenize(List[random.randint(0, len(List) - 1)])
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
      this_is_useless = "lol"

  for each in dupetxt:
    if dupetxt.index(each) == nameposition:
      newsentence.extend(nametoken)
      newsentence.append(each)

    elif each[1] == 'NOUN':
      newsentence.append(nounlist[random.randint(0, len(nounlist) - 1)])
    elif each[1] == 'VERB':
      newsentence.append(verblist[random.randint(0, len(verblist) - 1)])
    elif each[1] == 'ADV':
      newsentence.append(adverblist[random.randint(0,len(adverblist) - 1)])
    elif each[1] == 'ADJ':
      newsentence.append(adjectivelist[random.randint(0,len(adjectivelist) - 1)])
    else:
      newsentence.append(each)

  untoken = ""
  for each in newsentence:
    if not (each[1] == '.'):
      untoken = untoken + " " + each[0].lower()
    else:
      untoken = untoken + each[0].lower()

  matches = tool.check(untoken)
  untoken = language_check.correct(untoken, matches)

  print(untoken)


while True:
  #zote response

  try:
    userinput = input().lower()
  except:
    userinput = ""
  userintent = IntentDetector(userinput)
  if userinput == "exit":
    print("Shuting down...")
    break

  if userintent == "greet" and len(greetlist) > 0:
    Generate(greetlist)
  elif userintent == "bye" and len(byelist) > 0:
    Generate(byelist)
  elif userintent == "agree" and len(agreelist) > 0:
    Generate(agreelist)
  elif userintent == "disagree" and len(disagreelist) > 0:
    Generate(disagreelist)
  elif userintent == "question" and len(questionlist) > 0:
    Generate(questionlist)
  elif userintent == "suggest" and len(suggestlist) > 0:
    Generate(suggestlist)
  elif userintent == "congrat" and len(congratlist) > 0:
    Generate(congratlist)
  elif userintent == "insult" and len(insultlist) > 0:
    Generate(insultlist)
  else:
    Generate(txtlist)
