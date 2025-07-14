import argparse
from itertools import chain as flatten, product as cartesian
import os

def codebreak(f):
    print(f)

###

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="Encrypt",
        description="Generates ciphertext file from plaintext based on Sebastian E. Schmittner's SAT-Based Public Key Encryption Scheme",
        epilog="https://eprint.iacr.org/2015/771.pdf",
    )

    parser.add_argument("cipher_num", type=int)
    args = parser.parse_args()

    filename = f"{os.environ.get("DATA_DIRECTORY_PATH")}{f"/cipher_{args.cipher_num}"*2}"
    codebreak(filename)
    

    