import sys
import os

import key
import argparse
import secrets
import numpy as np
from itertools import chain as flatten, product as cartesian
from collections import Counter
import h5py

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


def simplify_anf(term):

    term.discard(1)  # a*1=a
    if 0 in term:
        return [0]  # a*0=0
    return term


def cartesian_remove_1s(*iterables):

    pools = [tuple(pool) for pool in iterables]

    result = [[]]
    for pool in pools:
        result = [
            x + [y] if y > 1 else x for x in result for y in pool
        ]  # remove redundancy: a*1=a

    for prod in result:
        yield tuple(prod)


def decompose(expression):

    expression = set(expression)  # remove redundancy: a*a=a

    def trim(t):
        if t[1] == 0:
            return (t[0],)  # a^0 = a
        return (t[0], t[1])

    expression = map(trim, expression)
    return np.fromiter(cartesian_remove_1s(*expression), dtype=tuple)


def encrypt():
    J_MAP = [secure.sample(range(1, M), ALPHA) for _ in range(BETA)]
    CLAUSES = key.generate_clause_list()

    # decompose([])

    # DISTRIBUTE
    # expanded_clauses = [list(cartesian(*c)) for c in CLAUSES.data]
    # print(expanded_clauses)
    # # SIMPLIFY
    # expanded_clauses = [
    #     [simplify_ANF_term(term) for term in clause] for clause in expanded_clauses
    # ]
    # print(expanded_clauses)

    cipher = []

    beta_sets_file = open(f"data/cipher_{args.count}/map_{args.count}", "w")

    for a in range(BETA):

        beta_clauses_list = [CLAUSES.data[r] for r in J_MAP[a]]
        beta_literals_list = [l[0] for l in flatten(*beta_clauses_list)]
        beta_counts_set = set(Counter(beta_literals_list).items())

        beta_sets_file.write(str(f"{beta_counts_set}\n"))

        for i in range(ALPHA):

            ### clause: C_J(i,a)
            clause = CLAUSES.data[
                J_MAP[a][i]
            ]  # includes parity: {(x_1, p_1),(x_2, p_2),(x_3, p_3)}
            clause_literals_set = set(
                [l[0] for l in clause]
            )  # excludes parity: {x_1, x_2, x_3}

            ### random: R_(i,a)
            beta_literals_subset = filter(
                lambda t: t[0] not in clause_literals_set or t[1] >= 2, beta_counts_set
            )
            beta_literals_subset = set(
                [l[0] for l in beta_literals_subset]
            )  # all literals in {c_J(i,b) | b != a}
            random = list(
                filter(lambda _: secure.choice([True, False]), beta_literals_subset)
            )
            random = [(t, secure.choice([0, 1])) for t in random]

            ### summand
            summand = clause + random
            summand = decompose(summand)
            # print("DECOMPOSED SUMMAND,", summand)

            cipher.append(summand)

    beta_sets_file.close()

    cipher = np.fromiter([np.sort(t, axis=0) for t in flatten(*cipher)], dtype=object)

    # SORT

    cipher = sorted(
        cipher, key=lambda term: [p(term) for p in CIPHER_SORTING_ORDER], reverse=True
    )
    # cipher = [[args.plaintext], [1]] + cipher
    cipher_term_lengths = [len[t] for t in cipher]


    # WRITE TO FILE
    vlen_dtype = h5py.vlen_dtype(np.dtype("float64"))

    filepath = f"data/cipher_{args.count}/cipher_{args.count}.hdf5"
    with h5py.File(filepath, "w") as file:
        dset = file.create_dataset(name="c0", shape=(len(cipher),), dtype=vlen_dtype)
        dset[:] = cipher




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
