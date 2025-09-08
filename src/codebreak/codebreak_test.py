import h5py

with h5py.File("cipher_0.hdf5", 'r') as hf:
    dset = hf['c0'][-1]
    print(dset)