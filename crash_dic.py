import Global
import concept_fns
import control
import request_fns


def dic_a(art = ["art"]): #this is my best version so far may need to tweak later but follows his Test Action format and easyish to read
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
    request_fns.activate([["request", "clause(test crash_dic.cond_a())", "actions(crash_dic.actions_a_1())"]]) # we want it as one request

def cond_a():
    # getting the latest con should be the first c_list
    if(request_fns.if_find(request_fns.feature(Global.c_list[0], ['loc', '*PP*'])) and not Global.flagon("noun_group_flag")):
        wd = Global.find_class("a")
        wd.str2 = Global.c_list[0]
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
    print("A = " + wd.str1 + " found pp " + wd.str2 + " = " + wd.str1)
    request_fns.fill_gap([":ref"], wd.str2, wd.str1)

def bindings_a():
    return ["str1","str2"]

def dic_small(adj = ["adj"]):
    req = ["request", "clause(test True)", "(actions(crash_dic.actions_small())"]
    atts = adj
    return req, atts

def actions_small():
    wd = Global.find_class("small")
    wd.str1 = concept_fns.build_con(["*ltnorm*"], [], [])
    request_fns.activate([["request", "clause(test crash_dic.cond_small())", "actions(crash_dic.actions_small_1())"]])

def cond_small():
    if request_fns.if_find(request_fns.feature(Global.c_list[0], ['*PP*'])):
        wd = Global.find_class("small")
        wd.str2 = Global.c_list[0]
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
    request_fns.fill_gap([":size"], wd.str2, wd.str1)

def bindings_small():
    return ["str1", "str2"]

def dic_twin_engine(adj = ["adj"]):
    req = ["request", "clause(test True)", "(actions(crash_dic.actions_twin_engine())"]
    atts = adj
    return req, atts

def bindings_twin_engine():
    return ["str1", "str2"]

def actions_twin_engine():
    wd = Global.find_class("twin_engine")
    wd.str1 = concept_fns.build_con(["*PP*", ":class", ["group"], ":number", ["num", "number", ["2"]], ":member", ["*PP*", ":class", ["structure", ":type", ["engine"]]]])
    request_fns.activate([["request", "clause(test crash_dic.cond_twin_engine())", "actions(crash_dic.actions_twin_engine_1())"]])

def cond_twin_engine():
    wd = Global.find_class("twin_engine")
    if request_fns.if_find(request_fns.feature(Global.c_list[0], ['*PP*']) and request_fns.follows(Global.c_list[0], wd.str1)):
        wd.str2 = Global.c_list[0]
        new_bind = ["str2", wd.str2]
        idx = 0
        while(idx < len(Global.bindings)):
            if Global.bindings[idx] == "str2":
                Global.bindings[idx] = new_bind
                break
            idx=idx+1
        return True
    else:
        wd = Global.find_class("twin_engine")
        wd.str2 = False
        new_bind = ["str2", wd.str2]
        idx = 0
    while(idx < len(Global.bindings)):
        if Global.bindings[idx] == "str2":
            Global.bindings[idx] = new_bind
            break
        idx=idx+1
    return False

def actions_twin_engine_1():
    wd = Global.find_class("twin_engine")
    request_fns.fill_gap([":has-part"], wd.str2, wd.str1)

def dic_plane (noun = ["noun"]):
    req = ["request", "clause(test True)", "actions(crash_dic.actions_plane())"]
    atts = noun
    return req, atts

def actions_plane():
    concept_fns.build_con(["*PP*", ":class", ["vehicle"], ":type", ["airplane"]])

def bindings_plane():
    return []

def dic_stuffed(verb = ["verb"]):
    req = ["request", "clause(test True)", "actions(crash_dic.actions_stuffed())"]
    atts = verb
    return req, atts




