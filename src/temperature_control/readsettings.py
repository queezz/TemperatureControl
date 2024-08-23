import csv
import os
from os.path import join, expanduser

RED = "\033[1;31m"
GREEN = "\033[1;32m"
BLUE = "\033[1;34m"
RESET = "\033[0m"
GOOD = "\U00002705"
BAD = "\U0000274C"


def load_settings(path_to_file):
    """
    UPDATE: change sattings from a csv file to
    fully defined settings in a yaml file.
    """
    import yaml

    with open(path_to_file, "r") as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)


def select_settings(path_to_file="settings.yml", verbose=False):
    """
    Check if there is local settings file and
    if its version is same as current, load local one.
    """
    local_settings = join(expanduser("~"), ".temperatuer_control", "settings.yml")

    try:
        local_config = load_settings(local_settings)
        config = load_settings(path_to_file)
        if local_config["Settings Version"] == config["Settings Version"]:
            config = local_config
            if verbose:
                print(GOOD + f" Configuration file loaded:\n{local_settings}")
            return config
    except FileNotFoundError as ex:
        pass
    
    script_directory = os.path.dirname(os.path.abspath(__file__))
    absolute_path_to_file = os.path.join(script_directory, path_to_file)
    config = load_settings(absolute_path_to_file)
    if verbose:
        print(GOOD + f" Configuration file loaded:\n{os.path.abspath(path_to_file)}")

    return config


def init_configuration(settings="settings.yml", verbose=False):
    """
    Read settings.yml file, populate ADC Channels Properties,
    create datafolder if it dosn't exist.
    """
    config = select_settings(settings, verbose=verbose)
    config["Data Folder"] = init_datafolder(config)
    config["Log File Path"] = check_logfile(config)
    if verbose:
        print(GOOD + " Controlunit configuration loaded")
    return config


def check_logfile(config):
    folder = config["Data Folder"]
    logname = config["Log File"]
    logfilepath = join(folder, logname)
    if not os.path.exists(logfilepath):
        open(logfilepath, "a").close()
    return logfilepath


def init_datafolder(config, verbose=True):
    """
    Create folder for saving data, if not existing
    if datafolder starts with '~' - put the folder in home directory
    """
    foldername = config["Data Folder"]

    if foldername.startswith("~"):
        home = expanduser("~")
        foldername = home + foldername[1:]

    foldername = os.path.abspath(foldername)

    try:
        os.makedirs(foldername)
        if verbose:
            print(GOOD + f" Data folder created" + f": \n{foldername}")
    except FileExistsError:
        if verbose:
            print(GOOD + f" Data folder exists" + f": \n{foldername}")

    return foldername


if __name__ == "__main__":
    try:
        print(load_settings("settings.yml"))
    finally:
        pass
