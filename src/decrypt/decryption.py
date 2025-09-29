import h5py
import numpy as np

# from collections import defaultdict
# import matplotlib.pyplot as plt

def decrypt():
    with open("data/cipher_0_dir/priv_0.txt", "r") as file:
        priv = file.read()
        print("PRIV", priv)

        def assign(x):
            return int(priv[int(x-2)])
        v_assign = np.vectorize(assign)

        with h5py.File("data/cipher_0_dir/cipher_0.hdf5", "r") as file:
            if "expression" in file:
                expression = file.get("expression")
                expression = np.array(expression[:]) 
                
                expression = [all(v_assign(term)) for term in expression]
                expression = filter(lambda term: term, expression)
                expression = list(expression)

                size = sum(1 for _ in expression)
                
                g = size % 2

                return g



print(decrypt())
