import Global
import concept_fns

def c_head(x):
    form =  Global.find_class(x).value
    return form[0]

def concept_p(x):
    form = Global.find_class(x).value
    head = c_head(x)
    if(has_type(x, ["primitive-act", "state", "interp-relation"]) or script(x) or (head in ["lead-to-enable", "*do*"] and head.get("form", False))):
        return True
    else:
        return False

def has_type(c, typ):
    head =  c_head(c)
    member = None
    if isinstance(typ, list):
        return any(has_type(c, t1) for t1 in typ)
    if head == typ:
        return True
    elif head.get("type", False) and group(c):
        member = concept_fns.get_role_filler("member", c)
        has_type(member, typ)
    return False

def group(x):
    if(isinstance(x, list)):
        for i in x:
            if(isinstance(i, tuple)):
                if i.get("class", False) == ["group"]:
                    return True
        return False
    return x == ["group"]

def script(x):
    h = c_head(x)
    if(isinstance(h, str) and h.startswith("$")):
        return True
    else:
        return False


def c_prop(x, prop):
    target = Global.get_role_filler(prop, x)
    return Global.find_class(target).value