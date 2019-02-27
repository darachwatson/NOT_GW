#! /opt/local/bin/python

from __future__ import print_function, division
import pandas as pd
import feather
import astropy.units as u
from astropy import units as u
import healpy as hp
import numpy as np


def Mpctomodulus(distance):
    distmod = 5. * (np.log10(distance) + 5.)
    return distmod



def glade_to_binary(glade_file, out_file, binary_format='hdf'):
    glade_names = ["PGC", 
                   "GWGC name", 
                   "HyperLEDA name", 
                   "2MASS name", 
                   "SDSS-DR12 name", 
                   "flag1", 
                   "RA", 
                   "Dec", 
                   "dist", 
                   "dist_err", 
                   "z", 
                   "B", 
                   "B_err", 
                   "B_Abs", 
                   "J", 
                   "J_err", 
                   "H", 
                   "H_err", 
                   "K", 
                   "K_err", 
                   "flag2", 
                   "flag3"]
    DF = pd.read_csv(glade_file, sep="\s+", engine='python', names=glade_names)
    if binary_format=='hdf':
        DF.to_hdf(out_file, 'test', mode='w')
        return
    elif binary_format=='pickle':
        DF.to_pickle(out_file)
        return
    elif binary_format=='feather':
        DF.to_feather(out_file)
        return
    else: 
        return -1


def glade_to_df(glade_file):
    glade_names = ["PGC", 
                   "GWGC name", 
                   "HyperLEDA name", 
                   "2MASS name", 
                   "SDSS-DR12 name", 
                   "flag1", 
                   "RA", 
                   "Dec", 
                   "dist", 
                   "dist_err", 
                   "z", 
                   "B", 
                   "B_err", 
                   "B_Abs", 
                   "J", 
                   "J_err", 
                   "H", 
                   "H_err", 
                   "K", 
                   "K_err", 
                   "flag2", 
                   "flag3"]
    DF = pd.read_csv(glade_file, sep="\s+", engine='python', names=glade_names)
    return DF


# filename = 'bayestar_gstlal_C01.fits.gz'
filename = 'bayestar-HLV.fits.gz'
hpx, header = hp.read_map(filename, h=True, verbose=False);

# glade_file = 'GLADE_2.3.txt'
# glade_to_binary(glade_file,feather_file,binary_format='feather')


feather_file = 'GLADE_2.3.feather'
GLADE_DF = feather.read_dataframe(feather_file)


# pickle_file = 'GLADE_2.3.pkl'
# glade_to_binary(glade_file,pickle_file,binary_format='pickle')

# GLADE_DF = pd.read_pickle(pickle_file)


pix_probs = hp.pixelfunc.get_interp_val(hpx, GLADE_DF['RA'], GLADE_DF['Dec'],lonlat=True)


GLADE_DF['LVC_prob'] = pd.Series(pix_probs, index=GLADE_DF.index)
GLADE_DF['K_Abs'] = GLADE_DF['K']-Mpctomodulus(GLADE_DF['dist'])
K_Abs_sun = 5.08 # http://mips.as.arizona.edu/~cnaw/sun.html (assuming Glade uses the SDSS Ks band)
GLADE_DF['Mstar'] = 10**((K_Abs_sun - GLADE_DF['K_Abs'])*0.4)
GLADE_DF['prob'] = (GLADE_DF['LVC_prob']*GLADE_DF['Mstar'])
LVC_dist = 50 # LVC distance estimate
mass_loc_cutoff = 1e5
cut = (GLADE_DF['dist'] < LVC_dist) & (GLADE_DF['prob'] > mass_loc_cutoff)

print(GLADE_DF.loc[cut].sort_values(by='prob'))
