import concept_fns
import Global
import control
import macros
import predicates

# creates a new con and calls build_cd to build it
def add_con(concept, fillers=[], equivalences=[], markers=[]):
    newcon = concept_fns.build_cd(concept, fillers, equivalences)
    if(markers):
        markers = eval(newcon)
    else:
        Global.c_list.insert(0, newcon)
        currentcon = Global.find_class(newcon)
        print("Adding " + newcon + " = ", currentcon.value)
    return newcon

def activate(reqs):
    activate1(reqs)

def activate1(reqs): #creates a new request and places it at the back of crash-dic
    w = Global.find_class(Global.current_req) #find the current req
    newreqs = control.make_requests(w.word, reqs, Global.bindings) #create a new req based on the information of the current reqs
    new_con = Global.c_list[0]  #get the latest con cause it will be the one for the current req
    if(new_con):
        con = Global.find_class(new_con)
        con.assoc_req = newreqs #make its associated req the new req since both are assigned to the same word
        print(Global.current_req + " activating new requests: ",newreqs)
    pool = None
    if(Global.current_pool): # get the current pool or create a new pool if it doesnt exist
        pool = Global.current_pool
    else:
        pool = macros.new_pool(Global.word)
        Global.create_pool(pool)
    if(Global.current_pool):
        p = Global.pool_reqs(pool) #get the current list of request for the pool
        for r in newreqs: #and add our new requests to the front of it
            p.insert(0, r)
            Global.set_pool_reqs(pool, p)
            p = Global.pool_reqs(pool)
    control.activate_pool(pool) #then activate the pool

def feature(obj, pred): # this is generally mess but the general idea is to find all preds that are in the obj
    if isinstance(pred, list):
            return any(feature(obj, p) for p in pred)
    # ((and (symbolp pred) (get pred :expr)) these always seem to come back as nil
    # (apply pred (list obj)))
    con = obj
    if(isinstance(obj, str) and obj.find("con") != -1):
        con = Global.find_class(obj).value
    if pred == 'concept':
        predicates.concept_p(obj)
    if predicates.group(con): #group doesnt get the value while the others do
        return True
    #if feature(concept_fns.get_role_filler("member", obj), pred): # This line is breaking and I dont know why
     #   return True
    if predicates.c_head(obj) == pred:
        return True
    if isinstance(predicates.c_head(obj), tuple) and predicates.c_head(obj).get("type", False) == pred:
        return True
    if isinstance(con, tuple) and (predicates.c_prop((con.get("class", False) [0]), pred)):
        return True
    if isinstance(con, tuple) and (predicates.c_prop((con.get("type", False) [0]), pred)):
        return True
    else:
        return False

def if_find(*body): #finds the first value in the C_list that does not have embedded as a property tag
    temp = None
    for C in Global.c_list:
        con = Global.find_class(C).value
        if "embedded" not in con and all(body):
            temp = C
            break
    return temp

def follows(c1, c2): #checks if both items are in the c_list and they are not the same
    return c1 != c2 and c1 in Global.c_list and c2 in Global.c_list

def fill_gap(path, cd, filler): #place a con at the back of the con
    if(path == None or cd == None):
        if isinstance(path, list):
            path = list(path)
        else:
            return None
    set_gap(path, cd, filler) #set_gap will place the info
    print("Inserting", filler, "into", cd, "at", path)
    if(predicates.concept_p(cd) and precedes(filler, cd)): #this is not currently called but good luck when it is
        Global.find_class(cd).contopic = realcon(filler)
        Global.last_embedded_con = filler
        Global.find_class(filler).embedded = cd
    return cd

def set_gap(path, cd, filler): 
    concept_fns.set_role_filler(path,cd,filler)


