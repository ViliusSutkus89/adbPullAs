# adbPullAs
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
