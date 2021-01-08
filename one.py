from requests import get, post
from json.decoder import JSONDecodeError
from json import load, dump
from pprint import pprint

ONE_API = "https://one.prat.idf.il/api"
ONE_USER = ONE_API + "/account/getUser"
ONE_REPORTED_DATA = ONE_API + "/Attendance/GetReportedData"
ONE_MEMBER_HISTORY = ONE_API + "/Attendance/memberHistory"
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


def load_cookies(path):
    cookies = {}
    with open(path, 'rb') as f:
        try:
            cookies = load(f)
        except JSONDecodeError:
            pass
    return cookies if "AppCookie" in cookies else None


def authenticate(cookies, headers):
    user_response = get(ONE_USER, cookies=cookies, headers=headers)
    try:
        return user_response
    except JSONDecodeError:
        pass


def update_cookies(old, new):
    relevant_cookies = {key: val for key, val in new.items() if key in RELEVANT_COOKIES}
    old.update(relevant_cookies)


def save_cookies(path, cookies):
    cookies_to_save = {key: val for key, val in cookies.items() if key in SAVE_COOKIES}
    with open(path, 'w') as f:
        dump(cookies_to_save, f, indent=4)


def attend(cookies, headers, main_code: str, secondary_code: str):
    attendance_form = {
        'MainCode': main_code,
        'SecondaryCode': secondary_code
    }
    post(ONE_ATTEND, attendance_form, cookies=cookies, headers=headers)


def reported_data(cookies, headers):
    return get(ONE_REPORTED_DATA, cookies=cookies, headers=headers).json()


def run(path, headers, main_code, secondary_code):
    one_cookies = load_cookies(path)
    user = authenticate(one_cookies, headers)
    if not user:
        print("--> ERROR: Authentication Failure.")
        exit()
    update_cookies(one_cookies, user.cookies)
    save_cookies(path, one_cookies)
    attend(one_cookies, headers, main_code, secondary_code)
    pprint(reported_data(one_cookies, headers))


if __name__ == '__main__':
    run('config.json', HEADERS, '01', '01')
