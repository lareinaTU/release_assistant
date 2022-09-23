import json
import requests


def check_for_redirects(url):
    try:
        r = requests.get(url, allow_redirects=False, timeout=8)
        if 300 <= r.status_code < 400:
            redirect_url = url if url.startswith('http') else url + r.headers['location']
            return redirect_url
        else:
            return '[no redirect]'
    except requests.exceptions.Timeout:
        return '[timeout]'
    except requests.exceptions.ConnectionError:
        return '[connection error]'


def check_domains(urls):
    for url in urls:
        url_to_check = url if url.startswith('http') else "http://%s" % url
        redirect_result = check_for_redirects(url_to_check)
        if redirect_result in ["[timeout]", "[connection error]"]:
            print("%s => %s" % (url_to_check, redirect_result))
        elif redirect_result.startswith("http"):
            if redirect_result.split("://")[1].split("/")[0] != url_to_check.split("://")[1].split("/")[0]:
                print("[domain has changed:]", "%s => %s" % (url_to_check, redirect_result))
    print("[INFO]end to check web apps")


def get_app_url_list(filename):
    url_list = []
    with open(filename, 'r') as load_f:
        load_dict = json.load(load_f)
        for app_info in load_dict:
            if app_info.get("type") == "web_app":
                url_list.append(app_info.get("id"))
    return url_list


urls = get_app_url_list("./configs/apps/cros/test.json")
check_domains(urls)
