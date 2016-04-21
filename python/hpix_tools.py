"""
Small routine to convert from RA,DEC to HEALPIX pixel indices to
be ingested in the DB
"""
import argparse
import fitsio
import healpy
import numpy


def main():
    """
    This main function will read arguments from the command line including input and output filenames,
    names of the index, ra and dec columns and nside parameter for healpix

    Usage:
    hpixDB -i <file.fits> -o <output.fits> --columns index,ra,dec

    Optional:
    --nside <number> is the nside use for healpix (12*nside*nside number of pixels)
    --hpix_col <name> name of the output column for the indices

    This will generate a fits file with 2 a index column and healpix column with indices
    """
    parser = argparse.ArgumentParser(
        description="Creates Healpix indices for RA,DEC pair taken from a file",
        prog="hpixDB",
        usage='%(prog)s [-h] -i INPUT -o OUTPUT -c COLUMNS [--nside NSIDE] [--hpix_col HPIX_COL]',
        add_help=True)
    required_args = parser.add_argument_group('required named arguments')
    required_args.add_argument("-i", "--input", type=str, action="store", default=None, required=True,
                               help="The name of the input file")
    required_args.add_argument("-o", "--output", type=str, action="store", default=None, required=True,
                               help="The name of the output file")
    required_args.add_argument("-c", "--columns", type=str, action="store",
                               default="NUMBER,ALPHAWIN_J2000,DELTAWIN_J2000",
                               help="The name of the 3 columns used separated by comas, \
                               e.g.: NUMBER,RA,DEC, default=NUMBER,ALPHAWIN_J2000,DELTAWIN_J2000")
    optional_args = parser.add_argument_group('optional named arguments')
    optional_args.add_argument("--nside", type=int, action="store", default=16384,
                               help="Nside value for Healpix, has to be a power of 2")
    optional_args.add_argument("--hpix_col", type=str, action="store", default="HPIX",
                               help="The name of the healpix indices column in the output file")
    args = parser.parse_args()

    index_col, ra_col, dec_col = "".join(args.columns.split()).split(',')
    nside = args.nside
    hpix_col = args.hpix_col
    index_col = index_col.upper()
    ra_col = ra_col.upper()
    dec_col = dec_col.upper()
    # Read 3 columns from input data
    data_in = fitsio.read(args.input, columns=[index_col, ra_col, dec_col])
    # Convert to radians
    phi = data_in[ra_col]/180.*numpy.pi
    theta = (90. - data_in[dec_col])/180.*numpy.pi
    # Healpix indices
    pixs = healpy.ang2pix(nside, theta, phi, nest=True)
    nrows = len(phi)
    # Create Data Array for output
    data_out = numpy.zeros(nrows, dtype=[(index_col, 'i8'), (hpix_col, 'i8')])
    data_out[index_col] = data_in[index_col]
    data_out[hpix_col] = pixs
    # Write fits file
    fitsio.write(args.output, data_out, clobber=True)

