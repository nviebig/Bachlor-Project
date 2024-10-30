import os
import configparser

config = configparser.RawConfigParser()
config.read('Config_file.ini')
general_dic = dict(config.items("General"))
os.environ["pandeia_refdata"] = general_dic["pandeia_refdata"]
os.environ["WEBBPSF_PATH"] = general_dic["webbpsf_path"]
os.environ["PYSYN_CDBS"] = general_dic["pysyn_cdbs"]
import pancake
import shutil
from open_fits import plot_fits, plot_scene, plot_source_spectra


def create_coronographic_simulation():
    if not os.path.exists("Plots"):
        os.mkdir("Plots")
        print("Directory ", "Plots", " created ")
    else:
        shutil.rmtree("Plots")
        os.mkdir("Plots")
        print("Directory ", "Plots", " recreated ")

    config_new = configparser.RawConfigParser()
    config_new.read('Config_file.ini')


    pandeia_variables = dict(config_new.items("Pandeia"))
    mirisim_varibles = dict(config_new.items("Mirisim"))

    file_star = pandeia_variables["file_star"]
    file_planet = pandeia_variables["file_planet"]

    target = pancake.scene.Scene('Target')

    target.add_source('Star', r=int(pandeia_variables["radial_position_star"]),
                      theta=int(pandeia_variables["radial_position_star"]),
                      kind='file', filename=file_star, wave_unit='micron', flux_unit='mJy')
    target.add_source('Planet', r=int(pandeia_variables["radial_position_planet"]),
                      theta=int(pandeia_variables["angular_position_star"]),
                      kind='file', filename=file_planet, wave_unit='micron', flux_unit='mJy')

    plot_scene(target, title='')
    plot_source_spectra(target, title=r'Spectra of the Star and the $10^{4}$ times dimmer planet')

    seq = pancake.sequence.Sequence()
    """
    Parameters
            ----------
            scene : pancake.Scene() object
                The scene we want to observe
            exposures: list of tuples
                The exposures we want to perform, possible formats are
                - [(FILTER, PATTERN, NGROUP, NINT),...]
                - [(FILTER, 'optimise', t_exp),...] with t_exp in seconds
            mode : str
                Observing mode, 'coronagraphy' is working, 'imaging' a future development. 
            nircam_mask : str
                The NIRCam coronagraphic mask to use, 'default' we use round masks 
            nircam_subarray : str
                NIRCam subarray to use, 'default' will use the one assigned to the chosen mask
            miri_subaray : str
                MIRI subarray to use, 'default' will use the one assigned to the chosen mask
            telescope : str
                Telescope to observe with, only 'jwst' is possible at this time.
            optimise_margin : float
                Fraction of the input t_exp that we can deviate from the overall t_exp for a given exposure
            optimize_margin : str / None
                For the Americans
            max_sat : float
                Maximum fraction of saturation to reach when optimising
            rolls : list of floats
                PA angles to observe scene at
            nircam_sgd : str / None
                NIRCam small grid dither pattern to use, if any
            miri_sgd : str / None
                MIRI small grid dither pattern to use, if any
            scale_exposures : pancake.Scene()   
                Scene to scale the provided t_exp in order to reach ~the same number of photons
            verbose : bool
                Boolean toggle for terminal printing.
    """
    if pandeia_variables["filter"] == "F2300C":
        seq.add_observation(pandeia_variables["filter"],
                            miri_subarray="masklyot",
                            exposures=[(filter,"fast",int(mirisim_varibles["ima_frames"]),int(mirisim_varibles["ima_integrations"]))])
    else:
        seq.add_observation(target,
                            exposures=[(pandeia_variables["filter"],"fast",int(mirisim_varibles["ima_frames"]),int(mirisim_varibles["ima_integrations"]))])

    seq.run(save_file="./" + general_dic["file_name"] + ".fits")
    return target

target1 = create_coronographic_simulation()
plot_fits('./'+"Coronographic_simulation"+'.fits', "viridis", 0)
plot_fits('./'+"Coronographic_simulation"+'.fits', "viridis", 1)
'''
#---------------------------------------------------------------------
target1 = create_coronographic_simulation("F1065C","F1065C_OBservation")
plot_scene(target1, title='Target Scene')
plot_source_spectra(target1, title='Target Scene: Spectra')
plot_fits('./'+"F1065C_OBservation"+'.fits', "viridis", 0)
plot_fits('./'+"F1065C_OBservation"+'.fits', "viridis", 1)
#---------------------------------------------------------------------
target2 = create_coronographic_simulation("F1140C","F1140C_OBservation")
plot_fits('./'+"F1140C_OBservation"+'.fits', "viridis", 0)
plot_fits('./'+"F1140C_OBservation"+'.fits', "viridis", 1)
#---------------------------------------------------------------------
target3 = create_coronographic_simulation("F1550C","F1550C_OBservation")
plot_fits('./'+"F1550C_OBservation"'.fits', "viridis", 0)
plot_fits('./'+"F1550C_OBservation"+'.fits', "viridis", 1)
#---------------------------------------------------------------------
target4 = create_coronographic_simulation("F2300C","F2300C_OBservation")
plot_fits('./'+"F2300C_OBservation"+'.fits', "viridis", 0)
plot_fits('./'+"F2300C_OBservation"+'.fits', "viridis", 1)
#---------------------------------------------------------------------

'''