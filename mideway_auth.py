# Assuming that AmazonRequest is stored in a file called amazon_utils in the same folder as the current file.
from amazon_utils import AmazonRequest

am_req = AmazonRequest()

# If the site needs midway authentication (with custom flags for mwinit):
am_req.set_mw_cookie(flags=["-o"])

# If the website needs to be authenticated to FC Web Menu:
am_req.authenticate_web_menu(fc='GYR1')

response = am_req.send_req(url='https://w.amazon.com')
print(response.status_code)