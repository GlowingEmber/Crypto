import h5py
import numpy as np

# from collections import defaultdict
# import matplotlib.pyplot as plt


def decrypt():
    with open("data/cipher_0_dir/priv_0.txt", "r") as file:
        priv = file.read()

        with h5py.File("data/cipher_0_dir/cipher_0.hdf5", "r") as file:
            if "expression" in file:
                expression = file["expression"]

                # lengths = defaultdict(int)

                # for i in expression:
                #     l = len(i)
                #     lengths[l] += 1

                # plt.bar(lengths.keys(), lengths.values())
                # plt.xlabel('monomial term sizes')
                # plt.ylabel('count')
                # plt.show()

                # for term in expression:
                # parity = int(all(list(map(lambda literal: int(priv[literal-4]), term))))

                # g = g^parity

                g = 1

                for term in expression:
                    term = np.subtract(term, 2).astype(int)

                    term_parity = int(
                        all(map(lambda literal: int(priv[literal-1]), term))
                    )

                    g = g ^ term_parity
                    # print(g)

                    # if g == term_parity:
                    #     print(not g)

                    # g = g^term_parity

                    # if g_updated^g:
                    #     print(g_updated)

                    # g = g_updated
                    # 1^1 = 0
                    # 1^0 = 1
                    # 0^1 = 1
                    # 0^0 = 0

                    # if not g^parity:
                    #     print()
                    # g = g^parity

                print(g)


decrypt()
