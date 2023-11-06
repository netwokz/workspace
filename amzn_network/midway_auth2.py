import pytest
import requests
from requests_sigv4 import Sigv4Request

# This is a minimal example of what is needed to use Sigv4 Automation Access to Midway (SAAM),
# to allow canaries and/or integration tests to access a Midway protected resources through AEA

# It is NOT an example of best practices!

# See https://w.amazon.com/bin/view/NextGenMidway/UserGuide/SAAM/ for more information


def test_saaam_auth():
    # EXPORT AWS creds from isengard for local testing
    # Otherwise this will use the AWS creds from the environment it is run in
    # Those creds must be given "Allow" permission for action "midway-auth:GET", and resources "arn:<partition>:midway-auth:<region>:*:/api/sigv4/login"
    # Those creds must also be allowlisted in Midway for SAAM access
    sigv4_requestor = Sigv4Request(
        region='us-west-2',
        service='midway-auth'
    )

    # Login to to MidwayAuth - using the appropriate Sigv4 endpoint
    # SAAM session cookies are valid for 6 hours and should be re-used throughout that time
    # or the user could become throttled by Midway
    print("Requesting Midway session")
    resp = sigv4_requestor.get(
        'https://{}/api/sigv4/login'.format(
            'midway-auth-sigv4.us-west-2.amazonaws.com'),
        verify=False,
    )
    js = resp.json()
    session_data = js['session']
    print("Retrieved Midway session")

    # Store the MidwayAuth session as a cookie named "session" on the normal MidwayAuth domain
    s = requests.session()
    s.cookies.set("session", session_data, domain="midway-auth.amazon.com")
    print("Set session cookie")

    # Now we can visit the website just a like a normal user
    # When redirected to Midway, our session cookie will grant us access to an ID token for the target site
    print("Requesting webpage")
    resp = s.get("https://sigv-47-beta.corp.amazon.com")
    print("Got webpage")
    print(resp.history)
    for r in resp.history:
        print(r.headers)
    webpage = resp.text

    # Perform any tests on the target site that we would like
    # In this case, just checking that we successfully authenticated to the desired site
    page_validation_string = 'SigV-47'
    # Our tests run in account "203519064051"
    # Our tests run under the Role named "SAAMPoCBabylonCanaryTests-GizaHydraSecurityTestInv-1TRFWFY1ML8GV"
    # MidwayAuth will issue a username of the form svc-mw-<AccountID>-<Role/User Name>
    user_validation_string = 'svc-mw-203519064051-SAAMPoCBabylonCanaryTests-GizaHydraSecurityTestInv-1TRFWFY1ML8GV'
    assert page_validation_string in webpage
    assert user_validation_string in webpage


test_saaam_auth()
