import numpy as np

def calcCov(z):
    dim=z.shape[1]
    cov=(np.matmul(z,z.transpose()))/(dim-1)
    return cov

def calcCrossCov(y,z):
    dim=y.shape[1]
    crossCov=np.matmul(y,z.transpose())/(dim-1)
    return crossCov

def calcKalmanGain(crossCov,forecastCov,dataErrorCov):
    totalCov=forecastCov+dataErrorCov
    u,s,v=np.linalg.svd(totalCov)
    s=1/s
    s=np.diag(s)
    totalCovInv=np.matmul(np.matmul(u,s),u.transpose())
    tmp=np.matmul(crossCov,totalCovInv)
    return tmp