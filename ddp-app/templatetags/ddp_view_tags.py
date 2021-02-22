# import logging
import re
from os.path import join as pj
from os.path import realpath

import requests
import yaml
from django import template
from django.utils.safestring import mark_safe

import pypandoc

# from urllib import parse

# log = logging.getLogger(__name__)
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
                r = yaml.safe_load(stream)
                self.log('Config loaded: ' + str(r))
                return r
            except yaml.YAMLError as exc:
                self.log(exc)

    def abs_url(self, str):
        if str.startswith('/'):
            str = str[1:]
        return self.conf_base_url() + self.conf_content_type() + '/' +\
            str + '.' + self.conf_content_type()
        # return parse.urljoin(
        #     self.conf_base_url(), self.conf_content_type() + '/',
        #     '/' + str + '.' + self.conf_content_type()
        # )

    def conf_base_url(self):
        r = self.conf['base_url']
        if r.endswith('/') is False:
            r += '/'
        return r

    def conf_content_type(self):
        return self.conf['content_type']

    def log(self, str):
        print('=== DDP Log === ' + str)


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
    res = requests.get(furl, auth=('user', 'pass'))
    if res.status_code == 200:
        r = res.text
    else:
        c.log('View httpget failed ' + furl + str(res.status_code))
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
    if c.conf_content_type() == 'md':
        c.log('Serve md')
        str = request(url)
        return serve_md(str)
    if c.conf_content_type() == 'docx':
        c.log('Serve docx')
        tempfile = pj('/tmp/', url + '.docx')
        download_file(url, tempfile)
        return serve_docx(tempfile)
