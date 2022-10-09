"""
Module with ConfigMixin class
"""
import json
import argparse
import sys
from os import path
from pathlib import Path


class ConfigMixin:
    """
    Mixin with for accessing to configuration file. By default searches in ../ directory for a config.json
    """

    @property
    def _config_file(self, file_name: str = 'config', file_extension: str = '.json') -> str:
        """
        Resolve path for directory with config and gets path of config file. By default, it'll be ../config.json

        Args:
            file_name: file name without file extension
            file_extension: file extension with dote

        Returns:
            path of a config file
        """
        config_dir = str(Path(__file__).parent.parent.resolve())
        return path.join(config_dir, file_name + file_extension)

    def get_config(self) -> dict:
        """
        Binds config file to executed script and loads config

        Returns:
            config as a dict
        """
        config_file = self._bind_config_file()
        with open(config_file) as f:
            return json.load(f)

    def _bind_config_file(self) -> str:
        """
        Adds an argument for config to run script and uses default if that argument is absent

        Returns:
            path to config file
        """
        parser = argparse.ArgumentParser(description='messanger service')
        parser.add_argument(
            '--config',
            help='configuration file name',
            type=str,
            default=self._config_file)

        args, _ = parser.parse_known_args()
        if not args.config:
            parser.print_usage()
            sys.exit(1)
        return args.config
