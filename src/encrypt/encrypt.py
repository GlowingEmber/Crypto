import sys
import os
import key
import argparse
import secrets
from itertools import chain as flatten, combinations as subset, product as cartesian
from collections import Counter


import numpy as np
import h5py

from parameters import *

sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)
secure = secrets.SystemRandom()


def distribute(iterable):
    s = list(iterable)
    return flatten.from_iterable(subset(s, r) for r in range(1, len(s) + 1))


def simplify_cnf_to_anf(term):

    term.discard(1)  # a*1=a
    if 0 in term:
        return [0]  # a*0=0
    return term


# def cartesian_remove_1s(*iterables):

#     pools = [tuple(pool) for pool in iterables]

#     result = [[]]
#     for pool in pools:
#         result = [
#             x + [y] if y > 1 else x for x in result for y in pool
#         ]  # remove redundancy: a*1=a

#     for prod in result:
#         yield tuple(prod)

# modified itertools.product method
# def distribute(*iterables):

#     pools = [tuple(pool) for pool in iterables]

#     result = [[]]
#     for pool in pools:
#         result = [
#             x + [y] for x in result for y in pool
#         ]

#     for prod in result:
#         yield tuple(prod)


def cnf_to_anf(term):

    term = [(l[0], l[1] ^ 1) for l in term] # a = a xor 0; !a = a xor 1
    term = cartesian(*term)
    term = filter(lambda t: 0 not in t, term)
    term = map(lambda t: tuple(filter(lambda t: t != 1, t)), term)
    term = list(term)

    return term


def encrypt():
    J_MAP = [secure.sample(range(1, M), ALPHA) for _ in range(BETA)]
    CLAUSES = key.generate_clause_list()

    print(CLAUSES.data)

    cipher = []

    beta_sets_file = open(f"data/cipher_{args.count}_dir/map_{args.count}.txt", "w")

    for a in range(BETA):

        beta_clauses_list = [CLAUSES.data[r] for r in J_MAP[a]]
        beta_literals_list = [l[0] for l in flatten(*beta_clauses_list)]
        beta_counts_set = set(Counter(beta_literals_list).items())

        beta_sets_file.write(str(f"{beta_counts_set}\n"))

        for i in range(ALPHA):

            ### CREATE CLAUSE C_J(i,a)

            # includes parity: {(x_1, p_1),(x_2, p_2),(x_3, p_3)}
            clause = CLAUSES.data[J_MAP[a][i]]

            # excludes parity: {x_1, x_2, x_3}
            clause_literals_set = set([l[0] for l in clause])

            ### CREATE RANDOM R_(i,a)

            beta_literals_subset = filter(
                lambda t: t[0] not in clause_literals_set or t[1] >= 2, beta_counts_set
            )

            # all literals in {c_J(i,b) | b != a}
            beta_literals_subset = set([l[0] for l in beta_literals_subset])
            random = list(
                filter(lambda _: secure.choice([True, False]), beta_literals_subset)
            )
            random = [(t, secure.choice([0, 1])) for t in random]

            ### CREATE SUMMAND

            print("CLAUSE CNF --    ", clause)
            clause = cnf_to_anf(clause)  # + [(1,)]  # XOR with one for negation
            print("CLAUSE -- ANF", clause)

            print("RANDOM CNF --    ", random)
            random = cnf_to_anf(random)
            print("RANDOM ANF --    ", random)

            
            summand = list(cartesian(clause, random))
            print("SUMMAND ANF unflattened --   ", summand)

            summand = [list(set(flatten(*t))) for t in summand]
            print("SUMMAND ANF --   ", summand)

            cipher.append(summand)


    beta_sets_file.close()

    cipher = np.fromiter([np.sort(t, axis=0) for t in flatten(*cipher)], dtype=object)

    ### SORT

    cipher = sorted(
        cipher, key=lambda term: [p(term) for p in CIPHER_SORTING_ORDER], reverse=True
    )
    # cipher = [[args.plaintext], [1]] + cipher
    cipher_term_lengths = [len(t) for t in cipher]

    ### WRITE TO FILES
    filepath = f"data/cipher_{args.count}_dir/priv_{args.count}.txt"
    with open(filepath, "w") as file:
        file.write(key.PRIVATE_KEY_STRING)

    vlen_dtype = h5py.vlen_dtype(np.dtype("float64"))

    filepath = f"data/cipher_{args.count}_dir/cipher_{args.count}.hdf5"
    with h5py.File(filepath, "w") as file:
        dset = file.create_dataset(
            name="expression", shape=(len(cipher),), dtype=vlen_dtype
        )
        dset[:] = cipher

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
