#!/usr/bin/env python3

# --------------------------------------------------------------------------
# HTTP Status Check
#
# Check a list of web sites HTTP Status.
# --------------------------------------------------------------------------


class TextColors:
    RED = '\033[91m'
    BLACK = '\033[0m'
    BLUE = '\033[34'


import argparse
import time
import datetime
import ssl


# Create a global SSL context that ignores certificate validation
if hasattr(ssl, '_create_unverified_context'):
    ssl._create_default_https_context = ssl._create_unverified_context


"""
Verify that Python 3 is installed
"""
import sys

if sys.version_info < (3, 0, 0):
    print('\n{0}Python 3 is needed to run this script.  Visit the Python download page to install Python 3:  '
          'https://www.python.org/downloads{1}\n'.format(TextColors.RED, TextColors.BLACK))
    exit(1)


"""
Lets make sure the Request library is installed (http://docs.python-requests.org/en/latest)
"""
try:
    import requests

except ImportError:
    print('\n{0}You will need to install the Python Requests library to run this script.  Visit '
          'the Python Request site for installation directions:  '
          'http://docs.python-requests.org/en/latest.{1}'.format(TextColors.RED, TextColors.BLACK))
    exit(1)


class RequestResult(object):

    def __init__(self, httpstatus, message):
        self.httpstatus = httpstatus
        self.message = message


def logo():

    hello = r'''

             _____  _____  ___    __ _        _                  ___ _               _
      /\  /\/__   \/__   \/ _ \  / _\ |_ __ _| |_ _   _ ___     / __\ |__   ___  ___| | __
     / /_/ /  / /\/  / /\/ /_)/  \ \| __/ _` | __| | | / __|   / /  | '_ \ / _ \/ __| |/ /
    / __  /  / /    / / / ___/   _\ \ || (_| | |_| |_| \__ \  / /___| | | |  __/ (__|   <
    \/ /_/   \/     \/  \/       \__/\__\__,_|\__|\__,_|___/  \____/|_| |_|\___|\___|_|\_\
                                                                                     v0.80
    '''

    print(hello)

    print(time.strftime("%c"))


def satus_check(filename, proxy, followredirect, output, verbose, timeout):

    print('\n')
    print('[+] Performing HTTP Request...\n')

    totalurls = 0
    total200 = 0
    total302 = 0
    httprequest = []

    try:

        from urllib.parse import urlparse

        # Create the Proxy Server.  Example:  {'http': 'http://127.0.0.1:8080'}
        o = urlparse(proxy)
        proxies = {o.scheme: o.geturl()}

        # Create the HTTP Headers
        headers = {'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:30.0) Gecko/20100101 Firefox/30.0',
                   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                   'Accept-Language': 'en-us,en;q=0.5',
                   'Accept-Encoding': 'gzip, deflate',
                   'DNT': '1',
                   'Connection': 'close'}

        # Determine if we are using a proxy and make the HTTP Request
        if len(proxy) < 1:
            proxies = None

        counter = 0

        # Get the number of URLs in the file.  This is used for the status message.
        number_urls = file_length(filename)

        with open(filename, 'r') as f:

            verbosemessage = ''
            statuscode = ''

            for line in f:

                if len(line) > 0:

                    # Displays status of HTTP Request
                    if verbose is not True:
                        counter += 1
                        sys.stdout.write('\rProcessing {0} of {1}'.format(counter, number_urls))
                        sys.stdout.flush()

                    line = line.replace("\n", "")

                    try:

                        r = requests.get(line, proxies=proxies, headers=headers, allow_redirects=followredirect, verify=False, timeout=int(timeout))

                        if len(r.history) > 0:
                            statuscode = 302
                        else:
                            statuscode = r.status_code

                        if statuscode == 200:

                            total200 += 1

                            verbosemessage = '{0} - {1}'.format(statuscode, line, )
                            httprequest.append(RequestResult(statuscode, line))

                        elif statuscode == 302:

                            redirects = ''
                            total302 += 1

                            if len(r.history) > 0:

                                for redirect in r.history:
                                    redirects += ' > ' + truncate_url(redirect.url)

                            verbosemessage = '{0} - {1} {2}'.format(statuscode, line, redirects)
                            httprequest.append(RequestResult(statuscode, '{0} {1}'.format(line, redirects)))

                        else:
                            verbosemessage = '{0} - {1}'.format(statuscode, line)
                            httprequest.append(RequestResult(statuscode, line))

                    except requests.exceptions.Timeout as te:
                        verbosemessage = 'Timeout - {0}'.format(line)
                        httprequest.append((RequestResult('Timeout', line)))

                    except requests.exceptions.RequestException as e:
                        verbosemessage = 'Request Error - {0}'.format(line)
                        httprequest.append(RequestResult('Request Error', '{0} - {1}'.format(line, e)))

                    totalurls += 1

                    if verbose is True:
                        print(verbosemessage)

    except IOError:
        print('\n{0}The file of {1} could not be found.{2}'.format(TextColors.RED, filename, TextColors.BLACK))
        exit(1)

    # Display results to the console
    if verbose is not True:
        display_results(httprequest)

    # Save results to a text file
    if output is True:
        save_results(httprequest)

    # Display some stats
    print('\n{0} URLs have been analyzed.'.format(totalurls))
    print('{0} URLs have a HTTP Status of 200'.format(total200))
    print('{0} URLS have a HTTP status of 302'.format(total302))
    print('\n')


