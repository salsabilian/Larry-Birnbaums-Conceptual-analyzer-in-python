import Global

def c_head(x):
    form =  Global.find_class(x).value
    return form[0]

def concept_p(obj):
    form = Global.find_class(obj).value
    head = c_head(obj)