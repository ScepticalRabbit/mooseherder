
'''
===============================================================================
MOOSE Config Class

Authors: Lloyd Fletcher
===============================================================================
'''
from typing import Self
import json
from pathlib import Path


class MooseConfig:
    """ _summary_
    """
    def __init__(self, config: dict[str,Path | str] | None = None) -> None:

        self._required_keys = ['main_path','app_path','app_name']

        if config is not None:
            self._check_config_valid(config)

        self._config = config


    def get_config(self) -> dict[str,Path | str]:

        self._check_config_valid(self._config)
        return self._config # type: ignore


    def _check_config_valid(self, config: dict[str,Path | str] | None = None) -> None:

        if config is None:
            raise MooseConfigError(
                'Config dictionary must be initialised, load config file first.')

        for kk in self._required_keys:
            if kk not in config:
                raise MooseConfigError(
                    f'Config dictionary must contain all keys: {self._required_keys}')

        if not config['main_path'].is_dir(): # type: ignore
            raise MooseConfigError(
                "Main path to MOOSE does not exist. Check path at key 'main_path'.")

        if not config['app_path'].is_dir(): # type: ignore
            raise MooseConfigError(
                "MOOSE app path does not exist. Check path at key: 'app_path'.")


    def convert_path_to_str(self, in_config: dict[str,Path | str] | None
                             ) -> dict[str,str] | None:

        if in_config is None:
            return None

        conv_config = dict({})
        for kk in in_config:
            conv_config[kk] = str(in_config[kk])

        return conv_config


    def convert_str_to_path(self, in_config: dict[str,str] | None = None
                             ) -> dict[str, Path | str] | None:

        if in_config is None:
            return None

        conv_config = dict({})
        for kk in in_config:
            if 'path' in kk:
                conv_config[kk] = Path(in_config[kk])
            else:
                conv_config[kk] = in_config[kk]

        return conv_config


    def save_config(self,config_path: Path) -> None:

        if not config_path.parent.is_dir():
            raise MooseConfigError('Parent path to save config file does not exist.')

        with open(config_path, 'w', encoding='utf-8') as cf:
            config_strs = self.convert_path_to_str(self._config)
            json.dump(config_strs, cf, indent=4)


    def read_config(self, config_path: Path) -> Self:

        if not config_path.is_file():
            raise MooseConfigError(
                f'MOOSE config file does not exist at: {str(config_path)}.')

        with open(config_path, 'r', encoding='utf-8') as cf:
            config_strs = json.load(cf)
            config_paths = self.convert_str_to_path(config_strs)

        self._check_config_valid(config_paths)

        self._config = config_paths
        return self


class MooseConfigError(Exception):
    """MooseConfigError _summary_

    Args:
        Exception (_type_): _description_
    """