#!/bin/sh
set -eu

applicationId=com.viliussutkus89.adb.pull.as

adb shell am start -W $applicationId/$applicationId.MainActivity
echo

echo "Pulling a single file into current directory"
./src/adbPullAs/__init__.py $applicationId /data/data/$applicationId/cache/test/activityScreenshot.png
rm activityScreenshot.png
echo

echo "Pulling a single file into specified directory"
mkdir test_tmp
./src/adbPullAs/__init__.py $applicationId /data/data/$applicationId/cache/test/activityScreenshot.png test_tmp
rm test_tmp/activityScreenshot.png
rmdir test_tmp
echo

echo "Pulling directory into current directory"
./src/adbPullAs/__init__.py $applicationId /data/data/$applicationId/cache/test
rm test/activityScreenshot.png
rm test/subDirectory/file1.txt
rm test/subDirectory/file2.txt
rmdir test/subDirectory
rmdir test
echo

echo "Pulling directory into specified directory"
mkdir test_tmp
./src/adbPullAs/__init__.py $applicationId /data/data/$applicationId/cache/test test_tmp
rm test_tmp/test/activityScreenshot.png
rm test_tmp/test/subDirectory/file1.txt
rm test_tmp/test/subDirectory/file2.txt
rmdir test_tmp/test/subDirectory
rmdir test_tmp/test
rmdir test_tmp
echo

echo "Asking for the same file twice"
mkdir test_tmp
./src/adbPullAs/__init__.py $applicationId /data/data/$applicationId/cache/test/activityScreenshot.png /data/data/$applicationId/cache/test/activityScreenshot.png test_tmp
rm test_tmp/activityScreenshot.png
rmdir test_tmp
echo
