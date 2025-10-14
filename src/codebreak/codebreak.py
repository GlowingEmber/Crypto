import argparse
import os

import sys

sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)
from parameters import *

import h5py
import numpy as np

MAX_DIFF_PCT = 0.5

def codebreak(filename):
    with h5py.File(filename, "r") as file:
        if "expression" in file:

            ciphertext = file["expression"]
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
                    
            for x in groups:
                print(sorted([int(l) for l in x]))  

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
        f"{os.environ.get("DATA_DIRECTORY")}/cipher_{args.n}_dir/cipher_{args.n}.hdf5"
    )
    codebreak(filename)
