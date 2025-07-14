from parameters import *
import key_generation as key_generation
import argparse
import secrets
from itertools import chain as flatten, product as cartesian

secure = secrets.SystemRandom()

def random_subset(row_terms):
    terms = list(filter(lambda _: secure.choice([True, False]), row_terms))
    terms = [l for l in terms]
    return terms

def simplify_ANF_term(term):
    term = set(term)
    term.discard(1)
    if 0 in term:
        return [0]
    return term

def simplify(expression):
    expression = [list(flatten(*term)) for term in expression]
    expression = [simplify_ANF_term(term) for term in expression]
    expression = list(filter(lambda t: t != [0], expression))
    return expression

def encrypt():
    J_MAP = [
        secure.sample(range(1, M), BETA) for _ in range(ALPHA)
    ]
    CLAUSES = key_generation.generate_clause_list()

    # DISTRIBUTE
    expanded_clauses = [list(cartesian(*c)) for c in CLAUSES.data]
    # SIMPLIFY
    expanded_clauses = [
        [simplify_ANF_term(term) for term in clause] for clause in expanded_clauses
    ]

    cipher = []

    for a in range(BETA):

        row = J_MAP[a]
        row_clauses = [CLAUSES.data[r] for r in row]
        row_literals = set([l[0] for l in flatten(*row_clauses)])

        for i in range(ALPHA):
    
            clause = expanded_clauses[J_MAP[i][a]]
            random = [random_subset(row_literals)]

            summand = simplify(cartesian(clause, random))

            cipher.append(summand)

    cipher = list(flatten(*cipher))

    # SORT

    cipher = [sorted(term, key=lambda term: int(term[1:])) for term in cipher]
    cipher = sorted(cipher, key=lambda term: [p(term) for p in GENERATED_CIPHER_SORTING])
    cipher = [[args.plaintext], [1]] + cipher

    # if True:
    #     cipher.reverse()

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
