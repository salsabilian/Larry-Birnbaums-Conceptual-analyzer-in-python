import Global
import macros
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
    #Come back to this function
    #consider_lexical_requests() 
    check_end_np()
    activate_item_requests(Global.word)
    consider_requests()
    check_begin_np()
    word = get_next_item()

def check_end_np():
  if(Global.flagon("noun_group_flag")):
    end_noun_phrase()
    Global.remove_flag("noun_group_flag")
    macros.pmsg( "End of noun group")


def check_begin_np():
  if(not Global.flagon("noun_group_flag")):
    Global.n_p_records = begin_noun_phrase(Global.next_word)
    Global.add_flag("noun_group_flag")
    if Global.changed_cons:
      macros.pmsg("Begin noun group:")


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


#FILL CODE HERE
def get_lex_info(word):
  newlex = macros.new_lex(word)
  if not word.get(Global.requests.get(word)):
    #can't find function anywhere
    look_up(word)
  Global.word[newlex] = word
  #unsure abt this: (setf (get newlex :reqs)            ; :pool) 
  Global.requests[newlex] = "pool"
  Global.build_pool(word , Global.make_requests(word, Global.requests[word]))

  
  




def activate_item_requests(wd):
  reqs = make_requests(wd, Global.find_class(wd).requests)
  macros.pmsg("ACTIVATE-ITEM-REQUESTS for word ", wd,": ", reqs)
  if(Global.find_class(wd).extra_requests or reqs):
    if(Global.flagon("skip_word_flag")):
      Global.remove_flag("skip_word_flag")
    else:
      if(Global.find_class(wd).extra_requests):
        Global.find_class(wd).extra_requests.append(reqs)
      else:
        Global.find_class(wd).extra_requests = reqs
    result = build_pool(wd, Global.find_class(wd).extra_requests)
    activate_pool(result)
    Global.find_class(wd).extra_requests = []


def init_ca():
  Global.init_ca_vars()
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
  begin_noun_phrase(Global.next_word)


def begin_noun_phrase(word=Global.next_word):
  np_req = find_pos_req(word, ['adj', 'arg', 'name', 'noun', 'num', 'poss', 'title1'])
  n_p_record = np_req
  if n_p_record:
    Global.add_flag("noun_group_flag")
    macros.pmsg("Begin noun group:")
  return np_req


#FILL CODE HERE
def put_first(req, pool):
  Global.pool_reqs(pool)
  for k,v in Global.pool_reqs(pool).items():
    if v == pool:
      del Global.pool_reqs(pool)[k]
      break
  res = (req,  Global.pool_reqs(pool))
  pool['pool-reqs'] = res




def find_pos_req(lex, poslist):
  atts = Global.atts.get(lex, [])
  for x in poslist:
    if x in atts:
      atts.remove(x)
  return atts


#FILL CODE HERE, unsure abt this
def get_pos(req):
  for k,v in req:
    if k == 'pos':
      return req[v][1]
  return None

def end_noun_phrase():
  atts = begin_noun_phrase(Global.next_word())
  if(atts and (("art" in Global.atts and not Global.n_p_record) or
               ("adj" in Global.atts and "num" in Global.atts and not("noun" in Global.n_p_record) and not("title" in Global.n_p_record) and not("name" in Global.n_p_record)) or
               ("title" in Global.atts and "noun" in Global.atts and not("name" in Global.n_p_record)) or
               ("name" in Global.atts and not("noun" in Global.n_p_record)))):
    Global.n_p_record = Global.atts + list(set(Global.n_p_record) - set(Global.atts)) # not sure about this got it from here: https://stackoverflow.com/questions/1319338/combining-two-lists-and-removing-duplicates-without-removing-duplicates-in-orig
    return False
  else:
    Global.n_p_record = []
    Global.remove_flag("noun_group_flag")
    return True


def clean_up_request_pools():
  clean_up_special_pools()
  for p in Global.request_pools:
    if(live_reqs(p)):
      Global.request_pools.append(p)


