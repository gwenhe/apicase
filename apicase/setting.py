import os
import yaml
from typing import Any, Dict
from pydantic import Extra, BaseSettings as Base


class BaseSettingSchema(Base):
    _yaml_path: str

    @classmethod
    def yaml_config_settings_source(cls, setting: Base) -> Dict[str, Any]:
        """
        A simple settings source that loads variables from a JSON file
        at the project's root.
        """
        encoding = setting.__config__.env_file_encoding
        with open(cls._yaml_path, encoding=encoding) as f:
            return yaml.load(f, Loader=yaml.FullLoader)

    class Config:
        env_file_encoding = 'utf-8'
        extra: Extra = Extra.allow

        @classmethod
        def customise_sources(
                cls,
                init_settings,
                env_settings,
                file_secret_settings,
        ):
            """
            None
            :param init_settings:
            :param env_settings:
            :param file_secret_settings:
            :return:
            """
            return (
                init_settings,
                BaseSettingSchema.yaml_config_settings_source,
                env_settings,
                file_secret_settings,
            )


class Settings(object):
    """
    :param
    """

    def __init__(self, env: str, env_suffix: str, env_path: str, setting_class):
        BaseSettingSchema._yaml_path = os.path.join(env_path, env + env_suffix)
        self.setting_class = setting_class

    def get_setting(self):
        """

        :return:
        """
        return self.setting_class()



