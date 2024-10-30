import subprocess
import configparser
config = configparser.RawConfigParser()
config.read('Config_file.ini')
general_dic = dict(config.items("General"))
print("Program is starting")
print("#========================================================")
print("Pandeia is running")
print("#========================================================")
subprocess.call([general_dic["loc_of_pandeia"],
                 general_dic["pos_of_pandeia_results"]])
print("#========================================================")
print("Pandeia finished")
print("#========================================================")
'''
print("Mirisim is running")
print("#========================================================")
subprocess.call([general_dic["loc_of_mirisim"],
                 general_dic["pos_of_mirisim_results"]])
print("#========================================================")
print("Program finished")
print("#========================================================")

'''