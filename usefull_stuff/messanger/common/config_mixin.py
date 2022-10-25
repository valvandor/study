"""
Module with ConfigMixin class
"""
import json
import argparse
import os.path
import sys
import logging
import logging.config
from os import path
from pathlib import Path

sys.path.append(os.path.join(os.getcwd(), '..'))
from common.exceptions import IncompleteConfig


class ConfigMixin:
    """
    Mixin with for accessing to configuration file. By default searches in ../ directory for a config.json
    """

    ROOT_DIR = str(Path(__file__).parent.parent.resolve())
    DEFAULT_LOG_DIR = 'test_message_app'

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
        return path.join(self.ROOT_DIR, file_name + file_extension)

    def setup_log_config(self, in_project_dir: bool = False) -> None:
        """
        Setups logging configuration

        Args:
            in_project_dir: bool value which reflect whether the logs should be stored in the project directory
        Raises:
            IncompleteConfigError: when wrong config
        """

        config = self.get_config()
        try:
            log_settings = config['logging']

            if in_project_dir:
                log_dir = path.join(self.ROOT_DIR, 'logs')
            else:  # unix-like system required
                log_dir = path.join('/var/log/', self.DEFAULT_LOG_DIR)
            if not os.path.exists(log_dir):
                os.mkdir(log_dir)

            self._set_paths_for_log_files(log_settings, log_dir)

            logging.config.dictConfig(log_settings)

        except KeyError as err:
            raise IncompleteConfig from err

    @staticmethod
    def _set_paths_for_log_files(log_settings: dict, log_dir: str) -> None:
        """
        Sets paths for handlers according to it's name

        Args:
            log_settings: settings to modify
            log_dir: directory where log files would be stored

        """
        for handler_name in log_settings['handlers'].keys():
            if handler_name == 'server':
                log_settings['handlers'][handler_name]['filename'] = os.path.join(log_dir, f'{handler_name}.log')
            if handler_name == 'client':
                log_settings['handlers'][handler_name]['filename'] = os.path.join(log_dir, f'{handler_name}.log')

            else:  # handler_name == 'console' or another one that not expected yet
                continue

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
