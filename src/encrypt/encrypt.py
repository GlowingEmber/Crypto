import sys
import os
from . import key
import argparse
import secrets
from itertools import chain as flatten, combinations as subset, product as cartesian
from collections import Counter

import numpy as np
import h5py

from parameters import *
# from ..decrypt.decrypt import decrypt

sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)
secure = secrets.SystemRandom()


def distribute(iterable):  # itertools powerset recipe
    s = list(iterable)
    return flatten.from_iterable(subset(s, r) for r in range(1, len(s) + 1))


###
# [(3, 0), (4, 1), (7, 1)]
# [(3,1), (4,0), (7,0)]
# [ 347 340 307 300 147 140 107 100 ]
# [ 347 340 307 300 147 140 107 100 ]
# [ 347 340 307 300 147 140 107 100 ]
#

# [(3, 0), (4, 1), (7, 1)]
# 347 341 317 311
# 347 34 37 3


def cnf_to_neg_anf(term):
    # NOT a, represented as tuple(a,0), equals a^1
    # a, represented as tuple(a,1), equals a^0
    # term = [(l[0], l[1] ^ 1) for l in term]

    term = term + [(1,)]
    term = cartesian(*term)
    term = filter(lambda t: 0 not in t, term)  # a*0 = 0
    term = map(lambda t: tuple(filter(lambda t: t != 1, t)), term)  # a*1 = a
    term = map(lambda t: tuple(set(t)), term)  # a*a = a
    term = list(term)
    return term


def encrypt():
    J_MAP = [secure.sample(range(1, M), ALPHA) for _ in range(BETA)]
    CLAUSES = key.generate_clause_list()

    cipher = []
    beta_sets_file = open(f"data/cipher_{args.count}_dir/map_{args.count}.txt", "w")

    for a in range(BETA):

        beta_clauses_list = [CLAUSES.data[r] for r in J_MAP[a]]
        beta_literals_list = [l[0] for l in flatten(*beta_clauses_list)]
        beta_counts_set = set(Counter(beta_literals_list).items())

        beta_sets_file.write(str(f"{beta_counts_set}\n"))

        for i in range(ALPHA):

            ### CLAUSE
            clause = CLAUSES.data[
                J_MAP[a][i]
            ]  # includes parity: [(x_1, p_1),(x_2, p_2),(x_3, p_3)]
            clause_literals_set = set(
                [l[0] for l in clause]
            )  # excludes parity: {x_1, x_2, x_3}

            ### RANDOM
            beta_literals_subset = filter(
                lambda t: t[0] not in clause_literals_set or t[1] >= 2, beta_counts_set
            )
            beta_literals_subset = set(
                [l[0] for l in beta_literals_subset]
            )  # all literals in {c_J(i,b) | b != a}

            anf_all_terms = list(distribute(beta_literals_subset))

            random = list(filter(lambda _: secure.choice([True, False]), anf_all_terms))

            # random = [(t, secure.choice([0, 1])) for t in random]

            ### SUMMAND

            # print("C in CNF", clause) # CNF
            # print("CLAUSE", clause)
            # print("ASSIGNMENT", [int(key.PRIVATE_KEY_STRING[l[0]-2]) == l[1] for l in clause])


            clause = cnf_to_neg_anf(clause)
            # print("CLAUSE AFTER CONVERTING TO ANF", clause)
            # print("DECRYPT AFTER CONVERTING to ANF", decrypt(key.PRIVATE_KEY_STRING, clause))
            # clause = clause + [(1,)]  # !a = a^1
            # print("DECRYPT AFTER NEGATING", decrypt(key.PRIVATE_KEY_STRING, clause))
            

            # print("!C in ANF", clause) # ANF

            # print("R in ANF", random) # ANF

            summand = list(cartesian(clause, random))
            summand = [set(flatten(*t)) for t in summand]
            summand = list(map(lambda t: tuple(filter(lambda t: t != 1, t)), summand))
            summand = set(Counter(summand).items())

            summand = filter(lambda t: t[1] % 2 == 1, summand)
            summand = list(map(lambda t: t[0], summand))

            cipher.append(summand)

    beta_sets_file.close()
    print(cipher)
    cipher = np.fromiter([np.sort(t, axis=0) for t in flatten(*cipher)], dtype=object)

    ### SORT

    cipher = sorted(
        cipher, key=lambda term: [p(term) for p in CIPHER_SORTING_ORDER], reverse=True
    )

    ### WRITE TO FILES
    filepath = f"data/cipher_{args.count}_dir/priv_{args.count}.txt"
    with open(filepath, "w") as file:
        file.write(key.PRIVATE_KEY_STRING)

    vlen_dtype = h5py.vlen_dtype(np.dtype("float64"))

    filepath = f"data/cipher_{args.count}_dir/cipher_{args.count}.hdf5"
    with h5py.File(filepath, "w") as file:
        pass
        dset = file.create_dataset(
            name="expression", shape=(len(cipher),), dtype=vlen_dtype
        )
        dset[:] = cipher

    print(cipher)
    # print(decrypt(key.PRIVATE_KEY_STRING, cipher))


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
