import os

from slack_html_parser import SlackHTMLParser
from slack_webhook_msg import SlackWebhookBot

MY_TEST_URL = "https://hooks.slack.com/workflows/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"  # variable = data

html_string = """
    <p>
        Here <i>is</i> a <strike>paragraph</strike> with a <b>lot</b> of formatting.
    </p>
    <br>
    <code>Code sample</code> & testing escape.
    <ul>
        <li>
            <a href="https://www.google.com">Google</a>
        </li>
        <li>
            <a href="https://www.amazon.com">Amazon</a>
        </li>
    </ul>
"""
parser = SlackHTMLParser()
slack_message = parser.parse(html_string)
slack = SlackWebhookBot(MY_TEST_URL)
slack.send(slack_message)
