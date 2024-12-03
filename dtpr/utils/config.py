# dtpr/utils/config.py
import os
import yaml
import warnings


class Config:
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
                    self.common_opt_args[subkey]["type"] = eval(
                        self.common_opt_args[subkey]["type"]
                    )

    def change_config_file(
        self, outfolder=".", config_path=".workspace/event_config.yaml"
    ):
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
            warnings.warn(
                f"Error changing configuration file: {e}. Using the default configuration file."
            )

    @staticmethod
    def _load_config(config_path):
        """
        Loads the configuration from a YAML file.

        Args:
            config_path (str): The path to the configuration file.

        Returns:
            dict: The loaded configuration dictionary.
        """
        with open(config_path, "r") as file:
            try:
                config = yaml.safe_load(file)
                return config
            except yaml.YAMLError as exc:
                raise exc


event_config_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "./templates/event_config_template.yaml")
)
EVENT_CONFIG = Config(event_config_path)
