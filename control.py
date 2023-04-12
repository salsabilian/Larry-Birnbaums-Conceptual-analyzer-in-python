import Global
import macros

# lisp version stored data as a list so modifications needed
# I think we just convert to a list split at spaces

def CA(in_=[]):
  Global.changed_cons = []
  Global.current_phrase = []
  Global.current_module = ":CA"
  if(in_ and Global.input):
    Global.input = input
  elif (not(in_) or len(in_.split()) <= 1): # if we dont have a string of words
    return []
  elif not(isinstance(in_[0], list) or isinstance(in_[0], tuple)): # if we have a string of words
    Global.input = [in_] # we are creating a one item list
  elif(isinstance(in_[0], list) or isinstance(in_[0], tuple)): # if we have a list of lists
    Global.input = in_
  macros.pmsg("Current Input: ")
  macros.pmsg(Global.input)
  init_ca()
  if Global.sentence is None:
    Global.working = None
    return None
  word = get_next_item()
  while word:
    print("\n\n======================= Current Word: " + Global.word + " ==========================")
    print("Phrase: ", end="")
    print(Global.current_phrase,end="")
    print(" rest: ", end="")
    print(Global.sentence)
    clean_up_request_pools()
    word = get_next_item()

def clean_up_request_pools():
  clean_up_special_pools()
  for p in Global.request_pools:
    if(live_reqs(p)):
      Global.request_pools.append(p)

def save_live_reqs(pool):
  for r in Global.pool_reqs(pool):
    if not(r in Global.active): # not 100% on this
      Global.remove_pool_reqs(pool, r)

def live_reqs(pool):
  for r in Global.pool_reqs(pool):
    if(r in Global.active):
      return True

def clean_up_special_pools():
  save_live_reqs('lexical_pool')


def get_next_item():
  if Global.flagon("change_trace_flag"):
    Global.pause = not(Global.pause)
    Global.remove_flag("change_trace_flag")
  if(Global.sentence):
    Global.word = Global.sentence.pop(0)
  else:
    return None
  if(Global.next_word() == '*'):
    Global.add_flag("change_trace_flag")
    Global.sentence = Global.sentence[1:]
  Global.current_phrase.append(Global.word)
  return Global.word

def next_sentence():
  return Global.input.pop(0)

def init_ca():
  Global.init_ca_vars()
  Global.sentence = next_sentence()
  if(Global.sentence.find("(") != -1): # remove paranthesis
    Global.sentence = Global.sentence.replace("(","")
    Global.sentence = Global.sentence.replace(")","")
    Global.parans = 1
  Global.sentence = Global.sentence.split(" ")
  macros.pmsg("New Sentence is ")
  macros.pmsg(Global.sentence)
  Global.lexical_pool = []
  if(Global.next_word() == '*'):
    Global.add_flag("change_trace_flag")
    Global.sentence = Global.sentence[1:]
  begin_noun_phrase(Global.next_word)

def begin_noun_phrase(word=Global.next_word):
  np_req = find_pos_req(word, ['adj', 'arg', 'name', 'noun', 'num', 'poss', 'title1'])
  n_p_record = np_req
  if n_p_record:
    Global.add_flag("noun_group_flag")
    macros.pmsg("Begin noun group:")
  return np_req

def find_pos_req(lex, poslist):
  atts = Global.atts.get(lex, [])
  for x in poslist:
    if x in atts:
      atts.remove(x)
  return atts

CA('(a small twin-engine plane stuffed with marijuana crashed south of here yesterday)')