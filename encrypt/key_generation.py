from parameters import *
import secrets
import PL as PL

secure = secrets.SystemRandom()

PRIVATE_KEY = secrets.randbits(N)
PRIVATE_KEY_STRING = f"{bin(PRIVATE_KEY)[2:]:0>{N}}"  # B^n
valid_clause = lambda literal_index, parity: int(PRIVATE_KEY_STRING[literal_index]) == parity


def _generate_valid_clause():  # all variables ORed
    clause_literals = [f"x{l}" for l in secure.sample(range(N), K)]
    clause_signs = secure.sample([0, 1] * K, K)
    clause = [clause_literals, clause_signs]

    if any([valid_clause(int(clause[0][k][1:])-1, clause[1][k]) for k in range(K)]):
        return list(zip(*clause))
    return _generate_valid_clause()


def generate_clause_list():
    return PL.Expression(form="CNF", data=[_generate_valid_clause() for _ in range(M)])
