import concept_fns
import Global
import control
import macros
import predicates


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

def activate1(reqs):
    w = Global.find_class(Global.current_req)
    newreqs = control.make_requests(w.word, reqs, Global.bindings)
    new_con = Global.c_list[0]
    if(new_con):
        con = Global.find_class(new_con)
        con.assoc_req = newreqs #if this becomes an issue later can change for req in reqs in make_request
        print(Global.current_req + " activating new requests: ",newreqs)
    pool = None
    if(Global.current_pool):
        pool = Global.current_pool
    else:
        pool = macros.new_pool(Global.word)
        Global.create_pool(pool)
    if(Global.current_pool): #not 100% here
        p = Global.pool_reqs(pool)
        for r in newreqs:
            Global.set_pool_reqs(pool, p.insert(0, r))
            p = Global.pool_reqs(pool)
    control.activate_pool(pool)

def feature(obj, pred):
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

def if_find(*body):
    temp = None
    for C in Global.c_list:
        con = Global.find_class(C).value
        if "embedded" not in con and all(body):
            temp = C
            break
    return temp

