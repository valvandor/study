"""
Test config accessibility
"""
import json
import os
import sys
from pathlib import Path

sys.path.append(os.path.join(os.getcwd(), '..'))
from common.config_mixin import ConfigMixin


def test_get_default_config():
    """
    Test that default config is accessible and names 'config.json'
    """
    # ARRANGE
    cls_obj = ConfigMixin()
    root_dir = str(Path(__file__).parent.parent.resolve())

    # ACT
    path_to_default_config = cls_obj._config_file

    # ASSERT: default config should be named as 'config.json'
    assert path_to_default_config == os.path.join(root_dir, 'config.json')


def test_exist_default_config():
    """
    Test that default config is exists and is not empty
    """
    # ARRANGE
    root_dir = str(Path(__file__).parent.parent.resolve())
    config_path = os.path.join(root_dir, 'config.json')

    # ACT
    with open(config_path, 'r', encoding='utf-8') as cfg_file:
        config = json.load(cfg_file)

    # ASSERT
    assert config is not None


def test_config_options():
    """
    Test that default config contains necessary options
    """
    # ARRANGE
    root_dir = str(Path(__file__).parent.parent.resolve())
    config_path = os.path.join(root_dir, 'config.json')

    with open(config_path, 'r', encoding='utf-8') as cfg_file:
        config = json.load(cfg_file)

    # ASSERT
    assert config['listen_port'] is not None
    assert config['listen_address'] is not None
    assert config['max_connections'] is not None
    assert config['max_bytes_for_msg'] is not None
    assert config['encoding'] is not None
