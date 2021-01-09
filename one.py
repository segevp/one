from requests import get, post
from json.decoder import JSONDecodeError
from json import load, dump

ONE_API = "https://one.prat.idf.il/api"
ONE_USER = ONE_API + "/account/getUser"
ONE_REPORTED_DATA = ONE_API + "/Attendance/GetReportedData"
ONE_ATTEND = ONE_API + '/Attendance/InsertPersonalReport'
ONE_STATUSES = ONE_API + '/Attendance/GetAllFilterStatuses'

RELEVANT_COOKIES = [
    "AppCookie",
    "visid_incap_2025883",
    "incap_ses_253_2025883",
    "nlbi_2025883",
    "BIGipServerMFT-One-Frontends"
]
SAVE_COOKIES = [
    "AppCookie",
    "visid_incap_2025883"
]

HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/86.0.4240.183 Safari/537.36'
}


class Utils:
    @staticmethod
    def filter_dict(d, keys):
        return {key: val for key, val in d.items() if key in keys}


class Soldier:
    def __init__(self, path):
        self.path = path
        self.headers = HEADERS
        self.cookies = self._load_cookies()

        self.authenticated = self._authenticate()

    def _load_cookies(self):
        with open(self.path, 'rb') as f:
            cookies = load(f)
        if "AppCookie" not in cookies:
            raise KeyError("Needed cookie not found")
        return cookies if "AppCookie" in cookies else None

    def _save_cookies(self):
        cookies_to_save = Utils.filter_dict(self.cookies, SAVE_COOKIES)
        with open(self.path, 'w') as f:
            dump(cookies_to_save, f, indent=4)

    def _update_cookies(self, new):
        to_save = Utils.filter_dict(self.cookies, SAVE_COOKIES) != self.cookies
        relevant_cookies = Utils.filter_dict(new, RELEVANT_COOKIES)
        self.cookies.update(relevant_cookies)
        if to_save:
            self._save_cookies()

    def _request(self, url, data=None):
        request = get
        request_params = {
            'headers': self.headers,
            'cookies': self.cookies,
            'url': url
        }
        if data:
            request_params['data'] = data
            request = post
        response = request(**request_params)
        return response

    def _authenticate(self):
        response = self._request(ONE_USER)
        try:
            response.json()
        except JSONDecodeError:
            return False
        self._update_cookies(response.cookies)
        return True

    def attend(self, main_code: str, secondary_code: str):
        attendance_form = {
            'MainCode': main_code,
            'SecondaryCode': secondary_code
        }
        self._request(ONE_ATTEND, attendance_form)

    @property
    def reported_data(self):
        return self._request(ONE_REPORTED_DATA).json()

    @property
    def _possible_statuses(self):
        return self._request(ONE_STATUSES).json()


if __name__ == '__main__':
    soldier = Soldier('config.json')
    soldier.attend('01', '01')
