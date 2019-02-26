
# Imports for GCN listener
import gcn
import healpy as hp
import astropy.coordinates
import astropy.time
import astropy.units as u
import numpy as np

# Here are some extra imports for the galaxy cross matching:
from astropy.table import Table, vstack, hstack, Column
import astropy.units as u
from astropy.coordinates import SkyCoord
import ligo.skymap.plot
from scipy.stats import norm
import scipy.stats

# Function to call every time a GCN is received.
# Run only for notices of type
# LVC_PRELIMINARY, LVC_INITIAL, or LVC_UPDATE.
@gcn.handlers.include_notice_types(
    gcn.notice_types.LVC_PRELIMINARY,
    gcn.notice_types.LVC_INITIAL,
    gcn.notice_types.LVC_UPDATE)
def process_gcn(payload, root):
    # Respond only to 'test' events.
    # VERY IMPORTANT! Replace with the following code
    # to respond to only real 'observation' events.
    # if root.attrib['role'] != 'observation':
    #    return
    if root.attrib['role'] != 'test':
        return

    # Read all of the VOEvent parameters from the "What" section.
    params = {elem.attrib['name']:
              elem.attrib['value']
              for elem in root.iterfind('.//Param')}

    # Respond only to 'CBC' events. Change 'CBC' to "Burst'
    # to respond to only unmodeled burst events.
    if params['Group'] != 'CBC':
        return

    # Print all parameters.
    for key, value in params.items():
        print(key, '=', value)

    if 'skymap_fits' in params:
        # Read the HEALPix sky map and the FITS header.
        skymap, header = hp.read_map(params['skymap_fits'],
                                     h=True, verbose=False)
        header = dict(header)

        # Print some values from the FITS header.
        print('Distance =', header['DISTMEAN'], '+/-', header['DISTSTD'])


        prob, distmu, distsigma, distnorm = hp.read_map(params['skymap_fits'], field=[0, 1, 2, 3])

        npix = len(prob)
        nside = hp.npix2nside(npix)
        pixarea = hp.nside2pixarea(nside)



        #load in GLADE catalog
        # GLADE=Table.read('../data/GLADE_2.3.txt', format='ascii')
        #GLADE=Table.read('LIGOcross/GLADE_20170106_galexwise_DaveUpdate.fits')
        # GLADEcoord=SkyCoord(ra=GLADE['RA']*u.deg,dec=GLADE['DEC']*u.deg)
        # nGLADE=np.size(GLADE)

def target_list(m, header):

    # Done!
    return targetlist




def main():

    import lxml.etree
    payload = open('../data/MS181101ab-1-Preliminary.xml', 'rb').read()
    root = lxml.etree.fromstring(payload)
    process_gcn(payload, root)



    # gcn.listen(handler=process_gcn)


if __name__ == '__main__':
    main()

