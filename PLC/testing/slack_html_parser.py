import re
from html.parser import HTMLParser
from typing import Any, List, Tuple


class SlackHTMLParser(HTMLParser):
    def __init__(self, *args, **kwargs):
        """Escapes and converts an HTML string to Slack flavored
        Markdown (mrkdwn).

        More about Slack's Markdown Flavor (mrkdwn) can be seen here:
            https://api.slack.com/reference/surfaces/formatting

        Call using `SlackHTMLParser(message_body).parse()`.
        """
        super().__init__(*args, **kwargs)
        self.slack_message = ""
        self.ignore_tag = False  # Used to skip tags we don't care about
        self.line_break = "::LINE::BREAK::"  # Unique sequence for swapping a <br>

    def handle_starttag(self, tag: str, attrs: List[Tuple[str, Any]]):
        """Called when the opening of a tag is encountered.

        The idea here is to swap out the tag with the respective mrkdwn
        symbol.

        Args:
            tag: Lowercase name of the HTML tag.  E.G. `br` or `i`.
            attrs: List of tuples with the tuple having the following form:
                (attribute name, value).  E.G. ('href', 'www.example.com').
        """
        if tag in ["i", "em"]:
            self.slack_message += "_"
        elif tag in ["b", "strong"]:
            self.slack_message += "*"
        elif tag == "strike":
            self.slack_message += "~"
        elif tag in ["br", "p", "ul"]:
            self.slack_message += self.line_break
        elif tag == "li":
            self.slack_message += f"{self.line_break}- "
        elif tag == "code":
            self.slack_message += "`"
        elif tag == "a":
            href = [x[1] for x in attrs if x[0] == "href"]
            if len(href) > 0:
                self.slack_message += f"<{href[0]}|"
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
            self.slack_message += data.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    def handle_endtag(self, tag: str):
        """Called when the closing of a tag is encountered.

        The idea here is to swap out the tag with the respective mrkdwn
        symbol.  This is basically the same as the handle_starttag.

        Args:
            tag: Lowercase name of the HTML tag.  E.G. `br` or `i`.
        """
        if tag in ["i", "em"]:
            self.slack_message += "_"
        elif tag in ["b", "strong"]:
            self.slack_message += "*"
        elif tag == "strike":
            self.slack_message += "~"
        elif tag == "p":
            self.slack_message += self.line_break
        elif tag == "code":
            self.slack_message += "`"
        elif tag == "a":
            self.slack_message += ">"

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
        return re.sub(r"^(\n)+", "", " ".join(self.slack_message.split()).replace(self.line_break, "\n"))  # Remove the leading line breaks
