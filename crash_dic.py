import Global
import concept_fns
import control
import request_fns


def dic_a(art = ["art"]): #this is my best version so far may need to tweak later but follows his Test Action format and easyish to read
    #req = ["request", "clause(test True)", "(actions((activate(request(clause(test(assign(str2,(if-find(Feature(c,[\"loc\",\"PP\"]) and not(flagon(\"noun_group_flag\"))))))(actions(print(str1+\"=\"+str2+\"found pp\")) (fill-gap(\":ref\",str2,str1)))))))))))"]
    req = ["request", "clause(test True)", "(actions(crash_dic.actions_a())"]
    atts = art
    return req, atts

def actions_a():
    wd = Global.find_class("a")
    wd.str1 = concept_fns.build_con(["*indef*"], [], [])
    new_bind = ["str1", wd.str1]
    idx = 0
    while(idx < len(Global.bindings)):
        if Global.bindings[idx] == "str1":
            Global.bindings[idx] = new_bind
            break
        idx=idx+1
    request_fns.activate([["request", "clause(test crash_dic.cond_a())", "actions(actions_a_1())"]]) # we want it as one request

def cond_a():
    # getting the latest con should be the first all_cons
    if(request_fns.if_find(request_fns.feature(Global.all_cons[0], ['loc', 'pp'])) and not Global.flagon("noun_group_flag")):
        wd = Global.find_class("a")
        wd.str2 = True
        new_bind = ["str2", wd.str2]
        idx = 0
        while(idx < len(Global.bindings)):
            if Global.bindings[idx] == "str2":
                Global.bindings[idx] = new_bind
                break
            idx=idx+1
            return True
    else:
        wd = Global.find_class("a")
        wd.str2 = False
        new_bind = ["str2", wd.str2]
        idx = 0
        while(idx < len(Global.bindings)):
            if Global.bindings[idx] == "str2":
                Global.bindings[idx] = new_bind
                break
            idx=idx+1
        return False

def actions_a_1():
    wd = Global.find_class("a")
    print(wd.str1 + "=" + wd.str2 + "found pp")
    fill_gap(":ref", wd.str2, wd.str1)

def bindings_a():
    return ["str1","str2"]

def the(art):
    req = [True, "str1=build_con(*def*)", "activate(req(str2=if(not(Global.flagon(\"noun_group_flag\") and (request_fns.if_find(feature c [loc,pp]))))))", "fill_gap(Global.ref,str2,str1)"]
    atts =  art
    return req, atts

def actions_the():
    wd = Global.find_class("the")
    wd.str1 = concept_fns.build_con(["def"], [], [])
    request_fns.activate([["request", "clause(test cond_the(str2))", "actions(actions_the_1(str1, str2))"]])

def cond_the():
    if(if_find(feature(c, ['loc', 'pp'])) and not Global.flagon("noun_group_flag")):
        wd = Global.find_class("the")
        wd.str2 = True
        return True
    else:
        wd = Global.find_class("the")
        wd.str2 = False
        return False

def actions_the_1():
    wd = Global.find_class("the")
    fill_gap(":ref", wd.str2, wd.str1)

def bindings_the():
    return ["str1", "str2"]

def dic_small(adj = ["adj"]):
    req = req = ["request", "clause(test True)", "(actions(crash_dic.actions_small())"]
    atts = adj
    return req, atts

def actions_small():
    wd = Global.find_class("small")
    wd.str1 = concept_fns.build_con(["*ltnorm*"], [], [])
    request_fns.activate([["request", "clause(test cond_small())", "actions(actions_small_1())"]])

def cond_small():
    if request_fns.if_find(request_fns.feature(Global.all_cons[0], ['pp'])):
        wd = Global.find_class("small")
        wd.str2 = True
        new_bind = ["str2", wd.str2]
        idx = 0
        while(idx < len(Global.bindings)):
            if Global.bindings[idx] == "str2":
                Global.bindings[idx] = new_bind
                break
            idx=idx+1
        return True
    else:
        wd = Global.find_class("small")
        wd.str2 = False
        new_bind = ["str2", wd.str2]
        idx = 0
        while(idx < len(Global.bindings)):
            if Global.bindings[idx] == "str2":
                Global.bindings[idx] = new_bind
                break
            idx=idx+1
        return False

def actions_small_1():
    wd = Global.find_class("small")
    fill_gap(":ref", wd.str2, wd.str1)

def bindings_small():
    return ["str1", "str2"]

def twin_engine(adj):
    req = [True,
           "str1=build_con([*PP*, Global.class, (group)], [Global.number, (*num* number(*2*))], [Global.member, [*PP*, Global.class, (structure), Global.type, (engine)]]",
           "activate(req(str2=(request_fns.if_find(feature c [pp]) and request_fns.follows(c, str1)))",
           "fill_gap(Global.has_part,str2,str1)"]
    atts = adj
    return req, atts

def actions_twin_engine():
    wd = Global.find_class("twin_engine")
    wd.str1 = concept_fns.build_con(["PP", {"class" : "group"}, {"number" : ["num", "number", ["2"]]}, {"member" : ["PP", {"class" : ["structure", {"type" : "engine"}]}]}])

def plane (noun):
    req = [True, "build_con([*PP*, Global.class, (vehicle), Global.type, (airplane)]"]
    atts = noun
    return req, atts

def pilot(noun):
    req = [True, "build_con([*PP*, Global.class, (human), Global.type, (*pilot*)]"]
    atts = noun
    return req, atts

def stuffed(verb): #definitely wrong, probably will have to rework this entire file
    req = [True,
           "str1=build_con(*do* <=> (*ptrans*), Global.actor(nil), Global.object=(nil), Global.to(*inside* Global.part=(nil), Global.from=(nil), Global.time=(nil))",
           "activate_lexical_reqs(\"with\", req = [Global.word = \"with\", activate_next(req=[str2=request_fns.if_find(feature c \"pp\") and not(feature c 'hi-anim)), fill_gap(Global.rel, str2, str1); concept_fns.subst_cd(str2, (concept_fns.get_role_filler \"(Global.to Global.part) str1) str1))", "else:(request_fns.kill_self)"]




