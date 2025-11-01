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
    def __init__(self,v):
        self.v = v

    def __repr__(self):
        return f"Coefficient(v={self.v})"

def recover_beta_literals(filename):
    with h5py.File(filename, "r") as file:
        if "expression" in file:

            ciphertext = file["expression"]
            ciphertext = np.array(ciphertext[:])
            ciphertext = map(tuple, ciphertext)

            lengths = map(len, ciphertext)

            ciphertext = zip(ciphertext, lengths)
            ciphertext, _ = zip(
                *filter(lambda x: x[1] > TERM_LENGTH_CUTOFF, ciphertext)
            )
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
                beta_literals_sets.append(sorted(np.array([int(l) for l in s])))
            return beta_literals_sets


def recover_plaintext(beta_literals_sets, clauses):

    def distribute(iterable):  # from itertools powerset recipe
        return flatten.from_iterable(
            subset(iterable, r) for r in range(1, len(iterable) + 1)
        )

    for beta_literals_set in beta_literals_sets:

        all_clauses = np.array(ast.literal_eval(clauses))

        possible_clauses = np.fromiter(
            filter(
                lambda c: all(map(lambda l: l in beta_literals_set, list(zip(*c))[0])),
                all_clauses,
            ),
            dtype=list,
        )
        if len(possible_clauses) < ALPHA:
            raise ValueError(f"<{ALPHA} clauses found")
        
        v__cnf_to_neg_anf = np.vectorize(cnf_to_neg_anf)

        # print(beta_literals_set)
        c = v__cnf_to_neg_anf(possible_clauses)
        
        for C_i in c:
            

            C_i = np.fromiter(C_i, dtype=object)
            # print("C_i", C_i)
            R_i_all_terms = np.fromiter(distribute(beta_literals_set), dtype=object) # ANF of all possible beta terms that random chooses from
            # R_i_all_coefficients = np.arange(len(R_i_all_terms)) # a vector of variables to solve for
            R_i_all_coefficients = map(lambda i: Coefficient(i), range(len(R_i_all_terms))) # a vector of variables to solve for


            R_i_terms = np.fromiter(zip(R_i_all_coefficients, R_i_all_terms), dtype=object)

            C_iR_i = cartesian(R_i_terms, C_i)

            expression = []

            for term in C_iR_i:
                #  ((np.int64(0), (11,)), (np.int64(64), np.int64(16), np.int64(15)))
                coefficient = term[0][0]
                literals = tuple(sorted(set(term[0][1] + term[1])))
                full_term = (coefficient, literals)
                # print((coefficient, literals))
                expression.append(full_term)
                # print(expression)
                # np.append(expression, (coefficient, literals))
                # print(len(expression))

            # print("C_i \n", C_i)
            # print("R_i_terms \n", R_i_terms)
            # print("C_iR_i \n", np.fromiter(C_iR_i, dtype=object))

            final_expression = defaultdict(list)

            for e in expression:
                coefficient = e[0]
                literals = e[1]
                final_expression[literals].append(coefficient)

            print(final_expression)


            
            
            




        # possible_clauses = filter()

        # print(beta_literals_set)
        # # M_C = np.fromiter(distribute(beta_literals_set), dtype=tuple) # all possible monomials for the clauses
        # # C = np.zeros(len(M)) # indicates which monomials are used in the clause (2^k = 2^3 maximum)

        # M_R = np.fromiter(distribute(beta_literals_set), dtype=tuple)
        # print(M_R)
        # # R = np.arange(len(M))


def codebreak(n):
    hdf5_filename = f"{os.environ.get("DATA_DIRECTORY")}/cipher_{n}_dir/cipher_{n}.hdf5"
    clause_filename = (
        f"{os.environ.get("DATA_DIRECTORY")}/cipher_{n}_dir/clauses_{n}.txt"
    )

    with open(clause_filename, "r") as file:
        beta_literals_sets = recover_beta_literals(hdf5_filename)
        clauses = file.read()
        print(beta_literals_sets)
        y = recover_plaintext(beta_literals_sets, clauses)


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
