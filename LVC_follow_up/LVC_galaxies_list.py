from __future__ import print_function, division
import pandas as pd
import feather
import healpy as hp
import numpy as np
from LVC_follow_up import glade_db_tools

def Mpctomodulus(distance):
    distmod = 5. * (np.log10(distance) + 5.)
    return distmod


def mynorm(x,mu,sigma):
    y = (1./(sigma*np.sqrt(2*np.pi)))*np.exp(-0.5*((x-mu)/sigma)**2.0)
    return y

def gal_list(input_config_list_file,
             prob_cutoff,
             galaxy_DB,
             galaxy_DB_type,
             B_abs_sun,
             K_abs_sun):

    hP, header = hp.read_map(input_config_list_file, h=True, verbose=False, field=0)
    hD = hp.read_map(input_config_list_file, h=False, verbose=False, field=1)
    hD_sig = hp.read_map(input_config_list_file, h=False, verbose=False, field=2)

    if galaxy_DB_type=='ascii':
        GLADE_DF = glade_db_tools.glade_to_df(galaxy_DB)
    elif galaxy_DB_type=='feather':
        GLADE_DF = feather.read_dataframe(galaxy_DB)
    elif galaxy_DB_type=='pickle':
        GLADE_DF = pd.read_pickle(galaxy_DB)
    elif galaxy_DB_type=='hdf':
        GLADE_DF = pd.read_hdf(galaxy_DB)
    else:
        ValueError("galaxy_DB_type must be one of \'ascii\', \'feather\', \'pickle\', or \'hdf\'")

    pix_probs = hp.pixelfunc.get_interp_val(hP, GLADE_DF['RA'], GLADE_DF['Dec'],lonlat=True)
    pix_Ds = hp.pixelfunc.get_interp_val(hD, GLADE_DF['RA'], GLADE_DF['Dec'],lonlat=True)
    pix_D_sigs = hp.pixelfunc.get_interp_val(hD_sig, GLADE_DF['RA'], GLADE_DF['Dec'],lonlat=True)

    GLADE_DF['LVC_prob'] = pd.Series(pix_probs, index=GLADE_DF.index)
    GLADE_DF['LVC_D'] = pd.Series(pix_Ds, index=GLADE_DF.index)
    GLADE_DF['LVC_D_sig'] = pd.Series(pix_D_sigs, index=GLADE_DF.index)

    # There is no uncertainty on most of the GLADE galaxy distances, so I have notused them
    # GLADE_DF['dist_prob'] = mynorm(GLADE_DF['dist'], GLADE_DF['LVC_D'], np.sqrt(GLADE_DF['LVC_D_sig']**2 + GLADE_DF['dist_err']**2))
    GLADE_DF['dist_prob'] = mynorm(GLADE_DF['dist'], GLADE_DF['LVC_D'], GLADE_DF['LVC_D_sig'])

    GLADE_DF['B_abs_mag'] = GLADE_DF['B']-Mpctomodulus(GLADE_DF['dist'])
    GLADE_DF['Mstar_B'] = 10**((B_abs_sun - GLADE_DF['B_abs_mag'])*0.4)
    GLADE_DF['raw_total_prob_B'] = GLADE_DF['dist_prob']*GLADE_DF['LVC_prob']*GLADE_DF['Mstar_B']
    GLADE_DF['norm_total_prob_B'] = GLADE_DF['raw_total_prob_B']/GLADE_DF['raw_total_prob_B'].sum()

    GLADE_DF['K_abs_mag'] = GLADE_DF['K']-Mpctomodulus(GLADE_DF['dist'])
    GLADE_DF['Mstar_K'] = 10**((K_abs_sun - GLADE_DF['K_abs_mag'])*0.4)
    GLADE_DF['raw_total_prob_K'] = GLADE_DF['dist_prob']*GLADE_DF['LVC_prob']*GLADE_DF['Mstar_K']
    GLADE_DF['norm_total_prob_K'] = GLADE_DF['raw_total_prob_K']/GLADE_DF['raw_total_prob_K'].sum()


    gal_catalog_B = GLADE_DF.sort_values('norm_total_prob_B', ascending=False).reset_index()
    gal_catalog_B['cum_norm_total_prob_B'] = gal_catalog_B['norm_total_prob_B'].cumsum()

    gal_catalog_K = GLADE_DF.sort_values('norm_total_prob_K', ascending=False).reset_index()
    gal_catalog_K['cum_norm_total_prob_K'] = gal_catalog_K['norm_total_prob_K'].cumsum()

    cut_B = (gal_catalog_B['cum_norm_total_prob_B'].searchsorted(prob_cutoff))[0] + 1
    cut_K = (gal_catalog_K['cum_norm_total_prob_K'].searchsorted(prob_cutoff))[0] + 1
    return gal_catalog_B[:cut_B], gal_catalog_K[:cut_K]

# glade_to_binary(glade_file,feather_file,binary_format='feather')
# glade_to_binary(glade_file,pickle_file,binary_format='pickle')
