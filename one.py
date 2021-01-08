from requests import get, post
from json.decoder import JSONDecodeError
from json import load, dump
from pprint import pprint

ONE_API = "https://one.prat.idf.il/api"
ONE_USER = ONE_API + "/account/getUser"
ONE_REPORTED_DATA = ONE_API + "/Attendance/GetReportedData"
ONE_ATTEND = ONE_API + '/Attendance/InsertPersonalReport'

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


class Soldier:
    def __init__(self, path):
        self.headers = HEADERS
        self.path = path

        self.cookies = self.load_cookies()
        self.authenticated = self.authenticate()

    def load_cookies(self):
        with open(self.path, 'rb') as f:
            cookies = load(f)
        if "AppCookie" not in cookies:
            raise KeyError("Needed cookie not found")
        return cookies if "AppCookie" in cookies else None

    def _save_cookies(self):
        cookies_to_save = {key: val for key, val in self.cookies.items() if key in SAVE_COOKIES}
        with open(self.path, 'w') as f:
            dump(cookies_to_save, f, indent=4)

    def _update_cookies(self, new):
        to_save = len({key: val for key, val in self.cookies.items() if key in SAVE_COOKIES}) != self.cookies
        relevant_cookies = {key: val for key, val in new.items() if key in RELEVANT_COOKIES}
        self.cookies.update(relevant_cookies)
        if to_save:
            self._save_cookies()

    def authenticate(self):
        try:
            response = get(ONE_USER, cookies=self.cookies, headers=self.headers)
            self._update_cookies(response.cookies)
            return True
        except JSONDecodeError:
            return False

    def attend(self, main_code: str, secondary_code: str):
        attendance_form = {
            'MainCode': main_code,
            'SecondaryCode': secondary_code
        }
        post(ONE_ATTEND, attendance_form, cookies=self.cookies, headers=self.headers)

    @property
    def reported_data(self):
        return get(ONE_REPORTED_DATA, cookies=self.cookies, headers=self.headers).json()


if __name__ == '__main__':
    soldier = Soldier('config.json')
    soldier.attend('01', '01')
