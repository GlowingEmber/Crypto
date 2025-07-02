from parameters import *
import key_generation as key_generation
import argparse
import secrets
secure = secrets.SystemRandom()

def random_function(row): # Generates in ANF
    terms = list(filter(lambda _: secure.choice([True, False]), row))
    return terms

def encrypt():
    J_MAP = [secure.sample(range(1, M), BETA) for _ in range(BETA)] # len(J_map) is BETA
    CLAUSES = key_generation.generate_clause_list()
    print(CLAUSES.form)

    for i in range(ALPHA):
        for a in range(BETA):
            R_selection = random_function(J_MAP[a])
            print([CLAUSES.data[r] for r in R_selection])

###

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='Encrypt',
        description='Generates ciphertext file from plaintext based on Sebastian E. Schmittner\'s SAT-Based Public Key Encryption Scheme',
        epilog='https://eprint.iacr.org/2015/771.pdf'
    )
    parser.add_argument("-y, --plaintext", choices=[1, 0], type=int, default=1, nargs="?")
    parser.add_argument("-c", "--count", type=int, default=1, nargs="?")
    args = parser.parse_args()

    for cnt in range(args.count):
        encrypt()