import json
import unittest
import ddt as ddt
import requests


def get_app_url_list(filename):
    url_list = []
    with open(filename, 'r') as load_f:
        load_dict = json.load(load_f)
        for app_info in load_dict['apps']:
            if app_info.get("type") == "web_app":
                url_list.append(app_info.get("id"))
    return url_list


def check_for_redirects(url):
    try:
        url = url if url.startswith('http') else "http://%s" % url
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/129.0.0.0 Safari/537.36 '}
        r = requests.get(url, allow_redirects=False, timeout=300, headers=headers)
        if 300 <= r.status_code < 400:
            redirect_url = url if url.startswith('http') else url + r.headers['location']
            if url == redirect_url:
                return "[no redirect]"
            if redirect_url.startswith("http"):
                if redirect_url.split("://")[1].split("/")[0] != redirect_url.split("://")[1].split("/")[0]:
                    return "[domain has changed]"
        else:
            return '[no redirect]'
    except requests.exceptions.Timeout:
        return '[timeout]'
    except requests.exceptions.ConnectionError:
        return '[connection error]'


@ddt.ddt
class TestWebApp(unittest.TestCase):
    urls = get_app_url_list("./configs/apps/cros/apps_prod.json")

    @classmethod
    def setUpClass(cls):
        print("[INFO] start to check web app")

    @classmethod
    def tearDownClass(cls):
        print("[INFO] end to check web app")

    @ddt.data(*urls)
    def test_print(self, specific_url):
        check_result = check_for_redirects(specific_url)
        self.assertEqual(check_result, '[no redirect]', msg="the result of check %s is %s. " % (specific_url,
                                                                                                check_result))


if __name__ == "__main__":
    unittest.main()
