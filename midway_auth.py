import http
import requests
import urllib.parse
import logging
import os
import getpass

MIDWAY_ENDPOINT = 'https://midway-auth.amazon.com'
USERNAME = getpass.getuser()
PASSWORD = ''  # TBD
COOKIE_FILE = os.path.expanduser("~") + '\\.midway\\cookie'

logger = logging.getLogger()

print(COOKIE_FILE)


def resp_info(response):
    return '{}:{}:{}:{}'.format(
        response.headers.get('x-host'),
        response.headers.get('x-request-id'),
        response.status_code,
        response.text)


# Will store cookies in the same format as mwinit
cookie_jar = http.cookiejar.MozillaCookieJar(COOKIE_FILE)
session = requests.Session()
session.cookies = cookie_jar
# Get CSRF token
session_status_url = urllib.parse.urljoin(
    MIDWAY_ENDPOINT, '/api/session-status')
response = session.get(session_status_url)
if not response.ok:
    logger.error('Error while getting  session status: %s',
                 resp_info(response))
json_response = response.json()
csrf_param = json_response['csrf_param']
csrf_token = json_response['csrf_token']
# Login
login_url = urllib.parse.urljoin(MIDWAY_ENDPOINT, '/api/login')
login_data = {
    'format': 'json',
    'user_name': USERNAME,
    'password': PASSWORD,
    csrf_param: csrf_token,
}
logger.info('Testing with user %s', USERNAME)
# You need to send CSRF token and session cookie you received from previous step
response = session.post(login_url, data=login_data)
if not response.ok:
    logger.error('Login failed: %s', resp_info(response))
# Write the cookies to the file
cookie_jar.save()
# If Sentry is used behind the service, you need to opt-in to Sentry to Midway flow,
# This will add a cookie that will begin redirecting your subsequent authentication requests from Sentry to Midway.
# https://w.amazon.com/index.php/Sentry/Regionalized%20Identity/Sentry%20To%20Midway
response = session.post('https://sentry.amazon.com/sentry-braveheart?value=1')
if not response.ok:
    logger.error('Sentry authentication redirect failed: %s',
                 resp_info(response))
