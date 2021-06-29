import logging as logging
import re
from os.path import join as pj
from os.path import realpath

import requests
import toml
from django import template
from django.utils.safestring import mark_safe

import pypandoc

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
                self.log('Load config :' + str(d))
                return(d)
            except Exception as e:
                raise(e)

    def abs_url(self, str):
        if str.startswith('/'):
            str = str[1:]
        return self.conf_base_url() + '/' +\
            str + '.' + self.conf_content_type()

    def conf_base_url(self):
        r = self.conf['base_url']
        if r.endswith('/') is False:
            r += '/'
        return r

    def conf_content_type(self):
        return self.conf['content_type']

    def log(self, s):
        logger.info(str(s))


c = Conf()


def download_file(url, tempfile):
    furl = c.abs_url(url)
    c.log('Download ' + furl + ' to ' + tempfile)
    res = requests.get(furl)
    file = open(tempfile, 'wb')
    file.write(res.content)
    file.close


def request(url):
    r = ''
    furl = c.abs_url(url)
    c.log('Request ' + furl)
    res = requests.get(furl)
    if res.status_code == 200:
        r = res.text
    else:
        c.log('Request failed ' + str(res.status_code) + ': ' + furl)
    return r


def serve_md(str):
    return mark_safe(
        pypandoc.convert_text(str, 'html', format='md')
    )


def serve_docx(filename):
    r = ''
    # if file does not exist, pandoc throws an exception
    try:
        r = pypandoc.convert_file(filename, 'html', format='docx')
    except RuntimeError:
        pass
    return mark_safe(r)


@register.simple_tag(takes_context=False)
def get(url):
    c.log(c.conf_content_type())
    if c.conf_content_type() == 'md':
        str = request(url)
        return serve_md(str)
    if c.conf_content_type() == 'docx':
        tempfile = pj('/tmp/', url + '.docx')
        download_file(url, tempfile)
        return serve_docx(tempfile)
