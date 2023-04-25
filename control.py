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
    #Come back to this function
    #consider_lexical_requests() 
    check_end_np()
    activate_item_requests(Global.word)
    consider_requests()
    check_begin_np()
    word = get_next_item()

def activate_item_requests(wd):
  reqs = make_requests(wd, Global.requests.get(wd, []))
  macros.pmsg("ACTIVATE-ITEM-REQUESTS for word ", wd,": ", reqs)
  if(Global.extra_requests or reqs):
    if(Global.flagon("skip_word_flag")):
      Global.remove_flag("skip_word_flag")
    else:
      Global.extra_requests.append(reqs)
    result = build_pool(wd, Global.extra_requests)
    activate_pool(result)
    Global.extra_requests = []

def make_requests(wd, reqs=[], bindings=[]): #fix this
  if(reqs == []):
    reqs = Global.requests.get(wd, [])
  result = []
  for req in reqs: #request is generated so I guess req should already have something? debug later with lisp code
    result.append(gen_request(req, wd, bindings))
  return result

def gen_request(R, wd, bindings=[]):
  reqsym = macros.new_req(wd)
  #unsure about symbol-value R = R might be the same in python
  if(R[0] == 'request'):
    R = R[1:]
  val = clausify(R)
  Global.body[reqsym] = val
  Global.wd[reqsym] = wd
  Global.bindings[reqsym] = bindings #this is a list maybe should be a dictionary?
  for form in R:
    if form[0] == 'clause':
      break
    prop = macros.pool_req(form[0])
    prop.append(form[1:])
    macros.set_pool_reqs(form[0], prop)
  Global.active[reqsym] = True
  return reqsym



def check_end_np():
  if(Global.flagon("noun_group_flag")):
    end_noun_phrase()
    Global.remove_flag("noun_group_flag")
    macros.pmsg( "End of noun group")

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


def clean_up_request_pools(): # removes request pools which are no longer active
  clean_up_special_pools()
  for p in Global.request_pools:
    if(live_reqs(p)):
      Global.request_pools.append(p)

def save_live_reqs(pool):
  for r in Global.pool_reqs(pool):
    if not(r in Global.active): # not sure 100% on this
      Global.remove_pool_reqs(pool, r)

def live_reqs(pool):
  for r in Global.pool_reqs(pool):
    if(r in Global.active):
      return True

def clean_up_special_pools():
  save_live_reqs('lexical_pool')

def consider_lexical_requests():
  if(Global.pool_reqs('lexical_pool')):
    macros.pmsg("Considering Lexical Requests:")
    consider_pool('lexical_pool')
  else:
    consider_all_requests()


def consider_pool(pool):
  reqs = Global.pool_reqs(pool)
  t = []
  if(reqs):
    for r in reqs:
      if consider(reqs, pool): #not sure 100% on this (more certain) (this always has one item so may be easier to return true)
        t.append(True)
    return t
  else:
    return []

def consider(pool, request): #not sure on this entire function
  Global.new_con = []
  body = Global.body.get(request, [])
  tracep =  Global.tracep.get(request, []) #not 100% missing 2nd part 'tracep
  bindings = Global.bindings.get(request, [])
  if Global.active.get(request, []):
    if tracep:
      macros.pmsg("CONSIDERing active request", "body: ", body)
      macros.pmsg(" bindings:", bindings)
    for clause in body:
      res, tstbindings = eval_test(request, clause, bindings)
      if res:
        macros.pmsg(request, "has fired")
        Global.active.pop(request)
        eval_actions(request, clause, tstbindings, pool)
    if Global.active.get(request, []) == []:
      if Global.flagon('no_kill_flag'):
         Global.remove_flag('no_kill_flag')
         Global.active[request] = True
      return True
    else:
      return False

def eval_test(req, cl, bindings): #not sure on this one either
  bdgs, vars = collect_vars(cl, bindings)
  tstform = cl['test']
  bindings = bdgs
  Global.current_req = req
  res = []
  form = [bindings, Global.current_req]
  form.append(res)
  form.append(vars)
  form.append(tstform[:-1])
  res = tstform[-1]
  form.append(res) # this definitely seems wrong
  form.append(bindings)
  res = form.value
  bds = None
  return res, bds

def collect_vars(form, bindings=[]):
  foundvars = collect_vars1(form, bindings)
  res = []
  for s in foundvars:
    res.append(s[0], s[:1]) # I dont know this seems wrong unsure
  return foundvars, res


def consider_all_requests(): #(fixed uncertainty (I think?))
  if(Global.request_pools):
    #macros.pmsg("CONSIDER-ALL-REQUESTS")
    for pool in Global.request_pools:
      if consider_pool(pool).any():
        break


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




def check_begin_np():
  if(not Global.flagon("noun_group_flag")):
    Global.n_p_records = begin_noun_phrase(Global.next_word)
    Global.add_flag("noun_group_flag")
    if Global.changed_cons:
      macros.pmsg("Begin noun group:")

# def ldiff (l1 l2):
#   return list(set(l1).symmetric_difference(set(l2)))

#have some doubts on this  
def consider_latest_requests():
 #latest_pool = Global.request_pools[0]
 older_pools = Global.request_pools[1:]
 #latest_pool = ldiff(Global.request_pools, older_pools[1:])
 latest_pools = list (set(Global.request_pools).symmetric_difference.set(older_pools[1:]))
 while any(map(consider_pool, latest_pools)):
   macros.pmsg("CONSIDER-LATEST-REQUESTS latest pools:")

def consider_requests():
  if Global.flagon("noun_group_flag"):
    macros.pmsg("Considering latest requests:")
    consider_latest_requests()
  else:
    consider_all_requests()

def consider_lexical_requests():
    if Global.pool_reqs('lexical_pool'):
        macros.pmsg("Considering lexical requests:")
        consider_pool('lexical_pool')
    else:
        # macros.pmsg("No lexical reqs. Moving to consider all requests.")
        consider_all_requests()

CA('(a small twin-engine plane stuffed with marijuana crashed south of here yesterday)')