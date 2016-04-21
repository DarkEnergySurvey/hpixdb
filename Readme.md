## healpixDB

Small routine to convert from RA,DEC to HEALPIX pixel indices to
be ingested in the DB

### Use

    usage: hpixDB [-h] -i INPUT -o OUTPUT -c COLUMNS [--nside NSIDE] [--hpix_col HPIX_COL]

Creates Healpix indices for RA,DEC pair taken from a file

optional arguments:
  -h, --help            show this help message and exit

required named arguments:
  -i INPUT, --input INPUT
                        The name of the input file
  -o OUTPUT, --output OUTPUT
                        The name of the output file
  -c COLUMNS, --columns COLUMNS
                        The name of the 3 columns used separated by comas,
                        e.g.: NUMBER,RA,DEC,
                        default=NUMBER,ALPHAWIN_J2000,DELTAWIN_J2000

optional named arguments:
  --nside NSIDE         Nside value for Healpix, has to be a power of 2
  --hpix_col HPIX_COL   The name of the healpix indices column in the output file
