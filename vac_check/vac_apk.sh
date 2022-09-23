#!/bin/sh 

# env prepare

apks_folder="/home/android-apks"
screencap_folder="/home/screencap"
apktool_folder="/usr/local/apktool"
no_activity_file="/home/not_found_activity.txt"
install_failed_apks="/home/install_failed_apks.txt"
error_log="/home/error.log"
info_log="/home/info.log"

echo "[INFO] start to prepare env of apktools."

if [ -d "$apktool_folder" ];then
  echo "[INFO] apktools already exists."
else
  echo "[INFO] start to download files for apktools."
  mkdir /usr/local/apktool
  cd /usr/local/apktool
  wget https://raw.githubusercontent.com/iBotPeaches/Apktool/master/scripts/linux/apktool
  wget http://connortumbleson.com/apktool/apktool_2.2.2.jar
  wget https://connortumbleson.com/apktool/aapts/linux/aapt
  mv apktool_2.2.2.jar apktool.jar
  chmod +x apktool apktool.jar aapt
fi

mount -o remount rw /

rm -rf $no_activity_file $install_failed_apks $error_log $info_log $screencap_folder
touch $no_activity_file $install_failed_apks $error_log $info_log
mkdir $screencap_folder


# install -> start -> screencap -> stop -> uninstall

if [ -d "$apks_folder" ];then
  echo "[INFO] apks folder exists, then check."

  for name in ${apks_folder}/*
  do
    apk_name="$name" 
    cd /
    package_info=$(./usr/local/apktool/aapt dump badging $apk_name | grep "package: name=")
    pkg_name=$(echo $package_info | awk -F ''\''' '{print $2}')

    activity_info=$(./usr/local/apktool/aapt dump badging $apk_name | grep "launchable-activity")
    activity_name=$(echo $activity_info | awk -F ''\''' '{print $2}')

    if [ -z "$activity_name" ];then
        echo $apk_name >> $no_activity_file
    else
        echo $pkg_name
        echo $activity_name

        install_state_1=1
        install_state_2=1

        adb install "$apk_name"

        install_state_1=$?
        if [ ${install_state_1} -eq 1 ]; then
           echo "[ERROR] failed to install $apk_name, retrying..." >> $error_log
           adb install "$apk_name"

           install_state_2=$?
           if [ ${install_state_2} -eq 1 ]; then
              echo "[ERROR] retry to install $apk_name, then failed." >> $error_log
              echo $apk_name >> $install_failed_apks
           fi
        fi

        start_state_1=1
        start_state_2=1
        if [ ${install_state_1} -eq 0 -o ${install_state_2} -eq 0 ]; then
           adb shell am start "$pkg_name/$activity_name"

           start_state_1=$?
           if [ ${install_state_1} -eq 1 ]; then
              echo "[ERROR] failed to start service for $apk_name, retrying..." >> $error_log
              adb shell am start "$pkg_name/$activity_name"
              start_state_2=$?
              if [ ${start_state_2} -eq 1 ]; then
                 echo "[ERROR] retry to start service for $apk_name, then failed." >> $error_log
              fi
           fi

        fi

        if [ ${start_state_1} -eq 0 -o ${start_state_2} -eq 0 ]; then
          package_name=$(echo $apk_name | awk -F ''/'' '{print $4}')
          echo $package_name

          #adb shell screencap -p /sdcard/"$package_name"".png"
          #adb pull /sdcard/"$package_name"".png" $screencap_folder
          sleep 20
          screenshot --external "$screencap_folder""/""$package_name"".png"

          sleep 3
          adb shell am force-stop $pkg_name
        fi

        if [ ${install_state_1} -eq 0 -o ${install_state_2} -eq 0 ]; then
          adb uninstall $pkg_name
        fi
    fi
  done

else
  echo "[ERROR] failed to check apks, apk files not exist."
  exit 1
fi
