#globals.lisp
import crash_dic

#Added variable to keep track of parans
parans = 0
# Might Want to switch to a class based implementation (more dynamic)
class dic_word:
    extra_requests = None
    tracep = None
    bindings = None
    str1 = None
    str2 = None
    str3 = None
class req:
    tracep = None
    bindings = None
class con:
    value = None
a = dic_word()
small = dic_word()
twin_engine = dic_word()
plane = dic_word()
stuffed = dic_word()
# unique id counter for requests we could change this later to something more sophisticated if needed
uniqueid = 0
# (defparameter CHANGED-CONS nil)
changed_cons = []
# (defparameter CURRENT-PHRASE nil)
current_phrase = []
# (defparameter CURRENT-MODULE :CA)
current_module = "CA" #unsure
# (defparameter WORKING nil)
working = []
# (defparameter N-P-RECORD nil)
n_p_record = []
# ; (defparameter NEXT-WORD nil)
# next_word = []
# (defparameter *PAUSE* nil)
pause = []
# ;;; declared in CA4 (request-actions.lisp)
# ; (defparameter NEW-CON nil) ;; (was called !NEW-CON)
# new_con = []
# (defparameter LEXICAL-POOL nil)
lexical_pool = []
# (defparameter LAST-EMBEDDED-CON nil)
last_embedded_con = []
# (defparameter CHANGED-CONS nil)
changed_cons = []
# (defparameter *BINDINGS* nil) ;; just to declare it special. It will be scoped.
bindings = []
# ;;; from control.py.lisp mostly
# ;;;; THIS SHOULD BE REORG'd into a single top level data structure, not all these globals

# (defparameter ALL-REQS nil)
all_reqs = []
# (defparameter ALL-CONS nil)
all_cons = []
# (defparameter ALL-POOLS nil)
all_pools = []
# (defparameter CURRENT-POOL nil) ;; set when considering requests in that pool (MB 2/1/21)
current_pool = []
# (defparameter CURRENT-REQ nil)
current_req = None
# (defparameter ALL-LEXES nil)
all_lexes = []
# ; (defparameter SENT nil)  ;; redundant with SENTENCE - changed all occurrences to SENTENCE
# sent = []
# (defparameter SENTENCE nil)
sentence = []
# (defparameter INPUT nil) ;; list of sentence s-expressions, pop'd into SENTENCE one at a time
input = []

# (defparameter WORD nil) ;; the current word after pop'd off sentence
word = None
# (defparameter *defined-words* nil) ;; added by MB to keep track of defterms
defined_words = []
# ;;; changing this to a macro
# ;; (defparameter NEXT-WORD nil)

# (defmacro NEXT-WORD () `(car SENTENCE))
def next_word():
    if(sentence):
        if(sentence[0] == "twin-engine"):
            return "twin_engine"
        else:
            return sentence[0]
    else:
        return None

# (defparameter C-LIST nil)
c_list = []
# (defparameter REQUEST-POOLS nil)
request_pools = []
# (defparameter EXTRA-REQUESTS nil)
extra_requests = []
# (defparameter N-P-RECORDS nil)
n_p_records = []
# (defparameter LAST-EMBEDDED-CON nil)
last_embeded_con = []
# (defparameter CHANGED-CONS nil)
changed_cons = []
# (defparameter LEX nil)   ;;
lex = []
# (defparameter NEXT-LEX nil)
next_lex = []
# (defparameter POOL nil)
pool = []
# ;;; all flags are placed on the list :flags; the following functions test and remove flags
# (defparameter *flags* nil)
flags = []

# (defmacro flagon (flag) `(member ,flag *flags*))
def flagon(flag):
    return flag in flags
# (defmacro remove-flag (flag)
#   `(setf *flags* (remove ,flag *flags*)))
def remove_flag(flag):
    if(flagon(flag)):
        flags.remove(flag)
    else:
        print("flag not in flags")
# (defmacro add-flag (flag)
#   `(pushnew ,flag *flags*))
def add_flag(flag):
    flags.insert(0, flag)

def add_property(prop, key, val):
    prop[key] = val

def subst(new_val, old_val, sub_in_list):
    length = len(sub_in_list)
    i = 0
    while (i != length):
        if (sub_in_list[i] == old_val):
            sub_in_list[i] = new_val
        i += 1

# ;;; This initializes some variables - book-keeping globals containing generated gensyms
# (defun INIT-CA-VARS ()
#   (setf ALL-REQS nil)
#   (setf ALL-CONS nil)
#   (setf ALL-POOLS nil)
#   (setf ALL-LEXES nil)
#   (setf WORD nil)
#   ;; (setf NEXT-WORD nil) ;; now use macro
#   (setf C-LIST nil)
#   (setf REQUEST-POOLS nil)
#   (setf EXTRA-REQUESTS nil)
#   (setf *FLAGS* nil)
#   (setf N-P-RECORDS nil)
#   (setf LAST-EMBEDDED-CON nil)
#   (setf CHANGED-CONS nil)
#   ; (setf SENT nil)
#   (setf SENTENCE nil))
def init_ca_vars():
    all_reqs = []
    all_cons = []
    all_pools = []
    all_lexes = []
    word = []
    c_list = []
    request_pools = []
    extra_requests = []
    flags = []
    n_p_records = []
    last_embedded_cons = []
    changed_cons = []
    # sent = []
    sentence = []
    req, atts = crash_dic.dic_a()
    a.atts = atts
    a.requests = [req]
    req, atts = crash_dic.dic_small()
    small.atts = atts
    small.requests = [req]
    req, atts = crash_dic.dic_twin_engine()
    twin_engine.atts = atts
    twin_engine.requests = [req]
    req, atts = crash_dic.dic_plane()
    plane.atts = atts
    plane.requests = [req]
    req, atts = crash_dic.dic_stuffed()
    stuffed.atts = atts
    stuffed.requests = [req]

def pool_reqs(pool):
    return globals()[pool]

def set_pool_reqs(pool, new_value):
    globals()[pool] = new_value

def remove_pool_reqs(pool, value):
    globals()[pool].remove(value)

def find_class(class_name):
    return globals()[class_name]

def create_con(con_name):
    c = globals()[con_name] = con()
    return con_name

def create_req(req_name):
    r = globals()[req_name] = req()
    return r

def create_pool(pool_name):
    globals()[pool_name] = []
    return pool_name