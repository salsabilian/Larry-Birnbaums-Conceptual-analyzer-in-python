import Global
import macros
import concept_fns
import crash_dic

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
  if Global.sentence is None: #if we dont have a system just return cause somethings wrong
    Global.working = None
    return None
  word = get_next_item() #get the first word
  while word:
    print("\n\n======================= Current Word: " + Global.word + " ==========================")
    print("Phrase: ", end="")
    print(Global.current_phrase,end="")
    print(" rest: ", end="")
    print(Global.sentence)
    clean_up_request_pools()
    #Come back to this function
    #consider_lexical_requests() 
    check_end_np()  #check to see if the word is the end of a noun phrase
    activate_item_requests(Global.word) #create a request for the specific word
    consider_requests() #evaluate the request
    check_begin_np() # check to see if the word is the beginning of the noun phrase
    word = get_next_item() # get the next word

def check_end_np():
  if(Global.flagon("noun_group_flag") and end_noun_phrase()):
    Global.remove_flag("noun_group_flag") #get rid of the noun flag if were at the end of the noun phrase
    print( "End of noun group")


def check_begin_np():
  if(not Global.flagon("noun_group_flag")):
    Global.n_p_records = begin_noun_phrase(Global.next_word()) #check to see if the next word is part of a noun phrase
    if(Global.n_p_records): #if we return a value then we know it is a noun_phrase
      Global.add_flag("noun_group_flag") #so add the flag
      if Global.changed_cons: #if we have a con which we should if we've processed any words print a 2nd begin noun group
        print("Begin noun group;")


def get_next_item():
  if Global.flagon("change_trace_flag"): #this stuff is about trace and I dont really understand it but its in the lisp code
    Global.pause = not(Global.pause)
    Global.remove_flag("change_trace_flag")
  if(Global.sentence):
    Global.word = Global.sentence.pop(0) # get the next word in the sentence
    if(Global.word == "twin-engine"): #change twin-engine to an underscore cause python cant handle hyphens
      Global.word = "twin_engine"
  else: #if were out of words return none
    return None
  if(Global.next_word() == '*'):
    Global.add_flag("change_trace_flag")
    Global.sentence = Global.sentence[1:]
  Global.current_phrase.append(Global.word)
  return Global.word

#This function is incorrect and not used but it would be part of consider lexical_request
def get_lex_info(word): #we never
  newlex = macros.new_lex(word)
  if not word.get(Global.requests.get(word)):
    #can't find function anywhere
    look_up(word)
  Global.word[newlex] = word
  #unsure abt this: (setf (get newlex :reqs)            ; :pool)
  Global.requests[newlex] = "pool"
  Global.build_pool(word , Global.make_requests(word, Global.requests[word]))

def activate_item_requests(wd):
  reqs = make_requests(wd, Global.find_class(wd).requests) #create a request based on the request content of the word
  macros.pmsg("ACTIVATE-ITEM-REQUESTS for word ", wd,": ", reqs)
  if(Global.find_class(wd).extra_requests or reqs): #if we have extra requests or a request (we always should have one of these set)
    if(Global.flagon("skip_word_flag")): #if skip_word_flag is on then remove the flag and return back up to the next word
      Global.remove_flag("skip_word_flag")
    else:
      if(Global.find_class(wd).extra_requests): #otherwise add the new request to extra_requests
        Global.find_class(wd).extra_requests.append(reqs)
      else:
        Global.find_class(wd).extra_requests = reqs
    result = build_pool(wd, Global.find_class(wd).extra_requests) #afterwords build the pool for the request (each word will have a pool of requests)
    activate_pool(result) #activate the pool
    Global.find_class(wd).extra_requests = [] #clear the rest of the requests


def init_ca(): #general code for starting our programs with default values and handle the potential for there being paranthesis
  Global.init_ca_vars() #at the start and end of the sentence
  Global.sentence = next_sentence()
  if(Global.sentence.find("(") != -1): # remove parenthesis
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
  begin_noun_phrase(Global.next_word())


def begin_noun_phrase(word=Global.next_word()):
  np_req = find_pos_req(word, ['adj', 'arg', 'name', 'noun', 'num', 'poss', 'title1']) #check if the word has one of these attributes
  n_p_record = np_req #if it does set n_p_record to it
  if n_p_record: #if one attribute matches we have a noun group
    Global.add_flag("noun_group_flag")
    print("Begin noun group:")
  return np_req


