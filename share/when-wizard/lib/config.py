# file: share/when-wizard/lib/wizard_config.py
# -*- coding: utf-8 -*-
#
# Configuration for When Wizard application suite
# Copyright (c) 2015-2016 Francesco Garosi
# Released under the BSD License (see LICENSE file)


import os
import configparser


# Main configuration handler
class Config(object):
    _config_file = None
    _config_parser = None

    def __init__(self, config_file=USER_CONFIG_FILE):
        def bool_spec(v):
            if type(v) == str:
                v = v.lower()
                if v in ('true', 'yes', 'on', '1'):
                    return True
                elif v in ('false', 'no', 'off', '0'):
                    return False
                else:
                    return None
            else:
                return bool(v)
        self._config_file = config_file
        self._config_parser = configparser.ConfigParser()
        self._default()
        if os.path.exists(self._config_file):
            self.load()
        else:
            self.save()
        self._types = {
            'General': {
                'user email': str,
                'user name': str,
            },
        }

    def _default(self):
        self._config_parser.read_string("""
            [General]
            user email = true
            user name = false
            """)

    def get(self, section, entry, default=None):
        try:
            type_spec = self._types[section][entry]
            return type_spec(self._config_parser.get(section, entry))
        except (KeyError, configparser.Error):
            return None

    def set(self, section, entry, value):
        type_spec = self._types[section][entry]
        v = str(type_spec(value))
        if type_spec == bool:
            v = v.lower()
        self._config_parser.set(section, entry, v)

    def load(self):
        self._config_parser.read(self._config_file)

    def reset(self):
        self._default()
        self.save()

    def save(self):
        with open(self._config_file, mode='w') as f:
            self._config_parser.write(f)


# end.
