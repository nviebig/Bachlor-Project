import matplotlib.pyplot as plt
from astropy.visualization import astropy_mpl_style
from astropy.utils.data import get_pkg_data_filename, download_file
from astropy.io import fits
import glob
from matplotlib import colors,cm
import matplotlib as mpl
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as tck
import os
import astropy.units as u


def cart_to_polar(xy):
    '''
    Convert xy separations into offset, theta

    Parameters
    ----------
    xy : list of floats
        X and Y separation in arcsec

    Returns
    -------
    r : float
        radius offset in arcsec
    theta : float
        angular position, degrees
    '''
    r = np.sqrt(xy[0] ** 2 + xy[1] ** 2)  # radius, arcsec
    theta = np.rad2deg(np.arctan2(xy[1], xy[0]))  # angle, degrees
    return r, theta


def polar_to_cart(r, theta):
    '''
    Convert from polar to cartesian, assuming theta in degrees

    Parameters
    ----------
    r : float
        radius offset in arcsec
    theta : float
        angular position, degrees

    Returns
    -------
    xy : list of floats
        X and Y separation in arcsec

    '''
    x = r * np.cos(np.deg2rad(theta))
    y = r * np.sin(np.deg2rad(theta))

    return np.array([x, y])

def plot_fits(path,colormap,numb):
    image_file = get_pkg_data_filename(path)
    fits.info(image_file)
    image_data = fits.getdata(image_file)
    plt.figure()
    data = image_data[numb,:,:]
    im = plt.imshow(data,cmap=colormap)
    clb = plt.colorbar(im)
    clb.set_label("Flux density [mJ/pixel]")
    plt.xlabel("RA[arcsec]")
    plt.ylabel("DEC[arcsec]")
    plt.savefig("./Plots/Coronographic_image"+str(numb)+".png")
    plt.show()

def show_outputs(MIRISim_outputdir, output_type):
    """
    Plot the specified channel of the MIRISim outputs
    :param MIRISim_outputdir:
        name of the date-labelled dir. holding the MIRISIM outputs
    :param output_type:
        type of output to process
        (e.g. illum_models, det_images or skycubes)
    """
    infits = glob.glob('{}/{}/*.fits'.format(MIRISim_outputdir, output_type))[0]
    hdulist = fits.open(infits)

    if output_type.lower() == 'skycubes':
        hdu_index = 0
        datashape = hdulist[hdu_index].data.shape
        central_chan = datashape[0] // 2
        plt.imshow(hdulist[hdu_index].data[central_chan, :, :],
                   origin='lower', interpolation='nearest', cmap=cm.viridis)
        plt.title('channel {} of {}'.format(central_chan, infits.split('/')[-1]))
        plt.xlabel(hdulist[hdu_index].header['ctype1'])
        plt.ylabel(hdulist[hdu_index].header['ctype2'])

        print('skycubes')

    else:
        hdu_index = 1
        if len(hdulist[hdu_index].data.shape) > 3:

            integ, frames, nx, ny = hdulist[hdu_index].data.shape
            image = hdulist[hdu_index].data[integ - 1, frames - 1, :, :]

            integ, frames, nx, ny = hdulist[hdu_index].data.shape
            image = hdulist[hdu_index].data[integ - 1, frames - 1, :, :]

            norm = colors.LogNorm(image.mean() + 0.5 * image.std(), image.max(), clip=True)
            plt.imshow(image, origin='lower', cmap=cm.viridis, interpolation='nearest', norm=norm)
            plt.xlabel("'RA' Direction")
            plt.ylabel("'DEC' Direction")

        else:
            image = hdulist[hdu_index].data[0, :, :]

            norm = colors.LogNorm(image.mean() + 0.5 * image.std(), image.max(), clip=True)
            plt.imshow(image, origin='lower', cmap=cm.viridis, interpolation='nearest', norm=norm)
            plt.xlabel("'RA' Direction")
            plt.ylabel("'DEC' Direction")


        
        plt.title('{}'.format(infits.split('/')[-1]))
        plt.savefig("./Plots/" + '{}'.format(infits.split('/')[-1] + ".png"))
        plt.show()
