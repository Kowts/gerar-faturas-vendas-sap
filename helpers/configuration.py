import json

# Define a default configuration file path
CONFIG_FILE = 'configs.json'

# Load static variables from a JSON configuration file.
def load_config(config_file=None):
    """
    Args:
        config_file (str, optional): The path to the configuration file.
            If None, the default 'configs.json' will be used.

    Returns:
        dict: A dictionary containing the static variables.
    """
    if config_file is None:
        config_file = CONFIG_FILE

    try:
        with open(config_file, 'r', encoding='utf-8') as file:
            static_variables = json.load(file)
        return static_variables
    except FileNotFoundError as e:
        raise FileNotFoundError(
            f"Configuration file '{config_file}' not found."
        ) from e
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON format in '{config_file}'.") from e
