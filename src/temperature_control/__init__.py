import pathlib
import sys

# temporarily add this module's directory to PATH
_temperature_base_path = pathlib.Path(__file__).parent.absolute()
sys.path.append(str(_temperature_base_path))

# remove unneeded names from namespace
del pathlib, sys