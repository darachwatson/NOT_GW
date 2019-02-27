#!/opt/local/bin/python

## LVC_probs.py bayestar_map [--prob_cutoff=0.5] [--galaxy_DB='GLADE_2.3.feather'] [--galaxy_DB_type='feather'] [--B_sun=5.31 | --K_sun=5.08])
## D. Watson 09.11.2018

# K_Abs_sun = 5.08 # http://mips.as.arizona.edu/~cnaw/sun.html (assuming Glade uses the SDSS Ks band [AB])
# B_Abs_sun = 5.31 # http://mips.as.arizona.edu/~cnaw/sun.html (assuming Glade uses the Johnson B band [AB])

from LVC_follow_up import LVC_galaxies_list
from os import path
import argparse
from warnings import warn

parser = argparse.ArgumentParser()
parser.add_argument("bayestar_map", type=str,
                    help="Healpix fits file with the LVC location probability including distances")
parser.add_argument("--prob_cutoff", type=float, default=0.5,
                    help="Cumulative probability to cut the galaxy list at(default: 0.5)")
parser.add_argument("--galaxy_DB", type=str, default='GLADE_2.3.feather',
                    help="Galaxy database file (default: \'GLADE_2.3.feather\')")
parser.add_argument("--galaxy_DB_type", type=str, default='feather',
                    help="the file type of the galaxy database (valid options are \'feather\', \'pickle\', \'hdf\', and \'ascii\'; default: \'feather\')")
parser.add_argument('--B_sun',  type=float, default=5.31,
                    help="Absolute magnitude of the sun in the B band (default: 5.31)")
parser.add_argument('--K_sun', type=float, default=5.08,
                    help="Absolute magnitude of the sun in the K band (default: 5.08)")
parser.add_argument('-v', '--verbose', action='store_true',
                    help="print output filenames")
args = parser.parse_args()

if not path.exists(args.bayestar_map):
    parser.error("The file %s does not exist!" % args.bayestar_map)

if not path.exists(args.galaxy_DB):
    parser.error("The file %s does not exist!" % args.galaxy_DB)

galaxies_B, galaxies_K = LVC_galaxies_list.gal_list(input_config_list_file=args.bayestar_map,
                    prob_cutoff=args.prob_cutoff,
                    galaxy_DB=args.galaxy_DB,
                    galaxy_DB_type=args.galaxy_DB_type,
                    B_abs_sun=args.B_sun,
                    K_abs_sun=args.K_sun)

print(galaxies_B, galaxies_K)
