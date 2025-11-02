import argparse
import os
import sys
import ast

from itertools import chain as flatten, combinations as subset, product as cartesian
from collections import defaultdict

from src.encrypt.encrypt import cnf_to_neg_anf

sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)
from parameters import *

import h5py
import numpy as np

MAX_DIFF_PCT = 0.5


class Coefficient:
    def __init__(self, v):
        self.value = v

    def __repr__(self):
        return f"Coefficient(v={self.value})"


def recover_beta_literals(cipher_x_hdf5_file):
    if "expression" in cipher_x_hdf5_file:

        ciphertext = cipher_x_hdf5_file["expression"]
        ciphertext = np.array(ciphertext[:])
        ciphertext = map(tuple, ciphertext)

        lengths = map(len, ciphertext)

        ciphertext = zip(ciphertext, lengths)
        ciphertext, _ = zip(*filter(lambda x: x[1] > TERM_LENGTH_CUTOFF, ciphertext))
        ciphertext = set(ciphertext)

        groups = []

        while len(groups) < BETA:

            largest = max(ciphertext, key=len)
            group = set(largest)
            ciphertext.remove(largest)

            while True:

                closeness = map(lambda x: (x, len(group.difference(x))), ciphertext)
                closest = min(closeness, key=lambda x: x[1])

                max_diff = math.floor(MAX_DIFF_PCT * len(group))

                if closest[1] <= max_diff:
                    group = group.union(closest[0])
                    ciphertext.remove(closest[0])
                else:
                    groups.append(group)
                    group = set()
                    break

        beta_literals_sets = []
        for s in groups:
            beta_literals_sets.append(sorted([int(l) for l in s]))
        return sorted(beta_literals_sets)


def recover_plaintext(
    beta_literals_sets, clauses_x_txt_file, cipher_x_hdf5_file, map_x_txt_file
):

    clauses = clauses_x_txt_file.read()
    for x in beta_literals_sets:
        print([int(l) for l in x])

    print("----------")

    real_beta_literals_sets = ast.literal_eval(map_x_txt_file.read())
    for x in real_beta_literals_sets:
        print(x)

    def distribute(iterable):  # from itertools powerset recipe
        return flatten.from_iterable(
            subset(iterable, r) for r in range(1, len(iterable) + 1)
        )

    for beta_literals_set in beta_literals_sets:

        all_clauses = ast.literal_eval(clauses)

        possible_clauses = np.fromiter(
            filter(
                lambda c: all(map(lambda l: l in beta_literals_set, list(zip(*c))[0])),
                all_clauses,
            ),
            dtype=list,
        )
        print("possible clauses", possible_clauses)
        if len(possible_clauses) < ALPHA:
            raise ValueError(f"<{ALPHA} clauses found")
        
        R_terms = np.fromiter(distribute(beta_literals_set), dtype=object)

        n = len(R_terms)
        a = np.zeros((n,n), dtype=np.int64)
        b = np.zeros(n, dtype=np.int64)
        print("a", a)

        v__cnf_to_neg_anf = np.vectorize(cnf_to_neg_anf)
        C = v__cnf_to_neg_anf(possible_clauses)
        # C = [cnf_to_neg_anf(C_i) for C_i in possible_clauses]
        # print("hi", [list(x) for x in C])
        for C_i in C:
            #####
            C_i = np.fromiter(C_i, dtype=object)
            print(list(C_i))
            #####
            R_i_terms = R_terms
            R_i_coefficients = map(lambda i: Coefficient(i), range(len(R_i_terms)))
            R_i = np.fromiter(zip(R_i_coefficients, R_i_terms), dtype=object)

            print("C_i", C_i)
            #####
            unformatted_C_iR_i = cartesian(R_i, C_i)
            C_iR_i = []


            for term in unformatted_C_iR_i:

                coefficient = term[0][0]
                literals = tuple(sorted([int(x) for x in set(term[0][1] + term[1])]))
                full_term = (coefficient, literals)
                C_iR_i.append(full_term)

            distributed_C_iR_i = defaultdict(list)

            for term in C_iR_i:
                coefficient = term[0]
                literals = term[1]
                distributed_C_iR_i[literals].append(coefficient)


            print(distributed_C_iR_i)

            ciphertext = list(
                map(
                    lambda t: tuple(sorted([np.int64(l) for l in t])),
                    np.array(cipher_x_hdf5_file["expression"][:]),
                )
            )

            def clause_vector(coefficients, dimension):
                v = np.zeros(dimension)
                for c in coefficients:
                    v[c.value] = 1
                    # NOTE: if we are using XOR we would do v[c.value] = int(not v[c.value])
                    # whereas if we are using OR we would do v[c.value] = 1
                return v

            # m = len(distributed_C_iR_i.values())
            lhs = np.zeros((n, n), dtype=int)

            for i, row in enumerate(
                map(lambda x: clause_vector(x, n), distributed_C_iR_i.values())
            ):
                lhs[i] = row

            for x in distributed_C_iR_i.keys():
                print(x, x in ciphertext)

            rhs = map(lambda x: x in ciphertext, distributed_C_iR_i.keys())
            rhs = np.fromiter(rhs, dtype=int)
            np.set_printoptions(threshold=sys.maxsize)
            print("lhs", lhs)
            print("rhs", rhs)

        # try:
        #     sol = np.linalg.solve(lhs, rhs)
        #     print(sol)
        # except Exception as e:
        #     print(f"No solution: {e}")
        #     print(0)


def codebreak(n):
    hdf5_filename = f"{os.environ.get("DATA_DIRECTORY")}/cipher_{n}_dir/cipher_{n}.hdf5"
    clause_filename = (
        f"{os.environ.get("DATA_DIRECTORY")}/cipher_{n}_dir/clauses_{n}.txt"
    )

    with h5py.File(hdf5_filename, "r") as cipher_x_hdf5_file:
        beta_literals_sets = recover_beta_literals(cipher_x_hdf5_file)
        with open(clause_filename, "r") as clauses_x_txt_file:
            with open(f"data/cipher_{n}_dir/map_{n}.txt", "r") as map_x_txt_file:
                y = recover_plaintext(
                    beta_literals_sets,
                    clauses_x_txt_file,
                    cipher_x_hdf5_file,
                    map_x_txt_file,
                )


###

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="Encrypt",
        description="Generates ciphertext file from plaintext based on Sebastian E. Schmittner's SAT-Based Public Key Encryption Scheme",
        epilog="https://eprint.iacr.org/2015/771.pdf",
    )

    parser.add_argument("n", type=int)
    args = parser.parse_args()

    codebreak(args.n)
