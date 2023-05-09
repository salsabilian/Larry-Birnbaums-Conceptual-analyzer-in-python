#macros.py
import Global

#(defparameter *pmsg-flags* T) ;; show all msgs if T, else a list of keywords

pmsg_flags = True


def new_con():
    Global.uniqueid = Global.uniqueid + 1
    request = "CON"+ str(Global.uniqueid)
    Global.all_cons.insert(0, request)
    return Global.all_cons[0]


def new_lex(word):
    pass

def new_req(wd):
    Global.uniqueid = Global.uniqueid + 1
    request = "REQ-" + wd + "-" + str(Global.uniqueid)
    Global.all_reqs.insert(0, request)
    return Global.all_reqs[0]

def new_pool(word):
    Global.uniqueid = Global.uniqueid + 1
    pool = "POOL-" + word + "-" + str(Global.uniqueid)
    Global.all_pools.insert(0, pool)
    return Global.all_pools[0]


def putprop(sym, val, key):
    pass

def neq(arg1, arg2):
    pass


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

def trace_reqs(*reqs):
    for wd in reqs:
        if wd not in trace_reqs: # pushnew checks whether element is there in the list and if not then prepends it to the list
            trace_reqs.insert(0, wd)

def untrace_reqs(*reqs):
    if (reqs == None):
        trace_reqs = []
    else:
        for r in reqs:
            trace_reqs = trace_reqs.remove(r)


def pool_reqs(pool):
  pass


def props(s):
    pass
