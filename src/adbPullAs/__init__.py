#!/usr/bin/env python3
# Copyright (C) 2022
# ViliusSutkus89.com
# https://github.com/ViliusSutkus89/adbPullAs
#
# adbPullAs - adb pull wrapper to pull package private files from Android device
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

import getopt
import os
import pathlib
import subprocess
import sys
from pathlib import PurePosixPath


class FsTest:
    def __init__(self, package_name=None):
        self.__package_name = package_name

    def __implementation(self, test, path):
        args = ('adb', 'shell')
        if self.__package_name:
            args += ('run-as', self.__package_name)

        # sh -c || echo NOT needed because
        # old Androids exit "adb shell false" with exit code 0... workaround this
        args += ('sh', '-c', f'"{test} {path}" || echo NOT')

        return not subprocess.run(args, capture_output=True, text=True).stdout

    def exists(self, path):
        return self.__implementation('test -e', path)

    def is_directory(self, path):
        return self.__implementation('test -d', path)

    def is_file(self, path):
        return self.__implementation('test -f', path)


class TmpDir:
    @staticmethod
    def mkdir_unique(location, name_prefix):
        i = 0
        directory = location / name_prefix
        while len(subprocess.run(('adb', 'shell', 'mkdir', directory), capture_output=True).stdout):
            directory = location / f'{name_prefix}-{i}'
            i += 1
        return directory

    def __init__(self):
        self.dir = self.mkdir_unique(PurePosixPath('/data/local/tmp'), 'adbPullAs')

    def __del__(self):
        if self.dir:
            subprocess.run(('adb', 'shell', 'rm', '-r', self.dir))


class AdbPullAs:
    def __init__(self, package_name):
        self.__package_fs_test = FsTest(package_name)
        self.__regular_fs_test = FsTest()
        self.__run_as_package_args = ('adb', 'shell', 'run-as', package_name)

    def __cache_target(self, remote, cached_remote):
        ret_val = True
        if self.__package_fs_test.is_file(remote):
            subprocess.run(self.__run_as_package_args + ('cat', remote, '>', cached_remote), shell=False)
        elif self.__package_fs_test.is_directory(remote):
            if not self.__regular_fs_test.is_directory(cached_remote):
                subprocess.run(('adb', 'shell', 'mkdir', cached_remote))
            ls_proc = subprocess.run(self.__run_as_package_args + ('ls', f'{remote}/'), capture_output=True, text=True)
            for dir_entry in ls_proc.stdout.splitlines():
                ret_val &= self.__cache_target(
                    remote / dir_entry,
                    cached_remote / dir_entry
                )
        else:
            print('Unknown entity type', remote)
            ret_val = False
        return ret_val

    def pull(self, remotes, local_destination) -> bool:
        ret_val = True
        pull_args = ('adb', 'pull')

        tmp_dir = TmpDir()
        for remote in remotes:
            remote = PurePosixPath(remote)
            cached_remote = TmpDir.mkdir_unique(tmp_dir.dir, 'pull') / remote.name
            pull_args += (cached_remote, )
            ret_val &= self.__cache_target(remote, cached_remote)

        if local_destination:
            pull_args += (local_destination, )

        ret_val &= subprocess.run(pull_args).returncode == 0

        return ret_val


def main():
    args = []
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hv', ['help', 'version'])
        for o, a in opts:
            if o in ('-h', '--help'):
                print_usage()
                exit(os.EX_OK)
            elif o in ('-v', '--version'):
                print_version()
                exit(os.EX_OK)
    except getopt.GetoptError as err:
        print(err, "\n", file=sys.stderr)
        print_usage(sys.stderr)
        exit(os.EX_USAGE)

    package_name = None
    try:
        package_name = args.pop(0)
    except IndexError:
        print_usage(sys.stderr)
        exit(os.EX_USAGE)

    local = args.pop() if len(args) > 1 else None
    remotes = args
    if local:
        if not os.path.exists(local):
            print(local, '- COMPUTER_DESTINATION_DIR does not exist!', file=sys.stderr)
            exit(os.EX_NOINPUT)

        if not os.path.isdir(local):
            print(local, '- COMPUTER_DESTINATION_DIR is not a directory!', file=sys.stderr)
            exit(os.EX_NOINPUT)

    pull_status = AdbPullAs(package_name).pull(remotes, local)
    exit(os.EX_OK if pull_status else os.EX_IOERR)


def print_usage(output_to=sys.stdout):
    app = os.path.basename(sys.argv[0])
    print(app, 'usage:', file=output_to)
    print(app, 'PACKAGE_NAME ANDROID_SOURCE... COMPUTER_DESTINATION_DIR\n', file=output_to)
    print('COMPUTER_DESTINATION_DIR can be omitted to pull into current working directory,', file=output_to)
    print('\tbut only with a single supplied ANDROID_SOURCE (first example).', file=output_to)
    print('Multiple ANDROID_SOURCEs require COMPUTER_DESTINATION_DIR to be supplied.\n', file=output_to)
    print('Examples:', file=output_to)
    pn = 'com.viliussutkus89.application'
    print(app, pn, f'/data/data/{pn}/databases/androidx.work.workdb', file=output_to)
    print(app, pn, f'/data/data/{pn}/cache', f'/data/data/{pn}/files',
          './pulled_from_device', file=output_to)


def print_version():
    here = pathlib.Path(__file__).parent.resolve()
    version = (here / 'VERSION').read_text(encoding='utf-8')

    print(os.path.basename(sys.argv[0]), '-', 'adb pull wrapper to pull package private files from Android device')
    print('version:', version)
    print()
    print('THIS WORKS ONLY ON DEBUG APPLICATIONS')
    print()
    print('Copyright (C) 2022')
    print('ViliusSutkus89.com')
    print('https://github.com/ViliusSutkus89/adbPullAs')
    print()
    print('adbPullAs is free software: you can redistribute it and/or modify')
    print('it under the terms of the GNU General Public License version 3,')
    print('as published by the Free Software Foundation.')
    print()
    print('This program is distributed in the hope that it will be useful,')
    print('but WITHOUT ANY WARRANTY; without even the implied warranty of')
    print('MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the')
    print('GNU General Public License for more details.')
    print()
    print('You should have received a copy of the GNU General Public License')
    print('along with this program.  If not, see <https://www.gnu.org/licenses/>.')


if __name__ == '__main__':
    main()
