import key
import argparse
import secrets
from itertools import chain as flatten, product as cartesian
from collections import Counter

import sys
import os

sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)
from parameters import *

secure = secrets.SystemRandom()


def random_subset(available_row_literals_set):
    literals = filter(
        lambda _: secure.choice([True, False]), available_row_literals_set
    )
    literals = set([(l, secure.choice([0, 1])) for l in literals])
    return literals


def simplify_ANF_term(term):
    term = set(term)
    term.discard(1)
    if 0 in term:
        return [0]
    return term


def simplify(expression):
    pass
    # expression = [list(flatten(*term)) for term in expression]
    # expression = [simplify_ANF_term(term) for term in expression]
    # expression = list(filter(lambda t: t != [0], expression))

    # print(expression)
    # falses = set(map(lambda t: t[0], filter(lambda t: t[1] == 0, expression)))
    # trues = set(map(lambda t: t[0], filter(lambda t: t[1] == 1, expression)))

    # trues = trues - falses
    # return [(term,1) for term in trues] + [(term,0) for term in falses]


def encrypt():
    J_MAP = [secure.sample(range(1, M), ALPHA) for _ in range(BETA)]
    CLAUSES = key.generate_clause_list()

    # DISTRIBUTE
    # expanded_clauses = [list(cartesian(*c)) for c in CLAUSES.data]
    # print(expanded_clauses)
    # # SIMPLIFY
    # expanded_clauses = [
    #     [simplify_ANF_term(term) for term in clause] for clause in expanded_clauses
    # ]
    # print(expanded_clauses)

    cipher = []

    # f = open("data/cipher_0/map_0", "x")  # temporary solution

    print(J_MAP)

    for a in range(BETA):

        beta_clauses_list = [CLAUSES.data[r] for r in J_MAP[a]]
        beta_literals_list = [l[0] for l in flatten(*beta_clauses_list)]
        beta_counts_set = set(Counter(beta_literals_list).items())

        for i in range(ALPHA):

            clause = CLAUSES.data[J_MAP[a][i]]  # {(x_1, p_1),(x_2, p_2),(x_3, p_3)}
            clause_literals_set = set([l[0] for l in clause])  # {x_1, x_2, x_3}
            beta_literals_subset = filter(
                lambda t: t[0] not in clause_literals_set or t[1] >= 2, beta_counts_set
            )
            beta_literals_subset = set(
                [l[0] for l in beta_literals_subset]
            )  # all literals in {c_J_(i,b) | b != a}


            ### 
            random = list(
                filter(lambda _: secure.choice([True, False]), beta_literals_subset)
            )
            random = [(t, secure.choice([0, 1])) for t in random]

            summand = clause + random
            cipher.append(summand)

        # beta_literals_set = set(beta_literals_list)
        # beta_literals_count = set(Counter(beta_literals_list).items()) # BETA_a row literals with number of repeats
        # # print(beta_literals_set)

        # f.write(str(f"{beta_literals_set}\n"))

        # for i in range(ALPHA):
        #     pass

        # print([x[0] for x in CLAUSES.data[J_MAP[a][i]]])
        # print([x[0] for x in beta_literals_count])

        # available_beta_literals = list(filter(lambda t: t[0] not in clause_literals_set or t[1] > 1, clause_literals_set))
        # # random_literals_set = random_subset(available_beta_literals)
        # print(clause_literals_set)
        # print(beta_literals_set)
        # print(available_beta_literals)

        # clause_literals_set = set([l[0] for l in CLAUSES.data[J_MAP[i][a]]])
        # available_beta_literals = list(filter(lambda t: t[0] in clause_literals_set and t[1] < 2, beta_literals_count))
        # print("clause_literals_set", clause_literals_set)
        # print("beta_literals_count", beta_literals_count)
        # print("available_beta_literals", available_beta_literals)

        # for i in range(ALPHA):

        #     clause = CLAUSES.data[J_MAP[i][a]]
        #     clause_literals = set([l[0] for l in flatten(*clause)])

    # f.close()
    # cipher = list(flatten(*cipher))

    # SORT

    # cipher = [sorted(term, key=lambda term: int(term[1:])) for term in cipher]
    # cipher = sorted(cipher, key=lambda term: [p(term) for p in CIPHER_SORTING_ORDER])
    # cipher = [[args.plaintext], [1]] + cipher

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
    parser.add_argument(
        "-y", "--plaintext", choices=[1, 0], type=int, default=1, nargs="?"
    )
    parser.add_argument("-c", "--count", type=int, default=1, nargs="?")
    args = parser.parse_args()

    encrypt()
