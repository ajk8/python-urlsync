"""
urlsync -- Download a file from the interwebs and stash it locally...ONCE!

Usage: urlsync FROM [TO] [options]

Options:
  -h --help   print this help message
  -f --force  force re-download
  --insecure  ignore ssl security
"""

import docopt
import funcy
import os
import requests
requests.packages.urllib3.disable_warnings()


class _Die(Exception):
    """Print an error message and return an error code"""
    pass


def _info(msg):
    """Print an info message"""
    print('[INFO] {0}'.format(msg))


def _warn(msg):
    """Print a warning message"""
    print('[WARNING] {0}'.format(msg))


def _error(msg):
    """Print an error message"""
    print('[ERROR] {0}'.format(msg))


def _200_or_die(method, src, verify, stream):
    """Make a request and return the response if it succeeded"""

    # make the request
    try:
        response = getattr(requests, method)(src, verify=verify, stream=stream)

    # there was an ssl error
    except requests.exceptions.SSLError:
        raise _Die('certificate could not be verified')

    # only allow 200 and 307 (temporary redirect)
    if response.status_code not in (200, 307):
        raise _Die('could not make {0} request to url'.format(method))

    return response


def sync(src, dest=None, insecure=False, force=False):
    """
    Sync a file from a url to a local file based on file size

    :src:       URL of remote file to sync
    :dest:      local path of local file to sync
    :insecure:  allow ignoring ssl certificates
    :force:     download even if files have the same size
    """

    try:

        # process the source parameter
        src = src.strip()
        if not funcy.re_find(r'\w+://', src):
            src = 'http://{0}'.format(src)

        # set whether or not to verify ssl
        verify = not insecure

        # transform the url after any redirects
        response = _200_or_die('head', src, verify, False)
        if response.url != src:
            src = response.url
        elif 'location' in response.headers.keys():
            src = response.headers['location']

        # process the dest parameter
        if not dest:
            dest = src.split('?')[0].split('/')[-2 if src.endswith('/') else -1]

        # compare size with an existing file if it exists
        if os.path.exists(dest):
            size_dest = int(os.path.getsize(dest))

            # get the remote size by just hitting the headers
            response = _200_or_die('head', src, verify, False)
            if 'content-length' not in response.headers.keys():
                _warn('could not determine remote file size')

            # if they're the same, we don't download
            else:
                size_src = int(response.headers['content-length'])
                if size_dest == size_src:
                    _info('{0} already exists and is the same version'.format(dest))
                    return 0

        # go ahead
        _info('downloading to {0}'.format(dest))
        response = _200_or_die('get', src, verify, True)
        with open(dest, 'wb') as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)

    except _Die as e:
        _error(str(e))
        return 1


def main():
    """Execute sync method from the command line"""

    # grab the arguments out of the docstring at the top
    args = docopt.docopt(__doc__)
    return sync(args['FROM'], args['TO'], args['--insecure'], args['--force'])
