#!/usr/bin/env python3

# --------------------------------------------------------------------------
# FileListCreator.py
#
# This script will search for files with a specific file extension(s)
# entered by the user.  The user will have the option to display the list
# of files on the screen and/or save to a file.
# --------------------------------------------------------------------------

import argparse
import os
import time
import datetime


class TextColors:
    RED = '\033[91m'
    BLACK = '\033[0m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'


def logo():
    """
    Displays the script logo and help topics.
    """

    hello = r'''

      _____ _ _         _     _     _       ____                _             
     |  ___(_) | ___   | |   (_)___| |_    / ___|_ __ ___  __ _| |_ ___  _ __ 
     | |_  | | |/ _ \  | |   | / __| __|  | |   | '__/ _ \/ _` | __/ _ \| '__|
     |  _| | | |  __/  | |___| \__ \ |_   | |___| | |  __/ (_| | || (_) | |   
     |_|   |_|_|\___|  |_____|_|___/\__|   \____|_|  \___|\__,_|\__\___/|_|   
                                                                      v0.77
    '''

    print(hello)

    print('Example --format if search is being performed in /Users/Bob/tmp: \n')
    print('W = http://wwww.somewebsiteinthecloud.com/tmp/file1.aspx  (NOTE:  Make sure to add the URL to the --prepend argument.)')
    print('F = /Users/Bob/tmp/file1.aspx')
    print('S = /tmp/file1.aspx ')
    print('\n')


def searchForFiles(fileTypes, searchIn, prepend, format, saveLocation, noPrint):
    """
    Handles the seaching of file types

    :param fileTypes:  A comma delimited string of file extensions to search for.  Example:  aspx,html.
    :param searchIn:  The location to start the search in.
    :param prepend:  The string that will be prepended to the file location result.
    :param format:  Format of the file location result.
    :param saveLocation:  The location to save the results to.
    :param noPrint:  Do not print the results to screen
    """

    fileList = []
    filePath = ''

    print('[+] Searching for files in {0} \n'.format(searchIn))

    for t in fileTypes:
        for dirPath, dirName, files in os.walk(searchIn):
            for name in files:
                if name.lower().endswith(t):

                    f = prepend + os.path.join(dirPath, name)

                    if format == "W":
                        fileList.append(f.replace(searchIn, '').replace('\\','/'))
                    elif format == "F":
                        fileList.append(f)
                    elif format == "S":
                        fileList.append(f.replace(searchIn, ''))
                    else:
                        fileList.append(f.replace(searchIn, '').replace('\\','/'))
    
    # Print results to the screen
    if noPrint == False and len(fileList) > 0:
        for fl in fileList:
            print(fl)
        print('\n')
    
    print('[+] Search complete with {0} files found.'.format(str(len(fileList))))

    # If the user added the --save-to argument save the results to file.
    if len(saveLocation) > 0 and len(fileList) > 0:
        save_results(fileList, saveLocation)

    print('\n')


def save_results(results, saveLocation):
    """
    Saves the results in the selected display format to the
    location specified in the --save-to argument.

    :param results: List of file locations
    :param saveLocation:  Location to create and save the file
    """

    saveTo = os.path.join(saveLocation, create_file_name('FilesList'))

    thefile = open(saveTo, 'w')

    for f in results:
        thefile.write(f + '\n')

    thefile.close()
    
    print('\nYour file has been saved as {0}'.format(saveTo))


def create_file_name(filename, fmt='{filename}_%Y%m%d%H%M%S.txt'):
    return datetime.datetime.now().strftime(fmt).format(filename=filename)


def main():

    parse = argparse.ArgumentParser(description=logo())
    parse.add_argument('--search-in', action='store', dest='searchIn', required=True, help='The path to search for files in')
    parse.add_argument('--file-types', action='store', dest='fileType', required=True, help='A comma delimited string of file extensions to search for.  Example:  aspx,html')
    parse.add_argument('--prepend', action='store', dest='prepend', required=False, help='Prepend the file locations with something')
    parse.add_argument('--format', action='store', dest='outputFormat', required=False, default='W', help='Results output format:  W = Web, F = Full Path, S = Shortend Path.  Default is Web.')
    parse.add_argument('--save-to', action='store', dest='saveLocation', required=False, help='The location to save the results to')
    parse.add_argument('-np', action='store_const', dest='noPrint', const=True, default=False, help='Do not print results to screen')

    args = parse.parse_args()

    # Perform some argument validation
    # ----------------------------------
    isError = False

    if not os.path.exists(args.searchIn):
        print("{0}The --search-in path {1} does not exists.{2}".format(TextColors.RED, str(args.searchIn), TextColors.BLACK))
        isError = True
        
    if args.saveLocation is None and args.noPrint == True:
        print("{0}Since the -np argument is set the --save-to argument must be specified.{1}".format(TextColors.RED, TextColors.BLACK))
        isError = True

    if args.saveLocation is not None and os.path.exists(args.saveLocation) == False:
        print("{0}The --save-to path {1} does not exists.{2}".format(TextColors.RED, str(args.saveLocation), TextColors.BLACK))
        isError = True
     
    if isError:
        #parse.print_help()
        print('\n')
        exit(1)

    # Retrieve the arguments
    # ----------------------------------
    fileTypes = []
    prepend = ''
    saveLocation = ''

    fileTypes = str(args.fileType).split(",")
    
    if args.prepend is not None:
        prepend = str(args.prepend)

    if args.saveLocation is not None:
        saveLocation = str(args.saveLocation)

    # Perform the search
    # ----------------------------------
    searchForFiles(fileTypes, str(args.searchIn), prepend, str(args.outputFormat).upper(), saveLocation, args.noPrint)


if __name__ == "__main__":
    main()
