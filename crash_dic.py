import Global
import concept_fns


def dic_a(art = "art"): #this is my best version so far may need to tweak later but follows his Test Action format and easyish to read
    #req = ["request", "clause(test True)", "(actions((activate(request(clause(test(assign(str2,(if-find(Feature(c,[\"loc\",\"PP\"]) and not(flagon(\"noun_group_flag\"))))))(actions(print(str1+\"=\"+str2+\"found pp\")) (fill-gap(\":ref\",str2,str1)))))))))))"]
    req = ["request", "clause(test True)", "(actions(crash_dic.actions_a())"]
    atts = art
    return req, atts

def actions_a():
    wd = Global.find_class("a")
    wd.str1 = concept_fns.build_con(["indef"], [], [])
    activate(["request", "clause(test cond_a(str2))", "actions(actions_a_1(str1, str2))"])

def cond_a():
    if(if_find(feature(c, ['loc', 'pp'])) and not Global.flagon("noun_group_flag")):
        wd = Global.find_class("a")
        wd.str2 = True
        return True
    else:
        wd = Global.find_class("a")
        wd.str2 = False
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

def small(adj):
    req = [True, "str1=build_con(*ltnorm*)", "activate(req(str2=(request_fns.if_find(feature c [pp]))))", "fill_gap(Global.size,str2,str1)"]
    atts = adj
    return req, atts

def twin_engine(adj):
    req = [True,
           "str1=build_con([*PP*, Global.class, (group)], [Global.number, (*num* number(*2*))], [Global.member, [*PP*, Global.class, (structure), Global.type, (engine)]]",
           "activate(req(str2=(request_fns.if_find(feature c [pp]) and request_fns.follows(c, str1)))",
           "fill_gap(Global.has_part,str2,str1)"]
    atts = adj
    return req, atts

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




