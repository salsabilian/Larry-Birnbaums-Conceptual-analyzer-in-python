import Global
import macros
#This file is also not currently used
# (defun sub-head-p (item tree)
#   (cond ((not (consp tree)) nil)
#         ((equal item (car tree)) tree)
#         (t (or (sub-head-p item (car tree))
#                (sub-head-p item (cdr tree))))))
def sub_head_p(item, tree):
    if (not(isinstance(tree, list) or isinstance(tree, tuple))):
        return None
    elif (item == tree[0]):
        return tree
    else:
        return sub_head_p(item, tree[0]) or sub_head_p(item, tree[1:])