# concept-fns.ipynb was concept-fns.lisp in https://github.com/jmacbeth/CA/blob/main/concept-fns.lisp. This was also originally CA5.lisp.
# This contains the functions for building and maintaining Concept Dependencies

import request_fns
import macros
import Global

#Build-CD (A function below) is used to build an atomized (divide something into smaller parts) Concept Dependency structure. It takes 3 arguments:
#1. must evaluate to a legal CD conceptualization, namely the one which is to be atomized.
#2. must evaluate to a list of pairs of the form (Path CD). The CD will be atomized and placed at the end of the path in the structure built by the first argument
#3. must evaluate to a list of pairs in the form (Path1 Path2). The CD at the end of Path1 replaces the CD at the end of Path2 in the structure built by the first argument.
# If Path1 is NIL then the entire concept is returned so that back-pointers can be set.
# The second and third arguments can be optional

# was originally a macro but no macros in python Add-Con calls build-cd (the function below)
# originally uses an apostrophe to stop direct evaluation (in lisp) not sure if thats an issue will find out if it crashes
def build_con(concept, fillers=[], equivalences=[]):
    return request_fns.add_con(concept, fillers, equivalences)

def build_cd(concept, fillers=[], equivalences=[]):
    con = make_cd(concept)
    for e in equivalences: # lambda(e) equivalences
        subst_cd(get_role_filler(e[0], con), get_role_filler(e[1], con), con) #car = e[0] cadr = e[1]
    for f in fillers:
        set_role_filler(f[0], con, f[1])
    return con

# get_role_value is like get_role filler but the argument has been atomized
# atom-eval is defined in the macros file
def get_role_value(path, concept):
    return atom_eval(get_role_filler(path, concept))

# get role filler returns the end of the path which its first argument evaluates to within the CD which its second argument evaluates to
# do we want cons to be a tuple or a list? (tuple is closer to LISP, but was really only needed for car and cadr)
# correction cons should most likely be a list of tuples
def get_role_filler(path, concept):
    if(path == None):
        return concept
    elif(isinstance(path, str)): # if we dont have a list of paths (not sure if we need isidentifier)
        con = concept
        if(isinstance(con, str)):
            con = Global.find_class(concept).value
        if(isinstance(con, list) or isinstance(con, tuple)):
            val = next((i for i,v in enumerate(con[1:]) if v[0] == path), None) # this searches through the tuples finds the one whose index 0 matches the path and returns its index 1
    elif(isinstance(path, tuple)):
        return get_role_filler(path[1:], get_role_filler(path[0], concept))


# Not sure about embedded here need to do more research
def set_role_filler(path,concept,filler):
    nc = make_cd(filler)
    oc = get_role_filler(path,concept)
    if(oc):
        subst_cd(nc, oc, concept)
    else:
        # dont have this (chain_gap oc nc) in preds.lisp (propagage slot change)
        add_gap(path,concept,nc)
    concept.insert(0, changed_cons)
    embedded = [ele for key in concept for ele in key]
    putprop(nc, concept, embedded)
    return concept

# are we sure were returning role instead of con
def add_gap(path, concept, filler):
    con = get_role_filler(path[:-1], concept)
    role = path[-1]
    if(not(get_role_filler(role,con)) and con):
        con = atom_eval(con)
        con.append(role[0])
        con.append(make_cd(filler))
        return role
    else:
        return None

def make_cd(x):
    con = build_c(x, [])
    if(x != con):
        Global.changed_cons.insert(0, con)
    return con

def build_c(x, seen):
    if(not(isinstance(x, list))):
        return x
    if(x == ['previous']):
        return seen[1]
    newcon = macros.new_con()
    Global.create_con(newcon)
    seen.insert(0, newcon)
    c = Global.find_class(newcon)
    a = build_m(x[0], seen)
    if(a != None):
        if(c.value == None):
            c.value = [a]
        else:
            if(isinstance(a, list)):
                c.value = c.value + a
            else:
                c.value.append(a)
    b = build_m(x[1:], seen)
    if(b != None):
        if(isinstance(b, list)):
            c.value = c.value + b
        else:
            c.value.append(b)
    return newcon

def build_m(x, seen):
    if(x == []):
        return x
    if(not(isinstance(x, list))):
        return x
    temp = []
    while(1):
        if(x == []):
            return temp
        temp.append(x[0])
        temp.append(build_c(x[1], seen))
        if(x[2:] == None):
            return temp[1:]
        x = x[2:]
        if(x[1:] == None):
            print("Bad Modifier list")
    return temp[1:]

def subst_cd(new_c, old_c, cd):
    subcdc(new_c, old_c, cd, None)

def subcdc(new_c, old_c, cd, seen):
    if(cd == old_c):
        return new_c
    if(cd in seen): #maybe issubset might work better
        return cd
    else:
        seen.append(cd)
        cd = [subcdm(new_c,old_c,eval(cd[0]), seen), subcdm(new_c,old_c,eval(cd[1:]), seen)]
        return cd

def subcdm(new_c, old_c, form, seen):
    if(form == old_c):
        return new_c
    if(not(isinstance(form, list)) and not(isinstance(form, tuple))):
        return form
    temp = [None]
    while(1):
        temp = temp + [form[0], subcdc(new_c, old_c, form[1], seen)]
        if(len(form) > 2):
            form = form[2:]
        else:
            return temp[1:]

