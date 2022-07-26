# Copyright (C) 2022
# ViliusSutkus89.com
# https://github.com/ViliusSutkus89/adbPullAs
#
# adbPullAs is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3,
# as published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import os.path
import pathlib


class Versioner:
    def __init__(self):
        here = pathlib.Path(__file__).parent.resolve()
        self.version_file = os.path.abspath(here.parent / 'src' / 'adbPullAs' / 'VERSION')
        with open(self.version_file, 'r') as f:
            self.__version_str = f.read().strip()
        self.__version = list(map(int, self.__version_str.split('.')))

    def get_version(self):
        return self.__version

    def get_version_str(self):
        return self.__version_str

    def __save_version(self):
        with open(self.version_file, 'w') as f:
            f.write(self.__version_str)

    def increment_major(self):
        self.__version[0] += 1
        self.__version[1] = 0
        self.__version[2] = 0
        self.__version_str = '.'.join(str(x) for x in self.__version)
        return self.__save_version()

    def increment_minor(self):
        self.__version[1] += 1
        self.__version[2] = 0
        self.__version_str = '.'.join(str(x) for x in self.__version)
        return self.__save_version()

    def increment_patch(self):
        self.__version[2] += 1
        self.__version_str = '.'.join(str(x) for x in self.__version)
        return self.__save_version()
