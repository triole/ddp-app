import requests
import logging

from django import template
log = logging.getLogger(__name__)
register = template.Library()


@register.simple_tag(takes_context=True)
def httpget(context, url):
    r = requests.get(url, auth=('user', 'pass'))
    if r.status_code == 200:
        return r.text
    else:
        log.error("View httpget failed %s, %s", url, r.status_code)
    return ''


@register.simple_tag()
def hello():
    return 'world'