#this function is incomplete and not used in our code I believe its used in consider lexical requests
def put_first(req, pool):
  Global.pool_reqs(pool)
  for k,v in Global.pool_reqs(pool).items():
    if v == pool:
      del Global.pool_reqs(pool)[k]
      break
  res = (req,  Global.pool_reqs(pool))
  pool['pool-reqs'] = res




def find_pos_req(lex, poslist): #find if any word is in attribute in the attribute list if it does return it
  atts = Global.find_class(lex).atts
  for x in atts:
    if x not in poslist:
      atts.remove(x)
  return atts


#this function is not complete and not currently used
def get_pos(req):
  for k,v in req:
    if k == 'pos':
      return req[v][1]
  return None

def end_noun_phrase():
  atts = begin_noun_phrase(Global.next_word()) #see if any attribute matches atts
  if(atts and (("art" in atts and not Global.n_p_record) or
               (("adj" in atts or "num" in atts) and (not("noun" in Global.n_p_record) or not("title" in Global.n_p_record) or not("name" in Global.n_p_record)) or
               ("title" in atts or "noun" in atts and not("name" in Global.n_p_record)) or
               ("name" in atts and not("noun" in Global.n_p_record))))): #if any of these conditionals match its not the end of the noun_phrase
    Global.n_p_record = list(set(atts) | set(Global.n_p_records))
    return False
  else: #otherwise remove the noun_group_flag
    Global.n_p_record = []
    Global.remove_flag("noun_group_flag")
    return True


def clean_up_request_pools(): #clears non-active request
  clean_up_special_pools() #clears lexical non-active requests
  temp = []
  for p in Global.request_pools: #run through all request_pools
    if(live_reqs(p)): #leave only the live ones
      temp.append(p)
  Global.request_pools = temp


def live_reqs(pool): #checks the active flag
  for r in Global.pool_reqs(pool): #if any request in the pool has an active flag keep it
    if(Global.find_class(r).active):
      return True
    
def save_live_reqs(pool):
  for r in Global.pool_reqs(pool): #do the same with lexical_pools
    if not(Global.find_class(r).active):
      Global.remove_pool_reqs(pool, r)


def clean_up_special_pools(): #check lexical_pools
  save_live_reqs('lexical_pool')

#this function is not currently used and maybe incorrect
def consider_lexical_requests():
  if(Global.pool_reqs('lexical_pool')):
    macros.pmsg("Considering Lexical Requests:")
    consider_pool('lexical_pool')
  else:
    consider_all_requests()


def consider_requests():
  if Global.flagon("noun_group_flag"):
    consider_latest_requests()
  else:
    consider_all_requests()

def consider_pool(pool):
  reqs = Global.pool_reqs(pool) #get the requests assigned to a pool
  t = []
  if(reqs):
    for req in reqs: #run through all of them and consider there requests
      if consider(req, pool):
        t.append(True)
    return t
  else:
    return []


def consider_all_requests():
  if Global.request_pools:
    while any(consider_pool(pool) for pool in Global.request_pools): #if any request is true keep running through the global
      pass #request pools


#combines request_pool and older_pools in such a way to only get latest requests
def consider_latest_requests():
 older_pools = Global.request_pools[1:]
 while any(consider_pool(pool) for pool in ldiff(Global.request_pools, older_pools[1:])):
   pass

def ldiff(request_pools, older_pools): #runs through and only gets requests not in older_pool
  temp = []
  for pool in request_pools:
    if(pool not in older_pools):
      temp.append(pool)
  return temp

#pull the bindings from crash_dic()
def collect_vars1(form,bindings = []):
  str = "crash_dic.bindings_" + Global.word + "()"
  bindings = eval(str)
  return bindings

#FILL CODE HERE, we dont use this
def merge_blists(b): #remove duplicates in the lists of vars
  temp_bindings = []
  for i in b:
    if i not in temp_bindings:
      temp_bindings.append(i)
  b = temp_bindings
  return b

#return a list of str bindings and there values
def collect_vars(form, bindings=[]):
  foundvars = collect_vars1(form, bindings)
  res = {}
  for s in foundvars:
    wd = Global.find_class(Global.word)
    res[s] = getattr(wd, s)
  return foundvars, res




