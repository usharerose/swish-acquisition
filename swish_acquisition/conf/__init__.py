"""
Settings and configuration for Swish, referred to Django
Read values defined in settings module from
- environment variables
- module itself
"""
from functools import wraps
import importlib
import json
from json import JSONDecodeError
import logging
import os
import re
import traceback
from typing import Any, Callable, Union


logger = logging.getLogger(__name__)


ENVIRONMENT_VARIABLE = 'SWISH_SETTINGS_MODULE'
DEFAULT_SETTINGS_MODULE = 'swish_acquisition.settings'
SETTING_KEY_MAX_LENGTH = 100
SETTING_KEY_MATCH = re.compile(r'^[a-zA-Z0-9_-]+$').match


class Settings:

    def _setup(self):
        self.__dict__.clear()
        settings_module = os.environ.get(ENVIRONMENT_VARIABLE, DEFAULT_SETTINGS_MODULE)
        self.SETTINGS_MODULE = settings_module
        mod = importlib.import_module(settings_module)
        for setting_key in dir(mod):
            # Setting names must be all uppercase
            if not setting_key.isupper():
                continue

            local_value = getattr(mod, setting_key)
            env_value = self._get_value_from_env(setting_key, local_value)
            setting_value = local_value if env_value is None else env_value
            setattr(self, setting_key, setting_value)

    def _get_value_from_env(self, key: str, value: Any) -> Any:
        self._validate_setting_key(key)

        if isinstance(value, dict):
            return self._get_dict_setting_value(key, value)
        elif isinstance(value, list):
            return self._get_list_setting_value(key, value)
        return self._get_common_setting_value(key, value)

    @staticmethod
    def _validate_setting_key(key: str) -> bool:
        """
        1. validate the length of setting key
        2. validate the characters of setting key, only support
            * alphabet (lowercase and uppercase)
            * underline
            * hyphenation
        """
        if len(key) > SETTING_KEY_MAX_LENGTH:
            raise ValueError(
                f'The length of environment key [{key[:SETTING_KEY_MAX_LENGTH]} ...] '
                f'should be less than {SETTING_KEY_MAX_LENGTH}')

        if not SETTING_KEY_MATCH(key):
            raise ValueError(
                f'Environment key [{key}] contains illegal characters')

        return True

    def _get_dict_setting_value(self, parent_setting_key: str, dict_value: Any):
        if not isinstance(dict_value, dict):
            return {}

        for child_setting_key, child_setting_value in dict_value.items():
            full_setting_key = f'{parent_setting_key}_{child_setting_key}'
            dict_value[child_setting_key] = self._get_value_from_env(full_setting_key, child_setting_value)

        return dict_value

    @staticmethod
    def _get_list_setting_value(setting_key: str, list_value: list) -> list:
        env_value = os.environ.get(setting_key.upper(), None)
        if env_value is None:
            return list_value

        try:
            deserialized_value = json.loads(env_value)
            if not isinstance(deserialized_value, list):
                raise JSONDecodeError(msg='Expecting JSON array',
                                      doc=env_value, pos=1)
        except JSONDecodeError:
            raise ValueError(
                f'Value of environment variable [{setting_key.upper()}] is not an illegal JSON array')

        return deserialized_value

    @staticmethod
    def _get_common_setting_value(setting_key: str, value: Any) -> Any:
        env_value = os.environ.get(setting_key.upper(), None)
        if env_value is None:
            return value

        if isinstance(value, (bool, int, float)):
            return _convert_to_target_dtype(env_value, value)

        return env_value

    def __getattr__(self, name):
        if name not in self.__dict__:
            self._setup()

        if name not in self.__dict__:
            # avoid infinite recursion
            # https://docs.python.org/3/reference/datamodel.html#object.__getattribute__
            return object.__getattribute__(self, name)

        return getattr(self, name)

    def __repr__(self):
        return f'<{self.__class__.__name__} "{self.SETTINGS_MODULE}">'


def _convert_to_target_dtype(source_value: str, target_value: Any) -> Union[bool, int, float, str]:
    """
    convert the data type of source_value to target_value's
    """
    if isinstance(target_value, bool):
        return _string_to_boolean(source_value)  # type: ignore
    if isinstance(target_value, int):
        return _string_to_int(source_value)  # type: ignore
    if isinstance(target_value, float):
        return _string_to_float(source_value)  # type: ignore
    return source_value


def dtype_convert_wrapper(func: Callable) -> Callable:

    @wraps(func)
    def _wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception:  # NOQA
            logger.exception(f'Exception occurred when convert data type:\n{traceback.format_exc()}')
            raise

    return _wrapper


@dtype_convert_wrapper
def _string_to_boolean(value: str) -> bool:
    value = value.strip().lower()
    if value == 'true':
        return True
    elif value == 'false':
        return False
    raise ValueError(f'Invalid input [{value}] converted to boolean')


@dtype_convert_wrapper
def _string_to_int(value: str) -> int:
    return int(value)


@dtype_convert_wrapper
def _string_to_float(value: str) -> float:
    return float(value)


settings = Settings()
