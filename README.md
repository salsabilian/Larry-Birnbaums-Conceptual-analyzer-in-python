In the 1970s the Yale AI group designed one of the first conceptual analyzer. This CA was called the Larry Birnbaum's Conceptual analyzer and was designed in Mlisp
and was based on the original system English Language Interpreter. Modifications and additions to the code were done in 1978-9 by Mark Burstein and Lewis Johnson. In
2022, Mark Burstein recovered the original code from printouts and converted it to common lisp here: https://github.com/jmacbeth/CA. The purpose of this code repository
is to convert Mark Bursteins common lisp implementation over to python. 

You can run the program using the command: python main.py.
The current output is: 

Current Input: ['(a small twin-engine plane stuffed with marijuana crashed south of here yesterday)']
New Sentence is ['a', 'small', 'twin-engine', 'plane', 'stuffed', 'with', 'marijuana', 'crashed', 'south', 'of', 'here', 'yesterday']


======================= Current Word: a ==========================
Phrase: ['a'] rest: ['small', 'twin-engine', 'plane', 'stuffed', 'with', 'marijuana', 'crashed', 'south', 'of', 'here', 'yesterday']
ACTIVATE-ITEM-REQUESTS for word  a :  ['REQ-a-1']
REQ-a-1 has fired
Adding CON3 =  ['*indef*']
REQ-a-1 activating new requests:  ['REQ-a-4']
Begin noun group:
Begin noun group;


======================= Current Word: small ==========================
Phrase: ['a', 'small'] rest: ['twin-engine', 'plane', 'stuffed', 'with', 'marijuana', 'crashed', 'south', 'of', 'here', 'yesterday']
Begin noun group:
ACTIVATE-ITEM-REQUESTS for word  small :  ['REQ-small-5']
REQ-small-5 has fired
Adding CON7 =  ['*ltnorm*']
REQ-small-5 activating new requests:  ['REQ-small-8']


======================= Current Word: twin_engine ==========================
Phrase: ['a', 'small', 'twin_engine'] rest: ['plane', 'stuffed', 'with', 'marijuana', 'crashed', 'south', 'of', 'here', 'yesterday']
Begin noun group:
ACTIVATE-ITEM-REQUESTS for word  twin_engine :  ['REQ-twin_engine-9']
REQ-twin_engine-9 has fired
Adding CON11 =  ['*PP*', ':class', 'CON12', ':number', 'CON13', ':member', 'CON15']
REQ-twin_engine-9 activating new requests:  ['REQ-twin_engine-18']
REQ-small-8 has fired
Inserting CON7 into CON11 at [':size']


======================= Current Word: plane ==========================
Phrase: ['a', 'small', 'twin_engine', 'plane'] rest: ['stuffed', 'with', 'marijuana', 'crashed', 'south', 'of', 'here', 'yesterday']
End of noun group
ACTIVATE-ITEM-REQUESTS for word  plane :  ['REQ-plane-19']
REQ-plane-19 has fired
Adding CON21 =  ['*PP*', ':class', 'CON22', ':type', 'CON23']
REQ-twin_engine-18 has fired
Inserting CON11 into CON21 at [':has-part']
REQ-a-4 has fired
A = CON3 found pp CON21 = CON3
Inserting CON3 into CON21 at [':ref']


======================= Current Word: stuffed ==========================
Phrase: ['a', 'small', 'twin_engine', 'plane', 'stuffed'] rest: ['with', 'marijuana', 'crashed', 'south', 'of', 'here', 'yesterday']
ACTIVATE-ITEM-REQUESTS for word  stuffed :  ['REQ-stuffed-24']
