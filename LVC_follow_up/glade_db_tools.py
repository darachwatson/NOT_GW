import pandas as pd

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
