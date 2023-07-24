#macros.py
import Global

#(defparameter *pmsg-flags* T) ;; show all msgs if T, else a list of keywords

pmsg_flags = True #lets us know if we are printing pmsgs or not


def new_con(): #creates a unique name for each con and inserts it into our cons list these are then declared as class instances
    Global.uniqueid = Global.uniqueid + 1
    request = "CON"+ str(Global.uniqueid)
    Global.all_cons.insert(0, request)
    return Global.all_cons[0]


def new_lex(word): #we havent done this yet but probably similar pattern
    pass

def new_req(wd): #creates a unique name for each req and inserts it into our reqs list these are then declared as class instances
    Global.uniqueid = Global.uniqueid + 1
    request = "REQ-" + wd + "-" + str(Global.uniqueid)
    Global.all_reqs.insert(0, request)
    return Global.all_reqs[0]

def new_pool(word): #creates a unique name for each pool and inserts it into our cons list these are then declared as class instances
    Global.uniqueid = Global.uniqueid + 1
    pool = "POOL-" + word + "-" + str(Global.uniqueid)
    Global.all_pools.insert(0, pool)
    return Global.all_pools[0]

#these are not used and probably dont need to be used anymore
def putprop(sym, val, key):
    pass

def neq(arg1, arg2):
    pass

#these are used for printing they arent really used anymore but the basic idea is to print the info if pmsg_flags is set
# whether its a list of items or not
def pmsg(*args):
    if(pmsg_flags) and (pmsg_flags or args[0] == True or args[0] == pmsg_flags):
        pmsg1(*args)

def pmsg1(*args):
    nl = True
    for arg in args:
        if(not(nl)):
            print(" ", end="")
        nl = None
        if(arg == True):
            nl = True
            print()
        elif(isinstance(arg, str)):
            print(arg, end="")
        else: # in lisp this would have additional formatting to let us know its a list (but python automatically does that)
            print(arg)

trace_reqs = []
#these are also not used but most likely for debugging using trace
def trace_reqs(*reqs):
    for wd in reqs:
        if wd not in trace_reqs: # pushnew checks whether element is there in the list and if not then prepends it to the list
            trace_reqs.insert(0, wd)
#this is also not used
def untrace_reqs(*reqs):
    if (reqs == None):
        trace_reqs = []
    else:
        for r in reqs:
            trace_reqs = trace_reqs.remove(r)

#this is not used and theres a version in global so can probably be deleted
def pool_reqs(pool):
  pass

#not sure what this is used for
def props(s):
    pass
