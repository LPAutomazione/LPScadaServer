import json
import os
import platform

from PySide2.QtCore import QObject

DEFAULT_SETTINGS = {
    "DEBUG": True,
    "timer_granularity": 100
}


class _SettingsSingleton(QObject):
    instance = None

    def __init__(self, parent=None):
        super(_SettingsSingleton, self).__init__(parent=parent)
        self._settingsFilePath = os.path.join(os.getcwd(), "data", "settings.json")
        self._dict = {}

        # If the settings file doesn't exits, create it
        if not os.path.exists(self._settingsFilePath):
            with open(self._settingsFilePath, 'w') as outfile:
                json.dump(self._dict, outfile, indent=4)
        else:
            with open(self._settingsFilePath) as json_file:
                self._dict = json.load(json_file)

    def _write(self):
        with open(self._settingsFilePath, 'w') as outfile:
            json.dump(self._dict, outfile, indent=4)
            if platform.system() != "Windows":
                os.sync()   # enforce writing on disk, if necessary

    def _read(self, key):
        if key not in self._dict:
            self._dict[key] = DEFAULT_SETTINGS[key]
            self._write()
        return self._dict[key]

    def get(self, propName: str):
        return self._read(propName)

    def set(self, propName: str, value):
        if propName not in self._dict.keys() or self._dict[propName] != value:
            self._dict[propName] = value
            self._write()


def settings():
    if _SettingsSingleton.instance is None:
        _SettingsSingleton.instance = _SettingsSingleton()
    return _SettingsSingleton.instance

