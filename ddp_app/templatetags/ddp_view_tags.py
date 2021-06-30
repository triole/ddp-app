import logging as logging
import re
from os.path import join as pj
from os.path import realpath

import requests
import toml

import pypandoc
from django import template
from django.utils.safestring import mark_safe

logging.basicConfig(
    level=logging.INFO,
)
logger = logging.getLogger('ddp_app')

register = template.Library()


class Conf():
    def __init__(self):
        self.scriptname = realpath(__file__)
        self.scriptdir = '/'.join(self.scriptname.split('/')[:-1])
        self.basedir = re.search(r'.*(?=\/)', self.scriptdir).group(0)
        self.conf_file = pj(self.basedir, 'conf.toml')
        self.conf = self.load_config()

    def load_config(self):
        self.log(self.conf_file)
        with open(self.conf_file, 'r') as stream:
            try:
                data = stream.read()
                d = toml.loads(data)
                self.log('Load config: ' + str(d))
                return(d)
            except Exception as e:
                raise(e)

    def abs_url(self, str):
        if str.startswith('/'):
            str = str[1:]
        return self.conf_base_url() + '/' +\
            str + '.md'

    def conf_base_url(self):
        r = self.conf['base_url']
        if r.endswith('/') is False:
            r += '/'
        return r

    def log(self, s):
        logger.info(str(s))


conf = Conf()


def request(url):
    r = ''
    furl = conf.abs_url(url)
    conf.log('Request ' + furl)
    res = requests.get(furl)
    if res.status_code == 200:
        r = res.text
    else:
        conf.log('Request failed ' + str(res.status_code) + ': ' + furl)
    return r


def serve_md(str):
    return mark_safe(
        pypandoc.convert_text(str, 'html', format='md')
    )


@register.simple_tag(takes_context=False)
def get(url):
    str = request(url)
    return serve_md(str)


@register.inclusion_tag(filename='header.html', takes_context=False)
def load_frontend_libs():
    r = requests.get(conf.conf_base_url() + '/header.html')
    return r.text
