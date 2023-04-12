#macros.py

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
