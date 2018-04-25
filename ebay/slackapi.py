"""
curl -X POST --data-urlencode
'payload={"channel": "#webjhook", "username": "webhookbot",
"text": "This is posted to #webjhook and comes from a bot named webhookbot.",
"icon_emoji": ":ghost:"}'
https://hooks.slack.com/services/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

payload1={"text": "This is a line of text in a channel.\nAnd this is another line of text."}
payload2={"text": "A very important thing has occurred! <https://alert-system.com/alerts/1234|Click here> for details!",
          "username": "Webjhook",
          "channel": "#enqstripe"}
"""

import logging
import os
from slacker import Slacker
from django.conf import settings

slack = Slacker(settings.SLACK_SECRET_KEY)
slack_logger = logging.getLogger('django.request')
TEST_CHANNEL = os.environ.get('TEST_SLACK_CHANNEL', None)


channel_details = {
    "#xpressbuyer": {"username": settings.ENVIRON + ' software',
                     "icon_url": None,
                     "icon_emoji": ":email:"},
    "@Vishal": {},
}


def bold(text):
    """bold markdown"""
    return "*%s*" % text


def blockquote(text):
    """block quote markdown
    :param text:
    """
    lines = text.splitlines()
    lines_blockquote = ['> ' + line for line in lines]
    new_text = '\n'.join(lines_blockquote)
    return new_text


def post_to_slack(message, channel, username=None, icon_url=None, icon_emoji=None):
    try:
        channel = TEST_CHANNEL or channel
        channel_info = channel_details.get(channel, dict())
        slack.chat.post_message(
            channel=channel,
            text=message,
            username=username or channel_info.get("username"),
            icon_url=icon_url or ((not icon_emoji) and channel_info.get("icon_url")) or None,
            icon_emoji=icon_emoji or ((not icon_url) and channel_info.get("icon_emoji")) or None,
            as_user=False
        )
    except Exception as e:
        slack_logger.error('Error post message to slack\n', exc_info=True)


def send_notification(message, channel):
    try:
        post_to_slack(message, channel)
    except Exception as e:
        slack_logger.error('Error send notification to slack\n', exc_info=True)