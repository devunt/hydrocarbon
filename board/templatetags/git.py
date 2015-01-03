import subprocess

from django.template import Library


register = Library()

try:
    head = subprocess.Popen('git rev-parse --short HEAD',
        shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    VERSION = head.stdout.readline().strip().decode()
except:
    VERSION = 'unknown'

@register.simple_tag
def git_short_version():
    return VERSION
