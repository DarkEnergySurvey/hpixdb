"""
Small routine to convert from RA,DEC to HEALPIX pixel indices to
be ingested in the DB
"""
import argparse
import fitsio
import healpy
import numpy
import os

def main():
    """
    This main function will read arguments from the command line including input and output filenames,
    names of the index, ra and dec columns and nside(s) parameter for healpix

    Usage:
    hpixDB -i <file.fits> -o <output.fits> --columns index,ra,dec

    Optional:
    --nsides <number> is the nside(s) use for healpix (12*nside*nside number of pixels)
    --hpix_col <name> name of the output column for the indices

    This will generate a fits file with 2 a index column and healpix column with indices
    """
    parser = argparse.ArgumentParser(
        description="Creates Healpix indices for RA,DEC pair taken from a file",
        prog="hpixDB",
        usage='%(prog)s [-h] -i INPUT -o OUTPUT -c COLUMNS [--nsides NSIDE1 NSIDE2 ... NSIDEN] [--hpix_cols HPIX_COL1 HPIX_COLL2 ... HPIX_COLN]',
        add_help=True)
    required_args = parser.add_argument_group('Required named arguments')
    required_args.add_argument("-i", "--input", type=str, action="store", default=None, required=True,
                               help="The name of the input file")
    required_args.add_argument("-o", "--output", type=str, action="store", default=None, required=True,
                               help="The name of the output file")
    required_args.add_argument("-c", "--columns", type=str, action="store",
                               default="NUMBER,ALPHAWIN_J2000,DELTAWIN_J2000",
                               required=True,
                               help="The name of the 3 columns used separated by comas, \
                               e.g.: NUMBER,RA,DEC, default=NUMBER,ALPHAWIN_J2000,DELTAWIN_J2000")
    optional_args = parser.add_argument_group('Optional named arguments')
    optional_args.add_argument("--nsides", action="store", default='32, 64, 1024, 4096, 16384',
                               help="Nside(s) value for Healpix, has to be a power of 2")
    args = parser.parse_args()

    index_col, ra_col, dec_col = "".join(args.columns.split()).split(',')
    index_col = index_col.upper()
    ra_col = ra_col.upper()
    dec_col = dec_col.upper()

    # Extract nsides into an array and make them integers
    args.nsides = "".join(args.nsides.split()).split(',')
    args.nsides = [int(nside) for nside in args.nsides]

    # The filename we'll store and it format
    filename = os.path.basename(args.input)
    FILENAME_SIZE = 'S%s' % len(filename)
    
    # Read 3 columns from input data
    # We will assume that we have either SEpoch catalogs with 'LDAC_OBJECTS' format or, MEpoch with OBJECTS
    tab = fitsio.FITS(args.input)
    try:
        data_in = tab['LDAC_OBJECTS'].read(columns=[index_col, ra_col, dec_col])
    except IOError:
        data_in = tab['OBJECTS'].read(columns=[index_col, ra_col, dec_col])
    except:
        raise IOError("Could not find LDAC_OBJECTS or OBJECTS hdu on file")

    # Convert to radians
    phi = data_in[ra_col]/180.*numpy.pi
    theta = (90. - data_in[dec_col])/180.*numpy.pi

    # Create Data Array for output  before populating it
    nrows = len(phi)
    hpix_cols = ["HPIX_%s" % nside for nside in args.nsides]
    dtypes=zip(hpix_cols,['i8']*5)
    dtypes.insert(0,(index_col, 'i8'))
    dtypes.insert(1,('FILENAME', FILENAME_SIZE))
    data_out = numpy.zeros(nrows, dtype=dtypes)

    # Populate OBJECT and FILENAME needed for DB ingestion
    data_out[index_col] = data_in[index_col]
    data_out['FILENAME'] = [filename]*nrows

    # Loop over the Healpix indices we want
    for k in range(len(args.nsides)):
        nside = args.nsides[k]
        hpix_col = hpix_cols[k]
        pixs = healpy.ang2pix(nside, theta, phi, nest=True)
        data_out[hpix_col] = pixs

    # Write fits file
    fitsio.write(args.output, data_out, extname='OBJECTS', clobber=True)

