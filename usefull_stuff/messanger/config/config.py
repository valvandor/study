"""

"""
import argparse
import sys
from os import path
from pathlib import Path


def get_config_path(file_name: str = 'config', file_extension: str = '.json') -> str:
    """
    Resolve path for parent directory and gets path of config file. By default, it'll be ./config.json

    Args:
        file_name: file name without file extension
        file_extension: file extension with dote

    Returns:
        path of a config file
    """
    config_dir = str(Path(__file__).parent.resolve())
    return path.join(config_dir, file_name + file_extension)


def bind_config_file() -> str:
    """
    Adds an argument for config to run script and uses default if that argument is absent

    Returns:
        path to config file
    """
    config = get_config_path()

    parser = argparse.ArgumentParser(description='messanger service')
    parser.add_argument(
        '--config',
        help='configuration file name',
        type=str,
        default=config)

    args, _ = parser.parse_known_args()
    if not args.config:
        parser.print_usage()
        sys.exit(1)
    return args.config
