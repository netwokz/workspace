import os
import smtplib
import urllib3
import requests
import pandas as pd
from io import StringIO
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from requests_kerberos import HTTPKerberosAuth, OPTIONAL

# Function to send an email with the specified message


def send_email(message):
    recipients = [
        "pae2-cap-mgrs@amazon.com",
        "pae2-icqa@amazon.com",
        "pae2-afmleadership@amazon.com"
    ]
    sender = "pae2-data-analysts@amazon.com"
    msg = MIMEMultipart('mixed')
    msg['Subject'] = "PAE2 Offline Pods with Inventory"
    msg['To'] = ", ".join(recipients)
    email_content = message
    body = MIMEText(email_content, "plain")
    msg.attach(body)
    server = smtplib.SMTP("mail-relay.amazon.com")
    server.sendmail(sender, recipients, msg.as_string())
    server.quit()


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
req = requests.Session()
url = 'https://roboscout.amazon.com/view_plot_data/?sites=(PAE2)&instance_id=0&object_id=21303&BrowserTZ=America%2FLos_Angeles&app_name=RoboScout&mode=CSV'

try:
    resp = req.get(url, auth=HTTPKerberosAuth(
        mutual_authentication=OPTIONAL), verify=False, allow_redirects=True)
    if resp.status_code != 200:
        send_email("There are no offline pods")
        pass
    podDF = pd.read_csv(StringIO(resp.text), sep=',').drop(
        ['xValue', 'Index', 'Kiva_System_Key', 'Building', 'Pod_Recipe_Family'], axis=1)
    formathtml = """
    <html>
        <style>
            h1 {
                width: 1000px;
                text-align: center;
                font-weight: 900;
                
            }
            h2 {
                width: 600px;
                text-align: center;
                font-weight: bold;

            }      
            h3 {
                width: 500px;
                text-align: center;

            }
            table {
                border-collapse: collapse;
            }
            th{
                width: 250px;
                text-align: center;
                background-color:  #5D6D7E;
                color: #FDFEFE;
                border: 1px solid black;
            }
            table {
                width: 1000px;
            }
            td {
            width: 300px;
            text-align: center;
            color: black;
            background-color: #F8F9F9;
            border: 1px solid black;
            }
            </style>
        <head>
            <link rel="shortcut icon" href="/static/favicon.ico" type="image/x-icon">
            <link rel="icon" href="/static/favicon.ico" type="image/x-icon">
            <title>PAE2 Hourly Floor Status</title>
        </head>
    <body><center>"""

    prohtml = "</body></html>"

    podDF = podDF.to_html(index=False)

    html = formathtml + podDF + prohtml

    # Yeshtml += "<p>There are no more offline pods.</p>"

    #   recipients = [
    #   "pae2-cap-mgrs@amazon.com",
    #   "pae2-icqa@amazon.com",
    #    "pae2-afmleadership@amazon.com"
    #    ]

    recipients = ["gmikay@amazon.com"]  # test email
    sender = "pae2-data-analysts@amazon.com"
    msg = MIMEMultipart('mixed')
    msg['Subject'] = "PAE2 Offline Pods with Inventory"
    msg['To'] = ", ".join(recipients)
    HTMLBody = MIMEText(html, 'html')
    msg.attach(HTMLBody)
    server = smtplib.SMTP("mail-relay.amazon.com")
    server.sendmail(sender, recipients, msg.as_string())
    server.quit()
except Exception as e:
    resq = requests.Session()
    url = 'https://hooks.chime.aws/incomingwebhooks/d0677d82-acbf-4bdb-ae08-3965dc89333c?token=elVWeG5nWUh8MXxGRmtIeTNQbmkzOVZtckZpMXdBZV83SjBvV3NJMEdoOVJka0xwSlFfeUxB'
    text = 'Error in {f} | Code: {c} | {m}'.format(
        f=os.path.basename(__file__), c=type(e).__name__, m=str(e))
    PayLoad = '{"Content":"' + text + '"}'
    header = {"Content-Type": "application/json"}
    resq.post(url, data=PayLoad, headers=header)
