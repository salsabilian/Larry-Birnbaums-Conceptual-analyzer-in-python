import Global
import macros

# (defmacro def (word . prop-vals)
#   `(mapc #'(lambda (k-v)
#                (setf (get ,word (car k-v)) (cdr k-v)))
#          ,prop-vals))
def def_(word, *prop_vals): 
    for k, v in prop_vals: # key-value pairs?
        k[1:], v[1:] = word[k[0], v[0]] # unsure

# (defparameter *req-props* '(trace :trace))
req_props = Global.trace(trace, []) # not sure

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
        # cons 'REQUEST
        for c in (reqform[1:]):
            if (c[0] in req_props):
                props.append(c) # where does props come from or do define it (props = [])?
            else:
                clauses.append(c)
            for clause in clauses:
                acts = expand_sub_reqs(clause[1:])

            

# (defun expand-sub-reqs (acts &aux newacts newsub)
#   (loop with newacts = acts
#         for sub-req = (sub-head-p 'req newacts)
#         while sub-req
#         do (setf newsub (expand-req sub-req))
#            (setf newacts (subst newsub sub-req newacts))
#         finally (return newacts)))
def expand_sub_reqs(acts, aux, newacts, newsub):

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
    # :execute means the code should be evaluated at runtime
    # :load-toplevel means code should be evaluated when the file is loaded
    # :compile-toplevel means code should be evaluated at compile time
    if (word not in Global.defined_words):
        Global.defined_words.insert(0, word)
    Global.add_atts(word, atts)
    Global.add_atts(word, requests)