import numpy as np

# Percentage Error
def ErrorPercentage(actual, calculated, precision = 3):
    return np.round(np.sum(abs(actual - calculated)/actual)*100/len(actual), precision), np.round((actual - calculated)*100/actual, precision)
