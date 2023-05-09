import concept_fns
import Global
import control

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
    pool