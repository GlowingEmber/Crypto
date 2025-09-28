import h5py

with h5py.File("data/cipher_1/cipher_1.hdf5", 'r') as hf:
    
    for x in range(5):
        dset = hf['expression'][-5+x]
        print(dset)
    print("...\n")
    for x in range(5):
        dset = hf['expression'][0+x]
        print(dset)