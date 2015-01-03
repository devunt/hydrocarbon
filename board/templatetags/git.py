from django.template import Library


register = Library()

try:
    with open('.git/logs/HEAD', 'r') as f:
        f.seek(0, 2)
        fsize = f.tell()
        f.seek(max(fsize - 1024, 0), 0)
        line = f.readlines()[-1]
    VERSION = line.split()[1][:7]
except:
    VERSION = 'unknown'

@register.simple_tag
def git_short_version():
    return VERSION
