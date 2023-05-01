import Global
import macros
import utils

# (defmacro def (word . prop-vals)
#   `(mapc #'(lambda (k-v)
#                (setf (get ,word (car k-v)) (cdr k-v)))
#          ,prop-vals))
def def_(word, *prop_vals): 
    for k, v in prop_vals: # key-value pairs?
        word[k[0], v[0]] = k[1:], v[1:] # unsure

# (defparameter *req-props* '(trace :trace))
req_props = ['trace', ':trace'] # not sure, single quote means treat it as literal expression and not evaluate it

# (defun expand-req (reqform)
#   (when (eq (car reqform) 'REQ)
#     (cons 'REQUEST 
#           (loop for c in (cdr reqform)
#                 when (member (car c) *req-props*)
#                   collect c into props
#                 else collect c into clauses
#                 finally
#                    (return 
#                      (append props
#                              (loop for clause in clauses
#                                    for acts = (expand-sub-reqs (cdr clause))
#                                    collect `(CLAUSE (TEST ,(car clause))
#                                                     (ACTIONS ,@acts)))
#                       ))))))
def expand_req(reqform):
    props = []
    clauses = []
    if (reqform[0] == 'req'):
        r = ['request']
        for c in (reqform[1:]):
            if (c[0] in req_props):
                props.append(c)
            else:
                clauses.append(c)
            for clause in clauses:
                acts = expand_sub_reqs(clause[1:])
                expand_reqs = ['clause', ['test', clause[0]], ['actions', *acts]]
            props.append(expand_reqs)
        return r + props

# (defun expand-sub-reqs (acts &aux newacts newsub)
#   (loop with newacts = acts
#         for sub-req = (sub-head-p 'req newacts)
#         while sub-req
#         do (setf newsub (expand-req sub-req))
#            (setf newacts (subst newsub sub-req newacts))
#         finally (return newacts)))
def expand_sub_reqs(acts, aux, newacts, newsub):
    newacts = acts
    sub_req = sub_head_p('req', newacts)
    while (sub_req):
        sub_req = sub_head_p('req', newacts)
        newsub = expand_req(sub_req)
        newacts = subst(newsub, sub_req, newacts) # there is a subst_cd in concept_fns, but what is subst?
        return newacts

# (defmacro defterm (word atts . reqs)
#   (let ((requests
#           (loop for reqform in reqs
#                 collect (expand-req reqform))))
#   `(eval-when (:load-toplevel :execute :compile-toplevel)
#      (prog ()
#        (pushnew ',word *defined-words*)
#        (setf (get ',word :atts) ',atts)
#        (setf (get ',word :requests) ',requests)))))
def defterm(word, atts, *reqs):
    requests = []
    for reqform in reqs:
        requests.append(expand_req(reqform))
    # (eval-when (:load-toplevel :execute :compile-toplevel) tells when the code should be evaluated
    # :load-toplevel means code should be evaluated when the file is loaded
    # :execute means the code should be evaluated at runtime
    # :compile-toplevel means code should be evaluated at compile time
    if (word not in Global.defined_words):
        Global.defined_words.insert(0, word)
    Global.add_property(Global.atts, word, atts)
    Global.add_property(Global.requests, word, requests)