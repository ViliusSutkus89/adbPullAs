# adbPullAs
adb pull wrapper to pull files from package private directories.

WORKS ONLY ON DEBUG APPLICATIONS.

### Problem Scope

Developers and testers need to access data from `/data/data/com.viliussutkus89.adb.pull.as/cache`.

`adb pull /data/data/.../cache` is no go, because the directory is private.

`adb run-as com.viliussutkus89.adb.pull.as cp /data/data/.../cache /data/local/tmp` is no go, because that requires storage permissions.

`adb su -c cp /data/data/.../cache /data/local/tmp` is no go, because that requires root.

### Solution

Recursive wrapper around `adb` to list directories, `cat-pipe` file contents into `/data/local/tmp` and `adb pull` to host computer.
