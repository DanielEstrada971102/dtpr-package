# dtpr/utils/config.py
import os
import yaml
from dtpr.utils.functions import color_msg
import shutil
import warnings

class Config():
    """
    Configuration class to handle loading and setting up configurations from a YAML file.
    """
    def __init__(self, config_path):
        """
        Initializes the Config object.

        Args:
            config_path (str): The path to the configuration file.
        """
        self.path = config_path
        self._setup()

    def _setup(self):
        """
        Sets up the configuration by loading the config file and setting attributes.
        """
        config_dict = self._load_config(self.path)
        for key in config_dict.keys():
            setattr(self, key, config_dict[key])
            # Evaluate types of common_opt_args
            if key == "common_opt_args":
                for subkey in self.common_opt_args.keys():
                    self.common_opt_args[subkey]["type"] = eval(self.common_opt_args[subkey]["type"])

    def change_config_file(self, outfolder=".", config_path=".workspace/run_config.yaml"):
        """
        Changes the configuration file to a new path.

        Args:
            outfolder (str): The output folder containing the new config file.
            config_path (str): The relative path to the new config file. Default is ".workspace/run_config.yaml".
        """
        try:
            self.path = os.path.join(outfolder, config_path)
            self._setup()
        except Exception as e:
            warnings.warn(f"Error changing configuration file: {e}. Using the default configuration file.")


    @staticmethod
    def _load_config(config_path):
        """
        Loads the configuration from a YAML file.

        Args:
            config_path (str): The path to the configuration file.

        Returns:
            dict: The loaded configuration dictionary.
        """
        with open(config_path, 'r') as file:
            try:
                config = yaml.safe_load(file)    
                return config
            except yaml.YAMLError as exc:
                raise exc

run_config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "./templates/config_run_template.yaml"))
RUN_CONFIG = Config(run_config_path)


def create_workspace(outfolder):
    """
    Creates a workspace directory with necessary subdirectories and configuration files.

    Args:
        outfolder (str): The path to the output folder.
    """
    folder, workspace, config_file = validate_workspace(outfolder)

    if not folder:
        # Create the output folder
        color_msg(f"Creating output folder {outfolder}...", color="purple", indentLevel=0)
        os.system(f"mkdir -p {outfolder}")

    if not workspace:
        # Create the workspace folder
        color_msg(f"Setting workspace folder...", color="purple", indentLevel=0)
        os.system(f"mkdir -p {os.path.join(outfolder, '.workspace')}")

    if not config_file:
        # put a copy of the run_config.yaml file in the output folder
        run_config_path = os.path.join(outfolder, ".workspace/run_config.yaml")
        color_msg(f"Copying run_config.yaml file into the workspace folder...", color="purple", indentLevel=0)
        shutil.copy(RUN_CONFIG.path, run_config_path)

    color_msg(f"Workspace ready in {outfolder}", color="green", indentLevel=0)

    launch_config_cli(outfolder)

def validate_workspace(outfolder):
    """
    Validates the workspace directory structure.

    Args:
        outfolder (str): The path to the output folder.

    Returns:
        tuple: A tuple indicating the presence of the folder, workspace, and config file.
    """
    if not os.path.exists(outfolder):
        return (0, 0, 0) # no one of the required elements exists

    if not os.path.exists(os.path.join(outfolder, ".workspace/")):
        return (1, 0, 0) # Output folder does not contain a .workspace folder

    if not os.path.exists(os.path.join(outfolder, ".workspace/run_config.yaml")):
        return (1, 1, 0) # Output folder does not contain a run_config.yaml file
    
    return (1, 1, 1) # all required elements exist

def launch_config_cli(outfolder):
    """
    Launches a CLI to edit the configuration file.

    Args:
        outfolder (str): The path to the output folder.
    """
    color_msg("Do you want to edit the configuration file?", color="purple", indentLevel=1)
    anws = input(color_msg("y/n: ", color="purple", indentLevel=1, return_str=True))
    if anws == "y":
        os.system(f"vim {outfolder}/.workspace/run_config.yaml")
        color_msg("Configuration file saved.", color="green", indentLevel=1)

