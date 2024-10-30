import os
import configparser

config = configparser.RawConfigParser()
config.read('Config_file.ini')
general_dic = dict(config.items("General"))
os.environ["pandeia_refdata"] = general_dic["pandeia_refdata"]
os.environ["WEBBPSF_PATH"] = general_dic["webbpsf_path"]
os.environ["PYSYN_CDBS"] = general_dic["pysyn_cdbs"]
os.environ["CDP_DIR"] = general_dic["cdp_dir"]

from mirisim.config_parser import SimConfig, SimulatorConfig, SceneConfig
from mirisim import MiriSimulation
from mirisim.skysim import Skycube
from mirisim import skysim
from astropy.io import fits
from open_fits import show_outputs,create_fits_for_skycube

import glob


def show_output(output_type):
    outputdir = sorted(glob.glob('*_*_mirisim'), key=os.path.getmtime)[-1]
    outputDirContents = os.listdir(outputdir)
    directories = [name for name in outputDirContents if os.path.isdir(os.path.join(outputdir, name))]
    files = [name for name in outputDirContents if not os.path.isdir(os.path.join(outputdir, name))]

    show_outputs(outputdir, output_type)
    infits = glob.glob('{}/det_images/*.fits'.format(outputdir))[0]
    hdulist = fits.open(infits)


