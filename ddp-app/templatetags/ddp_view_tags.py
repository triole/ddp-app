import logging
import re
from os.path import join as pj
from os.path import realpath
from urllib import parse

import requests
import yaml
from django import template

log = logging.getLogger(__name__)
register = template.Library()


class Conf():
    def __init__(self):
        self.scriptname = realpath(__file__)
        self.scriptdir = '/'.join(self.scriptname.split('/')[:-1])
        self.basedir = re.search(r'.*(?=\/)', self.scriptdir).group(0)
        self.conf_file = pj(self.basedir, 'conf.yaml')
        self.conf = self.load_config()

    def load_config(self):
        with open(self.conf_file, 'r') as stream:
            try:
                return(yaml.safe_load(stream))
            except yaml.YAMLError as exc:
                print(exc)

    def abs_url(self, str):
        return parse.urljoin(self.get_base_url(), str)

    def get_base_url(self):
        return self.conf['base_url']


c = Conf()


@register.simple_tag(takes_context=True)
def httpget(context, url):
    furl = c.abs_url(url)
    print('Request ' + url)
    r = requests.get(furl, auth=('user', 'pass'))
    if r.status_code == 200:
        return r.text
    else:
        log.error("View httpget failed %s, %s", furl, r.status_code)
    return ''


@register.simple_tag()
def hello():
    return 'world man'
