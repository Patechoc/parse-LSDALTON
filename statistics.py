#!/usr/bin/env python 

import sys, os, re, math
import numpy as np

# ============================================================================ #
# Class: DAL_input
# ============================================================================ #
class matrix(object):
    def __init__(self, matrix=[[]] ):
        self.matrix    = np.array(matrix)
        self.mean      = None
        self.stdDev    = None
        self.variance  = None
        self.rms       = None

    def __repr__(self):
        str  = '\n{mat}\n'.format(mat=np.array(self.matrix))
        str += '\navg: {mean}'.format(mean=self.mean)
        str += '\nstd: {std}'.format(std=self.stdDev)
        str += '\nvar: {var}'.format(var=self.variance)
        str += '\nRMS: {rms}'.format(rms=self.rms)
        return str

    def get_stats(self):
        self.mean      = self.get_mean()
        self.stdDev    = self.get_stdDev()
        self.variance  = self.get_variance()
        self.rms       = self.get_RMSvalue()
        return self        

    def get_mean(self):
        self.mean = np.mean(self.matrix)
        return self.mean

    def get_stdDev(self):
        # "RMS error"/"RMS deviation"  = Standard deviation
        # The standard deviation is the square root of the average of the squared
        # deviations from the mean, i.e., std = sqrt(mean(abs(x - x.mean())**2)).
        # http://docs.scipy.org/doc/numpy/reference/generated/numpy.std.html#numpy.std
        std = np.std(self.matrix)
        return std 

    def get_variance(self):
        # The variance is the average of the squared deviations from the mean,
        # i.e., var = mean(abs(x - x.mean())**2).
        # http://docs.scipy.org/doc/numpy/reference/generated/numpy.var.html#numpy.var
        var = np.var(self.matrix)
        return var

    def get_RMSvalue(self):
        # The RMS value is the square root of the average of the squared
        # elements of the matrix
        # i.e., rms = sqrt(mean(x**2)).
        rms = math.sqrt(np.mean(np.square(self.matrix)))
        return rms


# ============================================================================ #
# Testing
# ============================================================================ #
if __name__ == "__main__":
    mat01 = [[1, 2], [3, 4]]
    mat02 = np.array([[ -1.06785000e-05,   1.45020000e-06,  -8.52600000e-06],
                    [  6.38938000e-05,   5.63897000e-05,   1.76832000e-05],
                    [  4.49890000e-06,   8.60220000e-06,  -2.38490000e-06],
                    [  1.19114000e-05,   9.59500000e-06,   4.44540000e-06],
                    [ -5.69520000e-06,  -1.03279000e-05,  -1.16304000e-05],
                    [  1.04919000e-05,  -9.63280000e-06,   5.74100000e-06],
                    [  8.30830000e-06,  -8.81250000e-06,   1.19956000e-05],
                    [  3.77040000e-06,   1.52898000e-05,  -8.78300000e-06],
                    [  9.89590000e-06,  -1.03254000e-05,   2.82040000e-06],
                    [ -7.32077000e-05,   2.82500000e-06,   7.80527000e-05],
                    [  3.53762000e-05,   6.30980000e-06,   7.29110000e-06],
                    [ -4.39422000e-05,  -1.22764000e-05,   1.11221000e-05],
                    [  4.06470000e-05,  -3.64624000e-05,   2.46980000e-06],
                    [ -7.06660000e-05,   2.92506000e-05,   2.17727000e-05],
                    [ -1.42704000e-05,   4.47619000e-05,  -4.80324000e-05],
                    [ -2.59069000e-05,  -3.39819000e-05,   5.30350000e-06],
                    [ -4.57860000e-06,  -1.44038000e-05,   4.75740000e-06],
                    [  4.07596000e-05,  -9.04330000e-06,   1.24914000e-05],
                    [  3.63805000e-05,   4.97230000e-06,  -2.90822000e-05],
                    [ -2.22115000e-05,  -3.33703000e-05,  -7.52538000e-05]])
    stats = matrix(mat01).get_stats()
    print "stats\n",stats
    print stats.get_mean()
