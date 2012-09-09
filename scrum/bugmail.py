from __future__ import absolute_import

import logging
import poplib
import re
from email.parser import Parser

from django.conf import settings

from scrum.models import BZProduct


BUG_ID_RE = re.compile(r'\[Bug (\d+)\]')
BUG_SUMMARY_RE = re.compile(r'\[[^]]\](?: New:)? (.+)$')
# 'admin' also comes through but is for account creation.
BUGZILLA_TYPES = (
    'new',
    'changed',
)
BUGZILLA_INFO_HEADERS = (
    'product',
    'component',
    'severity',
    'status',
    'priority',
    'assigned-to',
    'target-milestone',
)
log = logging.getLogger(__name__)


def get_messages(delete=True, max_get=50):
    """
    Return a list of `email.message.Message` objects from the POP3 server.
    :return: list
    """
    messages = []
    conn = poplib.POP3_SSL(settings.BUGMAIL_HOST)
    conn.user(settings.BUGMAIL_USER)
    conn.pass_(settings.BUGMAIL_PASS)
    num_messages = len(conn.list()[1])
    num_get = max(num_messages, max_get)
    for msgid in range(1, num_get + 1):
        msg_str = '\n'.join(conn.retr(msgid)[1])
        msg = Parser().parsestr(msg_str)
        if is_bugmail(msg):
            messages.append(msg)
            if delete:
                conn.dele(msgid)
    conn.quit()
    return messages


def is_bugmail(msg):
    """
    Return true if the Message is from Bugzilla and we care about it.
    :param msg: email.message.Message object
    :return: bool
    """
    all_products = BZProduct.objects.full_list
    if msg.get('x-bugzilla-type', None) in BUGZILLA_TYPES:
        prod = msg['x-bugzilla-product']
        comp = msg['x-bugzilla-component']
        if prod in all_products:
            if all_products[prod] and comp not in all_products[prod]:
                return False
            return True
    return False


def get_bug_id(msg):
    """
    Return the id of the bug the message is about.
    :param msg: email.message.Message object
    :return: int
    """
    if 'x-bugzilla-id' in msg:
        return int(msg['x-bugzilla-id'])
    m = BUG_ID_RE.search(msg['subject'])
    if m:
        return int(m.group(1))
    return None


def get_bugmails(delete=True):
    bugmails = {}
    for msg in get_messages(delete=delete):
        bid = get_bug_id(msg)
        if bid:
            bugmails[bid] = msg
    return bugmails


def extract_bug_info(msg):
    """
    Extract the useful info from the bugmail message and return it.
    :param msg: message
    :return: dict
    """
    info = {
        'summary': BUG_SUMMARY_RE.match(msg['subject']).group(1),
    }
    for h in BUGZILLA_INFO_HEADERS:
        val = msg.get('x-bugzilla-' + h)
        if val:
            info[h.replace('-', '_')] = val
    return info