#FILL CODE HERE,not used
def bind(var, val):
  globals()[var] = val


#FILL CODE HERE, not used
def bindings_as_letvars(bndgs):
  pass

def eval_test(req, cl, bindings): #checks the conditional at the start of the request
  bdgs, vars = collect_vars(cl, bindings)
  tstform = cl[0].replace("test", "") #removes the word test
  bindings = bdgs #need to set global bindings at some point
  Global.current_req = req #set the request to the current request
  res = tstform
  Global.bindings = bindings
  res = eval(tstform) #evaluate the conditional inside crash_dic
  bds = bindings
  return res, bds #return the bindings and result of conditional

def eval_actions(req, cl, bindings, pool): #achieves the action described in crash_dic request if the conditional is true
  bdgs,vars = collect_vars(cl, bindings)
  idx = cl[1].find("actions") #index 1 because crash-dic is split into [(request),clause,actions]
  act_list = cl[1][idx+7:] #length of word actions
  bvars = bindings_as_letvars(bindings) #currently does nothing
  act_vars = collect_vars([act_list], bindings) #get the values in bindings and act_list
  Global.bindings = bdgs
  Global.current_req = req #set the current_req and pool
  Global.current_pool = pool
  return eval(act_list)  #evaluate the action since the conditional was true specified in crash_dic

def consider(request,pool): #considers the conditional and the actions of the request
  Global.new_con = []
  req = Global.find_class(request) #get the request info
  body = req.body
  tracep =  req.tracep
  bindings = req.bindings
  if req.active: #check if the active flag is set if its not we do nothing cause its an old request
    if tracep:
      macros.pmsg("CONSIDERing active request", "body: ", body)
      macros.pmsg(" bindings:", bindings)
    #for clause in body: # this didnt work anyway in the original code
    res, tstbindings = eval_test(request, body, bindings) #evalue the conditional
    if res: #if we return a true
      macros.pmsg(request, "has fired", "\n") #disable the flag and do the action
      req.active = None
      eval_actions(request, body, tstbindings, pool)
    if not req.active: #if the flag is not active we have completed this request and return true
      if Global.flagon('no_kill_flag'): #if the no_kill_flag is set run the request again
         Global.remove_flag('no_kill_flag')
         req.active = True
      return True
    else: #a false means the conditional returned false
      return False

def next_sentence(): #get the first value in the sentence each time
  return Global.input.pop(0)

#Fill CODE HERE, not currently used
def skip_next_word():
  Global.add_flag("skip_word_flag")

def build_pool(wd, new_requests): #create a new pool and place all the requests in new_requests in there
  pool = macros.new_pool(wd)
  p = Global.create_pool(pool)
  for req in new_requests:
    if(Global.pool_reqs(p)):
      Global.set_pool_reqs(p, Global.pool_reqs(p).insert(0, req))
    else:
      Global.set_pool_reqs(p, [req])
  return pool


def activate_pool(pool): #place the pool on the global request pool if its not already there
  if pool not in Global.request_pools:
    Global.request_pools.insert(0, pool)
  return Global.request_pools

def make_requests(wd, reqs=[], bindings=[]):  #get the request
  if(reqs == []):
    reqs = [Global.find_class(wd).requests]
  result = []
  for req in reqs: #run through them and generate requests for them
    result.append(gen_request(req, wd, bindings))
  return result

def gen_request(R, wd, bindings=[]): #generate new_requests
  reqname = macros.new_req(wd)
  reqsym = Global.create_req(reqname)
  #unsure about symbol-value R = R might be the same in python
  if R[0] == "request": #remove the start so we only have the conditional and the actions
    R = R[1:]
  val = clausify(R)
  reqsym.body = val #set the body, bindings, and word for the request
  reqsym.word = wd
  reqsym.bindings= bindings #this is a list maybe should be a dictionary?
  #removing form loop stuff for now if needed will come back
  #for form in R:
  #  if form[0] == 'clause':
  #    break
  #  prop = macros.pool_reqs(form[0])
  #  macros.set_pool_reqs(form[0], prop)
  reqsym.active = True #finally set its active flag to true
  return reqname #return our new requests

#get rid of the request and clause word from our request
def clausify(r):
  if r[0] == 'request':
    r = r[1:]
  if r[0].find("clause") != -1:
    r[0] = r[0].replace("clause","")
  return r
