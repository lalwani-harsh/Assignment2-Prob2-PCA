import numpy as np
import os
import pdb
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

# datasets_dir = '/Download/MNIST/Data/Here'


def one_hot(x, n):
    if type(x) == list:
        x = np.array(x)
    x = x.flatten()
    o_h = np.zeros((len(x), n))
    o_h[np.arange(len(x)), x] = 1
    return o_h


def mnist(noTrSamples=1000, noTsSamples=100, \
                        digit_range=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9], \
                        noTrPerClass=100, noTsPerClass=10):
    assert noTrSamples==noTrPerClass*len(digit_range), 'noTrSamples and noTrPerClass mismatch'
    assert noTsSamples==noTsPerClass*len(digit_range), 'noTrSamples and noTrPerClass mismatch'
    # data_dir = 'MNI'
    fd = open('MNIST/train-images-idx3-ubyte')
    loaded = np.fromfile(file=fd, dtype=np.uint8)
    trData = loaded[16:].reshape((60000, 28*28)).astype(float)

    fd = open('MNIST/train-labels-idx1-ubyte')
    loaded = np.fromfile(file=fd, dtype=np.uint8)
    trLabels = loaded[8:].reshape((60000)).astype(float)

    fd = open('MNIST/t10k-images-idx3-ubyte')
    loaded = np.fromfile(file=fd, dtype=np.uint8)
    tsData = loaded[16:].reshape((10000, 28*28)).astype(float)

    fd = open('MNIST/t10k-labels-idx1-ubyte')
    loaded = np.fromfile(file=fd, dtype=np.uint8)
    tsLabels = loaded[8:].reshape((10000)).astype(float)

    trData = trData/255.
    tsData = tsData/255.

    tsX = np.zeros((noTsSamples, 28*28))
    trX = np.zeros((noTrSamples, 28*28))
    tsY = np.zeros(noTsSamples)
    trY = np.zeros(noTrSamples)

    count = 0
    for ll in digit_range:
        # Train data
        idl = np.where(trLabels == ll)
        idl = idl[0][: noTrPerClass]
        idx = list(range(count*noTrPerClass, (count+1)*noTrPerClass))
        trX[idx, :] = trData[idl, :]
        trY[idx] = trLabels[idl]
        # Test data
        idl = np.where(tsLabels == ll)
        idl = idl[0][: noTsPerClass]
        idx = list(range(count*noTsPerClass, (count+1)*noTsPerClass))
        tsX[idx, :] = tsData[idl, :]
        tsY[idx] = tsLabels[idl]
        count += 1
    
    np.random.seed(1)
    test_idx = np.random.permutation(tsX.shape[0])
    tsX = tsX[test_idx,:]
    tsY = tsY[test_idx]

    trX = trX.T
    tsX = tsX.T
    trY = trY.reshape(1, -1)
    tsY = tsY.reshape(1, -1)
    return trX, trY, tsX, tsY


def main():
    trX, trY, tsX, tsY = mnist(noTrSamples=400,
                               noTsSamples=100, digit_range=[5, 8],
                               noTrPerClass=200, noTsPerClass=50)


    pca = PCA(n_components=10)
    trX_transformed = pca.fit_transform(trX.T)
    tsX_transformed = pca.fit_transform(trX.T)
    trx_reconstruct = pca.inverse_transform(trX_transformed)

    # Problem1- Covariance of PCA constructed data
    trX_covar = np.matmul(trX_transformed.T, trX_transformed)
    tsX_covar = np.matmul(tsX_transformed.T, tsX_transformed)
    fig, (covariance_trX, covariance_tsX) = plt.subplots(1,2)
    fig.suptitle("\nCo-variance of PCA transformed data", fontsize = 12, color = "red")
    covariance_trX.set_title("\n\n\nPCA- covariance_trX\n")
    covariance_tsX.set_title("\n\n\nPCA- covariance_tsX\n")
    covariance_trX.matshow(trX_covar)
    covariance_tsX.matshow(tsX_covar)
    plt.show()

    #Problem2 - compare original and reconstructed images
    img, DIGITS = plt.subplots(2,10)
    DIGITS[0,0].imshow(trX[:, 1].reshape(28, -1))
    DIGITS[0,1].imshow(trx_reconstruct.T[:, 1].reshape(28, -1))
    DIGITS[0, 2].imshow(trX[:, 2].reshape(28, -1))
    DIGITS[0, 3].imshow(trx_reconstruct.T[:, 2].reshape(28, -1))
    DIGITS[0, 4].imshow(trX[:, 3].reshape(28, -1))
    DIGITS[0, 5].imshow(trx_reconstruct.T[:, 3].reshape(28, -1))
    DIGITS[0, 6].imshow(trX[:, 4].reshape(28, -1))
    DIGITS[0, 7].imshow(trx_reconstruct.T[:, 4].reshape(28, -1))
    DIGITS[0, 8].imshow(trX[:, 5].reshape(28, -1))
    DIGITS[0, 9].imshow(trx_reconstruct.T[:, 5].reshape(28, -1))

    DIGITS[1, 0].imshow(trX[:, 201].reshape(28, -1))
    DIGITS[1, 1].imshow(trx_reconstruct.T[:, 201].reshape(28, -1))
    DIGITS[1, 2].imshow(trX[:, 202].reshape(28, -1))
    DIGITS[1, 3].imshow(trx_reconstruct.T[:, 202].reshape(28, -1))
    DIGITS[1, 4].imshow(trX[:, 203].reshape(28, -1))
    DIGITS[1, 5].imshow(trx_reconstruct.T[:, 203].reshape(28, -1))
    DIGITS[1, 6].imshow(trX[:, 204].reshape(28, -1))
    DIGITS[1, 7].imshow(trx_reconstruct.T[:, 204].reshape(28, -1))
    DIGITS[1, 8].imshow(trX[:, 205].reshape(28, -1))
    DIGITS[1, 9].imshow(trx_reconstruct.T[:, 205].reshape(28, -1))
    img.show()

    # plt.imshow(trx_reconstruct.T[:, 5].reshape(28, -1))

    # plt.show()
    # trY[0,5]

if __name__ == "__main__":
    main()
