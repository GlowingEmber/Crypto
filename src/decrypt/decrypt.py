import h5py
import numpy as np

def decrypt():

    with open("data/cipher_0_dir/priv_0.txt", "r") as file:

        priv = file.read()

        with h5py.File("data/cipher_0_dir/cipher_0.hdf5", "r") as file:
            
            if "expression" in file:

                def assign(x):
                    x = int(x)
                    if x == 1:
                        return x
                    return int(priv[x - 2])

                v_assign = np.vectorize(assign)

                v_assign_conditional = lambda term: v_assign(term) if len(term) > 0 else []

                expression = file["expression"]
                expression = np.array(expression[:])

                expression = [all(v_assign_conditional(term)) for term in expression]
                expression = filter(lambda term: term, expression)
                expression = list(expression)

                size = sum(1 for _ in expression)

                g = size % 2

                return g


g_decryption = decrypt()
with open("data/cipher_0_dir/plain_0.txt", "r") as file:
    
    y = int(file.read())
    res = {
        0: "SUCCESS",
        1: "FAILURE"
    }
    print(f"{res[g_decryption]}: y={y}, g(priv)={y ^ g_decryption}")