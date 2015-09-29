# coding: utf8

import configparser

CONFIG_FILE = 'wannago.conf'

class Config(object):
    def __init__(self, config_file=CONFIG_FILE):
        self.config_file = config_file
        self.cfg = configparser.ConfigParser()
        self.cfg.read(config_file)

    def writeConfig(self):
        with open(self.config_file, 'w') as file:
            self.cfg.write(file)

    def setConfig(self, section, name, value, overwrite=True):
        if not section in self.cfg:
            self.cfg[section] = {}
        if not name in self.cfg[section] or overwrite:
            self.cfg[section][name] = value
        return value

    def getConfig(self, section, name, defaultValue=None, writeIfMissing=False):
        if not section in self.cfg or not name in self.cfg[section]:
            if writeIfMissing and defaultValue is not None:
                self.setConfig(section, name, defaultValue)
            return defaultValue
        return self.cfg[section][name]
    def getSection(self, section, defaultValue={}):
        if not section in self.cfg:
            return defaultValue

        return self.cfg[section]

    def setToken(self, token):
        self.setConfig('Navitia', 'Token', token)

    def getToken(self):
        return self.getConfig('Navitia', 'Token')

    def setLocation(self, alias, location):
        return self.setConfig('Locations', alias, location)

    def getLocation(self, alias):
        return self.getConfig('Locations', alias)

defaultConfig = Config()