def display_results(results):

    # Change status message to completed
    sys.stdout.write('\rProcessing Completed')
    sys.stdout.flush()

    print('\n')

    for r in results:
        if r.httpstatus == 200:
            print('{0} - {1}'.format(r.httpstatus, r.message))
        elif r.httpstatus == 302:
            print('{0} - {1}'.format(r.httpstatus, r.message))
            #print('{0}{1}{2} - {3}'.format(TextColors.BLUE, str(r.httpstatus), TextColors.BLACK, r.message))
        else:
            print('{0}{1}{2} - {3}'.format(TextColors.RED, str(r.httpstatus), TextColors.BLACK, r.message))


def save_results(results):

    thefile = open(create_file_name('HttpStatusCheck'), 'w')

    for r in results:
        thefile.write('{0},{1}\n'.format(r.httpstatus, r.message))

    thefile.close()

    print('\nYour file has been saved as {0}'.format(thefile.name))


def create_file_name(filename, fmt='{filename}_%Y%m%d%H%M%S.csv'):
    return datetime.datetime.now().strftime(fmt).format(filename=filename)


def truncate_url(url):
    return (url[:75] + '..') if len(url) > 75 else url


def file_length(filelocation):

    with open(filelocation) as f:
        for i, l in enumerate(f):
            pass
    return i + 1


def main():

    parse = argparse.ArgumentParser()
    parse.add_argument('--file', action='store', dest='file', required=True, help='Type in the location and name of the file to process.')
    parse.add_argument('--proxy', action='store', dest='proxy', required=False, help='Enter in the address of the proxy.  For example:  http://127.0.0.1:8080')
    parse.add_argument('--timeout', action='store', dest='timeout', required=False, default=5, help='Enter in the number of seconds for the HTTP Request before it timeouts.  The default is 5 seconds')
    parse.add_argument('-r', action='store_const', dest='redirect', const=True, default=False, help='Follow redirects when there is a 302')
    parse.add_argument('-o', action='store_const', dest='output', const=True, default=False, help='Write the results to a file.  The file will be saved in the same location as this script')
    parse.add_argument('-v', action='store_const', dest='verbose', const=True, default=False, help='Display error messages')


    args = parse.parse_args()

    if args.file is None:
        parse.print_help()
        print("\n")
        exit(1)

    filename = str(args.file)
    proxy = str(args.proxy)
    timeout = args.timeout
    followredirect = args.redirect
    output = args.output
    verbose = args.verbose

    logo()

    print('\nLoading URLs from {0}'.format(filename))

    satus_check(filename, proxy, followredirect, output, verbose, timeout)


if __name__ == "__main__":
    main()