def plot_source_spectra(scene, sources='all', title='', newfig=True,location="Plots"):
    '''
    Produce a plot of the spectra of sources within a scene.

    Parameters
    ----------
    sources : str / list of strings
        List of source names, or 'all' to plot all source spectra
    title : str
        Title of plot
    newfig : bool
        Start a new figure, default is True
    '''
    if newfig:
        plt.figure(figsize=(12, 8))
        ax = plt.subplot(111)
    for s in scene.pandeia_scene:
        if s['pancake_parameters']['name'] in sources or sources == 'all':
            ax.plot(s['spectrum']['sed']['spectrum'][0], s['spectrum']['sed']['spectrum'][1],
                    label=s['pancake_parameters']['name'])
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlim(0.5, 30)
    ax.set_ylim(1e-3, None)
    ax.set_title(title, y=1.1, fontsize=25)
    ax.tick_params(which='both', direction='in',labelsize=20, axis='both', top=True, right=True)
    ax.xaxis.set_ticklabels([], minor=True)
    ax.xaxis.set_major_formatter(tck.FormatStrFormatter('%g'))
    ax.xaxis.set_minor_locator(
        tck.FixedLocator([0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 20, 30]))
    ax.xaxis.set_major_locator(tck.FixedLocator([0.6, 1, 2, 3, 4, 5, 6, 8, 10, 15, 20, 28]))
    ax.set_xlabel('Wavelength ($\mu$m)', fontsize=25)
    ax.set_ylabel('Spectral Flux Density (mJy)', fontsize=25)
    ax.legend(numpoints=5, loc='lower left',prop={'size': 25})
    plt.savefig("./"+location+"/source_spectra"+".png")
    plt.show()

def plot_scene(scene, title='', newfig=True, location="Plots"):
    '''
    Plot the scene and its sources spatially.

    Parameters
    ----------
    title : str
        Title of plot
    newfig : bool
        Start a new figure, default is True
        :param location:
    '''

    if newfig:
        plt.figure(figsize=(5, 5))
        ax = plt.subplot(111, projection='polar')
    for s in scene.pandeia_scene:
        r, theta = cart_to_polar([s['position']['x_offset'], s['position']['y_offset']])
        theta -= 90  # As we use the y-axis as theta=0, not x
        ax.plot(np.deg2rad(theta), r, lw=0, marker='o', ms=10, label=s['pancake_parameters']['name'])
    ax.set_rmin(0)  # Centre the scene at 0,0
    ax.set_title(title, y=1.1, fontsize=14)
    ax.legend(numpoints=1, loc='best', framealpha=1)
    ax.set_theta_offset(np.pi / 2)
    plt.savefig("./" + location + "/plot_scene" + ".png")
    plt.show()


def create_fits_for_skycube(fits_file_path):
    image_file = get_pkg_data_filename(fits_file_path)
    fits.info(image_file)
    image_data = fits.getdata(image_file)
    data=np.array([image_data[0,:,:],image_data[0,:,:]])
    # Index of the reference pixel
    crpix = (1, 1, 1) # Starts at 1
    # Value of the reference pixel
    # Axis 1 & 2 are in ra,dec ; Axis 3 is in micron
    crval = (0., 0., 10)
    cdelt = (0.11, 0.11, 2)
    hdu = fits.PrimaryHDU(data)
    hdu.header['CRVAL1'] = crval[0]
    hdu.header['CRPIX1'] = crpix[0]
    hdu.header['CDELT1'] = cdelt[0]
    hdu.header['CTYPE1'] = "RA---TAN"
    hdu.header['CUNIT1'] = u.arcsec.to_string()
    hdu.header['CRVAL2'] = crval[1]
    hdu.header['CRPIX2'] = crpix[1]
    hdu.header['CDELT2'] = cdelt[1]
    hdu.header['CTYPE2'] = "DEC--TAN"
    hdu.header['CUNIT2'] = u.arcsec.to_string()
    hdu.header['CRVAL3'] = crval[2]
    hdu.header['CRPIX3'] = crpix[2]
    hdu.header['CDELT3'] = cdelt[2]
    hdu.header['CTYPE3'] = "WAVE"
    hdu.header['CUNIT3'] = u.micron.to_string()
    hdu.header['UNITS'] = (u.microjansky / u.arcsec ** 2).to_string()
    outFileName = 'Coronographic_simulation_for_mirisim.fits'
    if os.path.isfile(outFileName):
        os.remove(outFileName)
    hdu.writeto(outFileName)

