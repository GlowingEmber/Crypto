from parameters import *
import secrets
import PL as PL
secure = secrets.SystemRandom()

PRIVATE_KEY = secrets.randbits(N)
PRIVATE_KEY_STRING = f"{bin(PRIVATE_KEY)[2:]:0>{N}}" # B^n
valid_clause = lambda i, p: int(PRIVATE_KEY_STRING[i]) == p

def _generate_valid_clause(): # all variables ORed
    clause_integers = secure.sample(range(N), K)
    clause_signs = secure.sample([0, 1] * K, K)
    clause = tuple([clause_integers, clause_signs])

    if any([valid_clause(clause[0][k], clause[1][k]) for k in range(K)]):
        return clause
    return _generate_valid_clause()

def generate_clause_list(): 
    # return [_generate_valid_clause() for _ in range(M)]
    return PL.Expression(form="CNF", data=[_generate_valid_clause() for _ in range(M)])