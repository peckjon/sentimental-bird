import re

FNAME_MATCH = re.compile(r'/([^/]+)$')  # From the last slash to the end of the string 
PREFIX = re.compile(r'([^:]+://)(/)?(.+)')   # Check for a prefix like data://
def getParentAndBase(path):
    match = PREFIX.match(path)
    if match is None:
        base = FNAME_MATCH.search(path)
        if base is None:
            raise Exception('Invalid path')
        parent = FNAME_MATCH.sub('', path)
        return parent, base.group(1)
    else:
        prefix, leading_slash, uri = match.groups()
        parts = uri.split('/')
        parent_path = '/'.join(parts[:-1])

        if leading_slash is not None:
            parent_path = '{prefix}/{uri}'.format(prefix=prefix, uri='/'.join(parts[:-1]))
        else:
            parent_path = '{prefix}{uri}'.format(prefix=prefix, uri='/'.join(parts[:-1]))
        return parent_path, parts[-1]

def pathJoin(parent, base):
    if parent.endswith('/'):
        return parent + base
    return parent + '/' + base
