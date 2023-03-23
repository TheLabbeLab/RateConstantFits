import numpy as np

R = 1.9872  # cal/K.mol

#Ea given in cal/mol

def Linear(Ts, a, b):
    K = a*Ts + b
    return np.log(K)

def Arrhenius(Ts, A, Ea): 
    K = A*np.exp(-Ea/(R*Ts))
    return np.log(K)


def ModArrhenius(Ts, A, n, Ea): 
    K = A*Ts**n*np.exp(-Ea/(R*Ts))
    return np.log(K)

def DoubArrhenius(Ts, A1, n1, Ea1, A2, n2, Ea2):
    K1 = A1*Ts**n1*np.exp(-Ea1/(R*Ts))
    K2 = A2*Ts**n2*np.exp(-Ea2/(R*Ts))
    K = K1 + K2
    return np.log(K) 
