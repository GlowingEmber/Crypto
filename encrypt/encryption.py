from parameters import *
import key_generation as key_generation
import argparse
import secrets
from itertools import product, chain

secure = secrets.SystemRandom()

def random_function(row_terms):
    terms = list(filter(lambda _: secure.choice([True, False]), row_terms))
    terms = [[e] for e in terms]
    return terms

def simplify_ANF_term(term):
    if 0 in term:
        return [0]
    term = list(filter(lambda e: e != 1, term))
    term = list(set(term))
    return term

def encrypt():
    J_MAP = [
        secure.sample(range(1, M), BETA) for _ in range(ALPHA)
    ]
    CLAUSES = key_generation.generate_clause_list()

    expanded_clauses = [list(product(*c)) for c in CLAUSES.data]
    expanded_clauses = [
        [simplify_ANF_term(term) for term in clause] for clause in expanded_clauses
    ]

    cipher = []

    for i in range(ALPHA):
        for a in range(BETA):

            row = J_MAP[a]
            row_clauses = [CLAUSES.data[r] for r in row]
            row_literals = [list(zip(*clause))[0] for clause in row_clauses]
            row_literal_set = set(chain(*row_literals))

            R_selection = random_function(row_literal_set)
            c_J = expanded_clauses[J_MAP[i][a]]
            
            summand = list(product(c_J, R_selection))
            summand = [list(chain(*term)) for term in summand]
            
            summand = [simplify_ANF_term(term) for term in summand]
            summand = list(filter(lambda t: t != [0], summand))

            cipher.append(summand)

    cipher = list(chain(*cipher))

    cipher = [sorted(term, key=lambda term: int(term[1:])) for term in cipher]
    cipher.sort(key=lambda term: tuple([p(term) for p in GENERATED_CIPHER_SORTING]))

    cipher = [[args.plaintext], [1]] + cipher

    print(cipher)

###

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="Encrypt",
        description="Generates ciphertext file from plaintext based on Sebastian E. Schmittner's SAT-Based Public Key Encryption Scheme",
        epilog="https://eprint.iacr.org/2015/771.pdf",
    )
    parser.add_argument("-y", "--plaintext", choices=[1, 0], type=int, default=1, nargs="?")
    parser.add_argument("-c", "--count", type=int, default=1, nargs="?")
    args = parser.parse_args()

    encrypt()
