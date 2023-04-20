#macros.py
import Global

#(defparameter *pmsg-flags* T) ;; show all msgs if T, else a list of keywords

pmsg_flags = True

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

def new_req(wd):
    Global.uniqueid = Global.uniqueid + 1
    request = "REQ-" + wd + "-" + str(Global.uniqueid)
    Global.all_reqs.insert(0, request)
    return Global.all_reqs[0]