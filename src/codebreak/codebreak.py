import argparse
from itertools import chain as flatten, product as cartesian
import os
import ast

import sys

sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)
from parameters import *


# from collections import Counter

import numpy as np
import matplotlib.pyplot as plt


def codebreak(filename):
    with open(filename, "r") as file:
        ciphertext = ast.literal_eval(file.read())

        large_terms = list(
            filter(lambda term: len(term) >= TERM_LENGTH_CUTOFF, ciphertext)
        )
        subgroup = set(large_terms[-1])
        print(subgroup)
        group = set(subgroup)

        closest = [(term, len(subgroup.difference(term))) for term in ciphertext]
        # group = list(filter(lambda term: len(subgroup.difference(term)) < 0.1, ciphertext))

        # print(group)

        # max_diff_pct = 0.5
        # max_diff = max_diff_pct * len(subgroup)

        # group = list(filter(lambda term: len(subgroup.difference(term)) < max_diff, ciphertext))
        # flattened = list(flatten(*group))

        # repeats = list(Counter(flattened).values())
        # print(repeats)

        # unique = list(Counter(repeats).keys())
        # counter = list(Counter(repeats).values())

        # unique = sorted(enumerate(unique), key=lambda x: counter[x[0]])
        # counter = sorted(enumerate(counter), key=lambda x: counter[x[0]])

        # plt.scatter(list(zip(*unique))[1], list(zip(*counter))[1], color="blue", alpha=0.7, linestyle="solid")
        # plt.show()


###

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="Encrypt",
        description="Generates ciphertext file from plaintext based on Sebastian E. Schmittner's SAT-Based Public Key Encryption Scheme",
        epilog="https://eprint.iacr.org/2015/771.pdf",
    )

    parser.add_argument("n", type=int)
    args = parser.parse_args()

    filename = (
        f"{os.environ.get("DATA_DIRECTORY_PATH")}/cipher_{args.n}/cipher_{args.n}"
    )
    codebreak(filename)