def live_reqs(pool):
  for r in Global.pool_reqs(pool):
    if(r in Global.find_class(Global.word).active):
      return True
    
def save_live_reqs(pool):
  for r in Global.pool_reqs(pool):
    if not(r in Global.find_class(Global.word).active):
      Global.remove_pool_reqs(pool, r)


def clean_up_special_pools():
  save_live_reqs('lexical_pool')

def consider_lexical_requests():
  if(Global.pool_reqs('lexical_pool')):
    macros.pmsg("Considering Lexical Requests:")
    consider_pool('lexical_pool')
  else:
    consider_all_requests()


def consider_requests():
  if Global.flagon("noun_group_flag"):
    macros.pmsg("Considering latest requests:")
    consider_latest_requests()
  else:
    consider_all_requests()

def consider_pool(pool):
  reqs = Global.pool_reqs(pool)
  t = []
  if(reqs):
    for req in reqs:
      if consider(req, pool): #not sure 100% on this (more certain) (this always has one item so may be easier to return true)
        t.append(True)
    return t
  else:
    return []


def consider_all_requests():
  if Global.request_pools:
    while any(consider_pool(pool) for pool in Global.request_pools):
      pass



def consider_latest_requests():
 #latest_pool = Global.request_pools[0]
 older_pools = Global.request_pools[1:]
 #latest_pool = ldiff(Global.request_pools, older_pools[1:])
 latest_pools = list (set(Global.request_pools).symmetric_difference.set(older_pools[1:]))
 while any(map(consider_pool, latest_pools)):
   macros.pmsg("CONSIDER-LATEST-REQUESTS latest pools:")


#def collect_vars1(form, bindings = []): #parse the strings for := and find variables
#  if not isinstance(form, list) and not isinstance(form, tuple): #if its not a list something is deeply wrong
#    return None
#  if form[0].find(':=') != -1: #if theres no := theres no bindings
#    idx = [i for i in range(len(form[0])) if form[0].startswith(':=', i)] #
#    for i in idx:
#      comma = form[0][i+3:].find(',')
#      bindings.append([form[0][i+3:i+3+comma]]) #dont forget double brackets here
#  else:
#    bindings = merge_blists(collect_vars1(form[1:])) #recursively go through all the strings
#  return bindings

#FILL CODE HERE
#def collect_vars1(form, bindings = []): #parse the strings for variable bindings stored as function parameters inside
#  if not isinstance(form, list) and not isinstance(form, tuple): #if its not a list something is deeply wrong
#    return None
#  for x in form: #run through the form list
#    str = "actions_" + Global.word
#    if x.find(str) != -1: #if theres no function call theres no bindings
#     funcidx = x.find(str)
#     funcidx = funcidx + 8 + len(Global.word)
#     idx = [i for i in range(len(x)) if x.startswith(',', i)] # get all the idx values
#     for i in idx:
#      bindings.append(x[funcidx+1:i])
#      funcidx = i
#      bindings = merge_blists(bindings) #remove any duplicates
#     if(x[funcidx:].find(')') != -1):
#       idx = x[:funcidx].find(')')
#       bindings.append(x[funcidx+1:idx-1])
#       bindings = merge_blists(bindings) # remove any duplicates
#  return bindings

def collect_vars1(form,bindings = []):
  str = "crash_dic.bindings_" + Global.word + "()"
  bindings = eval(str)
  return bindings
  




#FILL CODE HERE
def merge_blists(b): #remove duplicates in the lists of vars
  temp_bindings = []
  for i in b:
    if i not in temp_bindings:
      temp_bindings.append(i)
  b = temp_bindings
  return b

def collect_vars(form, bindings=[]):
  foundvars = collect_vars1(form, bindings)
  res = {}
  for s in foundvars:
    wd = Global.find_class(Global.word)
    res[s] = getattr(wd, s)
  return foundvars, res




#FILL CODE HERE
def bind(var, val):
  globals()[var] = val


