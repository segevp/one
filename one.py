from requests import get
from json.decoder import JSONDecodeError
from json import load

# One Relevant URLs
ONE_URL = "https://one.prat.idf.il"
ONE_USER = ONE_URL + "/api/account/getUser"
ONE_REPORTED_DATA = ONE_URL + "/api/Attendance/GetReportedData"
ONE_MEMBER_HISTORY = ONE_URL + "/api/Attendance/memberHistory"

# Cookies and Headers
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/86.0.4240.183 Safari/537.36'
}
with open('config.json', 'rb') as f:
    COOKIES = load(f)

# BODY
# Test Authentication
user_response = get(ONE_USER, cookies=COOKIES, headers=HEADERS)
try:
    connection_check = user_response.json()
except JSONDecodeError:
    print("--> ERROR: Authentication Failure!")
    exit()

# Update cookies
COOKIES.update(user_response.cookies)
