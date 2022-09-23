import json
import os

json_data = json.load(open('/home/apk_config.json', 'r', encoding="utf-8"))
for dict_item in json_data:
    print(dict_item.get('type'))
    if dict_item.get('type') == "android_app":
        if dict_item.get('url'):
            download_apk_cmd = 'wget -P /home/android_apks %s' % (dict_item.get("url"))
            textlist = os.popen(download_apk_cmd).readlines()
            for line in textlist:
                print(line)