#FILL CODE HERE
def bindings_as_letvars(bndgs):
  pass

def eval_test(req, cl, bindings):
  bdgs, vars = collect_vars(cl, bindings)
  tstform = cl[0].replace("test", "")
  bindings = bdgs #need to set global bindings at some point
  Global.current_req = req
  res = tstform
  Global.bindings = bindings
  res = eval(tstform) #bds is done in eval in original but we can set them using a assign function call if needed
  bds = bindings
  return res, bds



#FILL CODE HERE
def eval_actions(req, cl, bindings, pool):
  bdgs,vars = collect_vars(cl, bindings)
  idx = cl[1].find("actions") #index 1 because crash-dic is split into [(request),clause,actions]
  act_list = cl[1][idx+7:] #length of word actions
  bvars = bindings_as_letvars(bindings)
  act_vars = collect_vars([act_list], bindings)
  
  Global.bindings = bdgs
  Global.current_req = req
  Global.current_pool = pool
  
  return eval(act_list)

  



def consider(request,pool): #not sure on this entire function
  Global.new_con = []
  req = Global.find_class(request)
  body = req.body
  tracep =  req.tracep
  bindings = req.bindings
  if req.active:
    if tracep:
      macros.pmsg("CONSIDERing active request", "body: ", body)
      macros.pmsg(" bindings:", bindings)
    #for clause in body: # this didnt work anyway in the original code
    res, tstbindings = eval_test(request, body, bindings)
    if res:
      macros.pmsg(request, "has fired", "\n")
      req.active = None
      eval_actions(request, body, tstbindings, pool)
    if not req.active:
      if Global.flagon('no_kill_flag'):
         Global.remove_flag('no_kill_flag')
         req.active = True
      return True
    else:
      return False


def next_sentence():
  return Global.input.pop(0)




#Fill CODE HERE
def skip_next_word():
  Global.add_flag("skip_word_flag")


#FILL CODE HERE
def build_pool(wd, new_requests):
  pool = macros.new_pool(wd)
  p = Global.create_pool(pool)
  for req in new_requests:
    if(Global.pool_reqs(p)):
      Global.set_pool_reqs(p, [req, Global.pool_reqs(p)])
    else:
      Global.set_pool_reqs(p, [req])
  return pool

#FILL CODE HERE
def activate_pool(pool):
  if pool not in Global.request_pools:
    Global.request_pools.insert(0, pool)
  return Global.request_pools

def make_requests(wd, reqs=[], bindings=[]):
  if(reqs == []):
    reqs = [Global.find_class(wd).requests]
  result = []
  for req in reqs:
    result.append(gen_request(req, wd, bindings))
  return result

def gen_request(R, wd, bindings=[]):
  reqname = macros.new_req(wd)
  reqsym = Global.create_req(reqname)
  #unsure about symbol-value R = R might be the same in python
  if R[0] == "request":
    R = R[1:]
  val = clausify(R)
  reqsym.body = val
  reqsym.word = wd
  reqsym.bindings= bindings #this is a list maybe should be a dictionary?
  #removing form loop stuff for now if needed will come back
  #for form in R:
  #  if form[0] == 'clause':
  #    break
  #  prop = macros.pool_reqs(form[0])
  #  macros.set_pool_reqs(form[0], prop)
  reqsym.active = True
  return reqname


#FILL CODE HERE

#the lisp version uses R instead of r, wondering why
def clausify(r):
  if r[0] == 'request':
    r = r[1:]
  if r[0].find("clause") != -1:
    r[0] = r[0].replace("clause","")
  return r
      
      

# def ldiff (l1 l2):
#   return list(set(l1).symmetric_difference(set(l2)))

#have some doubts on this  




def consider_lexical_requests():
    if Global.pool_reqs('lexical_pool'):
        macros.pmsg("Considering lexical requests:")
        consider_pool('lexical_pool')
    else:
        # macros.pmsg("No lexical reqs. Moving to consider all requests.")
        consider_all_requests()
