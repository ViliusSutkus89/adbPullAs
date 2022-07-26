# adbPullAs

[![test](https://github.com/ViliusSutkus89/adbPullAs/actions/workflows/test.yml/badge.svg)](https://github.com/ViliusSutkus89/adbPullAs/actions/workflows/test.yml)
[![adbPullAs on PyPI](https://badge.fury.io/py/adbPullAs.svg)](https://pypi.org/project/adbPullAs/)

adb pull wrapper to pull package private files from Android device.

WORKS ONLY ON DEBUG APPLICATIONS.

### Problem Scope

Developers and testers need to access data from `/data/data/com.viliussutkus89.adb.pull.as/cache`.

`adb pull /data/data/.../cache` is no go, because the directory is private.

`adb run-as com.viliussutkus89.adb.pull.as cp /data/data/com.viliussutkus89.adb.pull.as/cache /data/local/tmp` is no go, because `/data/local/tmp` may require storage permissions.

`adb su -c cp /data/data/.../cache /data/local/tmp` is no go, because it requires root.

### Solution

Recursive wrapper around adb.

Listing directories and reading files while using runtime permissions of specified application.

Piping contents into `/data/local/tmp` using normal adb user permissions and `adb pull`'ing into host computer.

### Install

adbPullAs is available on [PyPI](https://test.pypi.org/project/adbPullAs/)
```shell
python -m pip install adbPullAs
```

### Usage

adbPullAs is used as follows:
`adbPullAs PACKAGE_NAME ANDROID_SOURCE... COMPUTER_DESTINATION_DIR`.

`COMPUTER_DESTINATION_DIR` can be omitted to pull into current working directory,
	but only with a single supplied `ANDROID_SOURCE` (example 1).

Multiple `ANDROID_SOURCE`s require `COMPUTER_DESTINATION_DIR` to be supplied (example 2).

###### Example 1
```
adbPullAs com.viliussutkus89.application /data/data/com.viliussutkus89.application/databases/androidx.work.workdb
```
###### Example 2
```
adbPullAs com.viliussutkus89.application /data/data/com.viliussutkus89.application/cache /data/data/com.viliussutkus89.application/files ./pulled_from_device
```