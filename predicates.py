import Global
import concept_fns

# This whole file may have to be reworked depending on our basic implementation of con
#The general idea is to find the values within each con and see if they match values in the list

def c_head(x): #get the value at the start of the listof the con
    form =  Global.find_class(x).value
    return form[0]
#this checks if we have a concept and not just a valued con
def concept_p(x):
    form = Global.find_class(x).value
    head = c_head(x)
    if(has_type(x, ["primitive-act", "state", "interp-relation"]) or script(x) or (head in ["lead-to-enable", "*do*"] and head.get("form", False))):
        return True
    else:
        return False
#checks if the type of con i.e. the : property tags are in the list
def has_type(c, typ):
    head =  c_head(c)
    member = None
    if isinstance(typ, list):
        return any(has_type(c, t1) for t1 in typ)
    if head == typ:
        return True
    elif head[0] == ":type" and group(c):
        member = concept_fns.get_role_filler("member", c)
        has_type(member, typ)
    return False
#checks if the group value is anywhere inside the con list
def group(x):
    if(isinstance(x, list)):
        for i in x:
            if(isinstance(i, tuple)):
                if i.get("class", False) == ["group"]:
                    return True
        return False
    return x == ["group"]
#checks if there is a script in the list
def script(x):
    h = c_head(x)
    if(isinstance(h, str) and h.startswith("$")):
        return True
    else:
        return False
#gets the value for a con and returns it
def c_prop(x, prop):
    target = Global.get_role_filler(prop, x)
    return Global.find_class(target).value