def simulation():
    config = configparser.RawConfigParser()
    config.read('Config_file.ini')
    details_dict = dict(config.items("General"))
    Mirisim_dict = dict(config.items("Mirisim"))
    '''
    # ________________________________________
    hdu = fits.open(file_name + ".fits"
                    , mode='update')
    print(hdu.info())
    #import fits
    #delet second imsge
    #creste cube with

    hdu[1].header["SOURCE1"] = 'Star    '
    hdu[1].header["S1XOFF1"] = 0.002483570765056163
    hdu[1].header["S1YOFF1"] = 0.007443045263347564
    hdu[1].header["S1OFFAX"] = 1.0
    hdu[1].header["S1OFFAY"] = 1.0
    hdu[1].header["S1VGAMG"] = -0.716014222132072

    hdu[1].header["SOURCE2"] = 'Planet  '
    hdu[1].header["S2XOFF1"] = 0.002483570765056163
    hdu[1].header["S2YOFF1"] = 2.007443045263348
    hdu[1].header["S2OFFAX"] = 1.0
    hdu[1].header["S2OFFAY"] = 3.0
    hdu[1].header["S2VGAMG"] = 4.285099292173222
    hdu[1].header['CRVAL1'] = 0
    hdu[1].header['CRVAL2'] = 0
    hdu[1].header['CRVAL3'] = 10
    hdu[1].header['CRPIX1'] = 1
    hdu[1].header['CRPIX2'] = 1
    hdu[1].header['CRPIX3'] = 1
    hdu[1].header['CDELT1'] = 0.11
    hdu[1].header['CDELT2'] = 0.11
    hdu[1].header['CDELT3'] = 2
    hdu[1].header['CTYPE1'] = 'RA---TAN'
    hdu[1].header['CTYPE2'] = 'DEC--TAN'
    hdu[1].header['CTYPE3'] = 'WAVE'
    hdu[1].header['CUNIT1'] = 'arcsec'
    hdu[1].header['CUNIT2'] = 'arcsec'
    hdu[1].header['CUNIT3'] = 'micron'
    hdu.flush()
    hdu.close()
    '''

    create_fits_for_skycube('Coronographic_simulation.fits')
    scene = Skycube('Coronographic_simulation_for_mirisim.fits')
    # create Background emission object
    background = skysim.Background(level=Mirisim_dict["loglevel"],
                                   gradient=int(Mirisim_dict["gradient"]),
                                   pa=int(Mirisim_dict["pa"]))

    scene_config = SceneConfig.makeScene(loglevel=Mirisim_dict["loglevel"],
                                         background=background,
                                         targets=[scene])
    os.system('rm -fr ' + details_dict["file_name"] + '_scene_for_mirisim.ini')
    scene_config.write('./' + details_dict["file_name"] + '_scene_for_mirisim.ini')

    os.system('rm -fr ' + details_dict["file_name"] + '_scene_for_mirisim.ini')
    """
    Class SimConfig - store simulation parameters.
   
    'name': 'Default Simulation',

    # Dummy sections to prevent the algorithm to crash
    'Pointing_and_Optical_Path': {},
    'Integration_and_patterns': {},

    'Scene': 
    'filename': 'name of scene file to be used to generate sky cube.',
        
    Observation':
    'rel_obsdate': 'relative observation date (0 = launch, 1 = end of 5 yr).',
       

    'Primary_Optical_Path': {
        'POP': 'Component on which to centre, choose from MRS, IMA.',
        'ConfigPath': 'Configure the optical path (MRS sub-band or Imager mode).',
        
    'Dither_Patterns': {
            'Dither': 'Include Dithering (True/False).',
            'StartInd': 'Index of first position in dither pattern (lowest possible = 1).',
            'NDither': 'Number of Dither Positions.',
            'DitherPat': 'Name of input dither pattern file.',

        'IMA_configuration': {
            'filter': 'Imager Filter to be used.',
            'ReadDetect': 'Detector to be read out: Specify any sub-array here.',
            'Mode': "Detector read-out mode. Options are 'FAST' or 'SLOW'.",
            'Exposures': 'Number of Exposures.',
            'Integrations': 'Number of Integrations (per exposure).',
            'Frames': 'Number of frames (or groups) per integration. Note for MIRI NFrames = NGroups.',
        },

        'MRS_configuration': {
            'disperser': 'Specify grating position (SHORT, MEDIUM, LONG).',
            'detector': 'Specify Channel (SW, LW or BOTH).',
            'Mode': "Detector read-out mode. Options are 'FAST' or 'SLOW'.",
            'Exposures': 'Number of Exposures.',
            'Integrations': 'Number of Integrations (per exposure).',
            'Frames': 'Number of frames (or groups) per integration. Note for MIRI NFrames = NGroups.',
            
    'name': "Simulation",

    # Dummy sections to prevent the algorithm to crash
    'Pointing_and_Optical_Path': {},
    'Integration_and_patterns': {},


            'filename': "If no scene file is given at the command line, MIRISim looks for the name of the required"
                        " scene file here. If neither specified at the command line, nor here, MIRISim will return"
                        " an error because it has nothing to simulate."
        },

        'Observation': {
            'rel_obsdate': "Set the fraction of the nominal JWST lifetime after which the observation is taking place."
                           " This value is normalised to a nominal 5 year lifetime. This variable is used to quantify"
                           " the transmission efficiency which will slightly degrade with time."
        },

        'Primary_Optical_Path': {
            'POP': "Primary Optical Path of the observation. This sets which of the regions of the MIRI detector the"
                   " scene is to be centred on. The optical path can either be through the Imager ('IMA'), or through"
                   " the MRS ('MRS').",
            'ConfigPath': "Specification of which part of the Imager/MRS is to be used in the observation. Each"
                          " component has a different centre, and this command sets which 'centre' to observe through."
                          " Available MRS configuration paths include: 'MRS_1SHORT', 'MRS_1MEDIUM', 'MRS_2SHORT',"
                          " 'MRS_3MEDIUM', 'MRS_4SHORT', 'MRS_3SHORT', 'MRS_4MEDIUM', 'MRS_4LONG', 'MRS_1LONG',"
                          " 'MRS_2LONG', 'MRS_3LONG', 'MRS_2MEDIUM'.  Available Imager configuration paths include:"
                          " 'IMA_SUB128', 'IMA_SUB256', 'IMA_CORO1550', 'LRS_SLIT','IMA_SUB64', 'IMA_FULL',"
                          " 'LRS_SLITLESS', 'IMA_CORO1140', 'IMA_BRIGHTSKY', 'IMA_COROLYOT', 'IMA_CORO1065'.",
        },

        'Dither_Patterns': {
            'Dither': "Set whether to include dithering in the observation. If set to True, further information (such"
                      " as dither pattern) must be set.",
            'StartInd': "When using a recommended dither pattern, this specifies where in the pattern to start"
                        " dithering. Allowed values range from 1 (the starting index in the pattern file) to the last"
                        " point in the pattern file.",
            'NDither': "Number of Dither Positions to be observed. If the number of dither positions is greater than"
                       " those provided in the dither pattern profile, the sequence is restarted from dither position"
                       " 1.",
            'DitherPat': "The text file specified here sets out the dither pattern to be used. There are recommended"
                         " dither patterns each path (Imager/MRS/LRS). User specified dither patterns are not yet"
                         " implemented). The recommended dither pattern files are located in"
                         " $PATH_TO_MIRISIM/obssim/lib/data and consist of a text file with 2 columns of data"
                         " specifying the x and y coordinate offsets to take for each dither pointing.",
        },

        'IMA_configuration': {
            'filter': "Specification of which imager filter to use. The different filters are specified as: 'F1000W',"
                      " 'F1065C', 'F1130W', 'F1140C', 'F1280W', 'F1500W', 'F1550 C', 'F1800W', 'F2100W', 'F2300C',"
                      " 'F2550W','F560W','F770W','P750L'.",
            'ReadDetect': "Detector to be read out. If using the imager in a sub-array mode, specify the sub-array"
                          " here. Available sub-array modes include: 'FULL','SUB256','SUB128','SUB64', 'BRIGHTSKY'"
                          " and 'SLITLESSPRISM'.",
            'Mode': "Set whether to read out in FAST (2.775 s) or SLOW (27.75s) mode (times for full detector"
                    " read-out). FAST mode is generally used for the imager, SLOW mode for spectroscopy. See Table 4 of"
                    " Bouchet et al. 2015 (PASP, 127, 612 - MIRI PASP Paper 3) for times of sub-array modes. SLOW mode"
                    " is also most appropriate for faint objects and/or regions with low background emission. Fast mode"
                    " reads out data along rows of the detector, while slow mode reads out data along the columns.",
            'Exposures': "Number of Exposures to observe. An exposure is a set of integrations on a target in the given"
                         " detector read-out mode (i.e. FAST/SLOW).",
            'Integrations': "Number of Integrations (per exposure). An Integration is defined at the time between"
                            " detector resets (see Gordon et al. 2015, PASP 127, 696 - MIRI PASP Paper 10), and depends"
                            " on the read-out Mode (e.g. FAST or SLOW). The exposure time is set by nint x tint, where"
                            " nint is the number of integrations set here, and tint is the time of a single integration"
                            " (set by the number of frames and read mode).",
            'Frames': "Number of frames (or groups) to observe within an integration. For MIRI, there is identically"
                      " one frame per group, and thus, the number of frames and number of groups can be used"
                      " interchangeably. The number of frames x read-mode time (for FAST/SLOW) gives the integration"
                      " time (tint).",
        },

        'MRS_configuration': {
            'disperser': "Specify grating position. Each of the MRS channels is comprised of three sub-bands, specified"
                         " as 'SHORT', 'MEDIUM', and 'LONG'. The wavelength coverage of each sub-band (for each"
                         " channel) is given in Table 1 of Wells et al. 2015 (PASP, 127, 646 - MIRI PASP Paper 6) and"
                         " in the user guide.",
            'detector': "Specify observing Channel. Channels are observed in pairs; either the short wavelength"
                        " channels are simulated, or the long wavelength channels. Options include channels 1 and 2"
                        " (specified as 'SW'), channels 3 and 4 (specified as 'LW') or all channels (specified as"
                        " 'BOTH').",
            'Mode': "Set whether to read out in FAST (2.775 s) or SLOW (27.75s) mode (times for full detector"
                    " read-out). FAST mode is generally used for the imager, SLOW mode for spectroscopy. See Table 4 of"
                    " Bouchet et al. 2015 (PASP, 127, 612 - MIRI PASP Paper 3) for times of sub-array modes. SLOW mode"
                    " is also most appropriate for faint objects and/or regions with low background emission. Fast mode"
                    " reads out data along rows of the detector, while slow mode reads out data along the columns.",
            'Exposures': "Number of Exposures to observe. An exposure is a set of integrations on a target in the given"
                         " detector read-out mode (i.e. FAST/SLOW).",
            'Integrations': "Number of Integrations (per exposure).  An Integration is defined at the time between"
                            " detector resets (see Gordon et al. 2015, PASP 127, 696 - MIRI PASP Paper 10), and depends"
                            " on the read-out mode (e.g. FAST or SLOW). The exposure time is set by nint x tint, where"
                            " nint is the number of integrations set here, and tint is the time of a single integration"
                            " (set by the number of frames and read mode).",
            'Frames': "Number of frames (or groups) to observe within an integration. For MIRI, there is identically"
                      " one frame per group, and thus, the number of frames and number of groups can be used"
                      " interchangeably. The number of frames x read-mode time (for FAST/SLOW) gives the integration"
                      " time (tint).",
        }
    }
"""
    sim_config = SimConfig.makeSim(
        name=details_dict["file_name"],  # name given to simulation
        scene=Mirisim_dict["scene"],  # name of scene file to input
        rel_obsdate=float(Mirisim_dict["rel_obsdate"]),  # relative observation date (0 = launch, 1 = end of 5 yrs)
        POP=Mirisim_dict["pop"],  # Component on which to center (Imager or MRS)
        ConfigPath=Mirisim_dict["configpath"],  # Configure the Optical path (MRS sub-band)
        Dither=Mirisim_dict["dither"],  # Don't Dither
        StartInd=int(Mirisim_dict["startind"]),  # start index for dither pattern [NOT USED HERE]
        NDither=int(Mirisim_dict["ndither"]),  # number of dither positions [NOT USED HERE]
        DitherPat=Mirisim_dict["ditherpat"],  # dither pattern to use [NOT USED HERE]
        disperser=Mirisim_dict["disperser"],  # [NOT USED HERE]
        detector=Mirisim_dict["detector"],  # [NOT USED HERE]
        mrs_mode=Mirisim_dict["mrs_mode"],  # [NOT USED HERE]
        mrs_exposures=int(Mirisim_dict["mrs_exposures"]),  # [NOT USED HERE]
        mrs_integrations=int(Mirisim_dict["mrs_integrations"]),  # [NOT USED HERE]
        mrs_frames=int(Mirisim_dict["mrs_frames"]),  # [NOT USED HERE]
        ima_exposures=int(Mirisim_dict["ima_exposures"]),  # number of exposures   !change in test case! 2
        ima_integrations=int(Mirisim_dict["ima_integrations"]),  # number of integrations !change in test case! 272
        ima_frames=int(Mirisim_dict["ima_frames"]),  # number of groups (for MIRI, # Groups = # Frames)
        ima_mode=Mirisim_dict["ima_mode"],  # Imager read mode (default is FAST ~ 2.3 s)
        filter=Mirisim_dict["filter"],  # Imager Filter to use
        readDetect=Mirisim_dict["readdetect"]  # Portion of detector to read out
    )
    simulator_config = SimulatorConfig.from_default()
    mirisim = MiriSimulation(sim_config, scene_config, simulator_config)
    mirisim.run()

simulation()
show_output('det_images')
'''
#---------------------------------------------------------------------
simulation("F1065C_OBservation")
show_output('det_images')
#---------------------------------------------------------------------
simulation("F1140C_OBservation")
show_output('det_images')
#---------------------------------------------------------------------
simulation("F1550C_OBservation")
show_output('det_images')
#---------------------------------------------------------------------
simulation("F2300C_OBservation")
show_output('det_images')
#---------------------------------------------------------------------
'''
