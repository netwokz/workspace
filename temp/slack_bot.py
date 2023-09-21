from html.parser import HTMLParser
import re
from typing import Any, List, Tuple, Dict
import os
import requests
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class SlackWebhookBot:
    def __init__(self, webhook_url: str, timeout: int = 15):
        """Class to send messages to a provided Slack webhook URL.

        You can read more about Slack's Incoming Webhooks here:
            https://api.slack.com/messaging/webhooks

        Args:
            webhook_url: The webhook URL to send a message to.  Typically
                formatted like "https://hooks.slack.com/services/...".

        Kwargs:
            timeout: Number of seconds before the request will timeout.
                This is used to prevent a hang and is set to a default
                value of 15 seconds.
        """
        self.webhook_url = webhook_url
        self.timeout = timeout
        self.headers = {
            'Content-Type': 'application/json',
        }

    def send(self, message: str, subject: str = 'New message!') -> bool:
        """Sends a formatted message to the webhook URL.

        Args:
            message: Plain text string to send to Slack.

        Kwargs:
            subject: The subject of the message that will appear in the notification
                preview.

        Returns:
            A boolean representing if the request was successful.
        """
        success = False
        payload = self.format_message(subject, message)
        try:
            r = requests.post(
                self.webhook_url,
                headers=self.headers,
                json=payload,
                timeout=self.timeout
            )
        except requests.Timeout:
            logger.error(
                'Timeout occurred when trying to send message to Slack.')
        except requests.RequestException as e:
            logger.error(f'Error occurred when communicating with Slack: {e}.')
        else:
            success = True
            logger.info('Successfully sent message to Slack.')

        return success


class SlackHTMLParser(HTMLParser):
    def __init__(self, *args, **kwargs):
        """Escapes and converts an HTML string to Slack flavored
        Markdown (mrkdwn).

        More about Slack's Markdown Flavor (mrkdwn) can be seen here:
            https://api.slack.com/reference/surfaces/formatting

        Call using `SlackHTMLParser(message_body).parse()`.
        """
        super().__init__(*args, **kwargs)
        self.slack_message = ''
        self.ignore_tag = False  # Used to skip tags we don't care about
        self.line_break = '::LINE::BREAK::'  # Unique sequence for swapping a <br>

    def format_message(self, subject: str, body: str) -> Dict:
        """Formats the subject and message body into Slack blocks.

        Args:
            subject: Subject that will appear on the notification popup.
            body: The full message body.

        Returns:
            A dictionary payload with Slack block formatting.
        """
        return {
            'text': subject,
            'blocks': [
                {
                    'type': 'section',
                    'text': {
                        'type': 'mrkdwn',
                        'text': f'*{subject}*',
                    },
                },
                {
                    'type': 'section',
                    'text': {
                        'type': 'mrkdwn',
                        'text': body,
                    },
                },
            ],
        }

    def handle_starttag(self, tag: str, attrs: List[Tuple[str, Any]]):
        """Called when the opening of a tag is encountered.

        The idea here is to swap out the tag with the respective mrkdwn
        symbol.

        Args:
            tag: Lowercase name of the HTML tag.  E.G. `br` or `i`.
            attrs: List of tuples with the tuple having the following form:
                (attribute name, value).  E.G. ('href', 'www.example.com').
        """
        if tag in ['i', 'em']:
            self.slack_message += '_'
        elif tag in ['b', 'strong']:
            self.slack_message += '*'
        elif tag == 'strike':
            self.slack_message += '~'
        elif tag in ['br', 'p', 'ul']:
            self.slack_message += self.line_break
        elif tag == 'li':
            self.slack_message += f'{self.line_break}- '
        elif tag == 'code':
            self.slack_message += '`'
        elif tag == 'a':
            href = [x[1] for x in attrs if x[0] == 'href']
            if len(href) > 0:
                self.slack_message += f'<{href[0]}|'
        else:
            self.ignore_tag = True

    def handle_data(self, data: str):
        """Handles the data within a tag.

        This is called after `handle_starttag` and before `handle_endtag`.

        We will also escape the following text per Slack's documentation:
        - '&' -> '&amp;'
        - '<' -> '&lt;'
        - '>' -> '&gt;'

        Args:
            data: The data/string within the HTML tag.
        """
        if not self.ignore_tag:
            self.slack_message += data\
                .replace('&', '&amp;')\
                .replace('<', '&lt;')\
                .replace('>', '&gt;')

    def handle_endtag(self, tag: str):
        """Called when the closing of a tag is encountered.

        The idea here is to swap out the tag with the respective mrkdwn
        symbol.  This is basically the same as the handle_starttag.

        Args:
            tag: Lowercase name of the HTML tag.  E.G. `br` or `i`.
        """
        if tag in ['i', 'em']:
            self.slack_message += '_'
        elif tag in ['b', 'strong']:
            self.slack_message += '*'
        elif tag == 'strike':
            self.slack_message += '~'
        elif tag == 'p':
            self.slack_message += self.line_break
        elif tag == 'code':
            self.slack_message += '`'
        elif tag == 'a':
            self.slack_message += '>'

        self.ignore_tag = False

    def parse(self, html_string: str) -> str:
        """Parses a given HTML string and applies simple formatting.

        Note that we need to apply the line break replacing here
        instead of with the handle tag methods.

        Args:
            html_string: The HTML string to convert to Slack mrkdwn.

        Returns:
            A formatted Slack mrkdwn string.
        """
        self.feed(html_string)
        return re.sub(
            r'^(\n)+',  # Remove the leading line breaks
            '',
            ' '.join(self.slack_message.split()).replace(self.line_break, '\n')
        )


html_string = '''
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
'''
webhook_url = os.environ.get('SLACK_WEBHOOK_URL')
parser = SlackHTMLParser()
slack_message = parser.parse(html_string)
slack = SlackWebhookBot(webhook_url)
slack.send(slack_message)
