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


class Versioner:
    def __init__(self):
        abs_dir_name = os.path.abspath(os.path.dirname(__file__))
        self.__version_files = [os.path.abspath(os.path.join(abs_dir_name, f)) for f in ('../pyproject.toml', '../src/adbPullAs/__init__.py')]
        self.__version_str = self.__get_version()
        if not self.__version_str:
            raise RuntimeError("Unable to find version string.")
        self.__version = list(map(int, self.__version_str.split('.')))

    def __get_version(self):
        for f in self.__version_files:
            with open(f, 'r') as fp:
                for line in fp:
                    if line.startswith('version = '):
                        delimiter = '"' if '"' in line else "'"
                        return line.split(delimiter)[1]
        return False

    def get_version_str(self):
        return self.__version_str

    def __save_version_file(self, file):
        with open(file, 'r+') as fh:
            position = 0
            for line in fh:
                if line.startswith('version = '):
                    fh.seek(position)
                    fh.write(f"version = '{self.__version_str}' #")
                    return True
                position += len(line)

    def __save_version(self):
        updated_list = []
        for file in self.__version_files:
            if self.__save_version_file(file):
                updated_list.append(file)
        return updated_list

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
