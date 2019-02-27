#!/opt/local/bin/python

## glade_ascii_to_binary.py GLADE_filename binary_output_filename --output_DB_type='feather')
## D. Watson 09.11.2018

from LVC_follow_up import glade_db_tools
from os import path
import argparse
from warnings import warn

parser = argparse.ArgumentParser()
parser.add_argument("GLADE_filename", type=str,
                    help="GLADE ascii file")
parser.add_argument('-o', "--output_filename", type=str,
                    help="Name of the output binary file")
parser.add_argument("--output_DB_type", type=str, default='feather',
                    help="the file type of the output file (valid options are \'feather\', \'pickle\', and \'hdf\'; default: \'feather\')")
parser.add_argument('-f', '--force_overwrite', action='store_true',
                    help="overwrite existing binary")
parser.add_argument('-v', '--verbose', action='store_true',
                    help="print output filenames")
args = parser.parse_args()

if not path.exists(args.GLADE_filename):
    parser.error("The file %s does not exist!" % args.bayestar_map)

if path.exists(args.output_filename) & (not args.force_overwrite):
    parser.error("The file %s already exists. Use \'-f\' to overwrite" % args.output_filename)

glade_db_tools.glade_to_binary(args.GLADE_filename,args.output_filename,binary_format=args.output_DB_type)
