import concept_fns
import Global

def add_con(concept, fillers=[], equivalences=[], markers=[]):
    newcon = concept_fns.build_cd(concept, fillers, equivalences)
    if(markers):
        markers = eval(newcon)
    else:
        Global.c_list = Global.c_list.insert(0, newcon)
        print("Adding" + newcon + "=" + newcon.value)
    return newcon
