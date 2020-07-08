from random import choice
import string
import argparse
import time
import datetime

def logo():
    """
    Displays the script logo and help topics.
    """

    hello = r'''
      ____     _____    ____                 _   _     ____         ____  U _____ u _   _   U _____ u   ____        _       _____   U  ___ u   ____     
     / __"| u |_ " _|U |  _"\ u     ___     | \ |"| U /"___|u    U /"___|u\| ___"|/| \ |"|  \| ___"|/U |  _"\ u U  /"\  u  |_ " _|   \/"_ \/U |  _"\ u  
    <\___ \/    | |   \| |_) |/    |_"_|   <|  \| |>\| |  _ /    \| |  _ / |  _|" <|  \| |>  |  _|"   \| |_) |/  \/ _ \/     | |     | | | | \| |_) |/  
     u___) |   /| |\   |  _ <       | |    U| |\  |u | |_| |      | |_| |  | |___ U| |\  |u  | |___    |  _ <    / ___ \    /| |\.-,_| |_| |  |  _ <    
     |____/>> u |_|U   |_| \_\    U/| |\u   |_| \_|   \____|       \____|  |_____| |_| \_|   |_____|   |_| \_\  /_/   \_\  u |_|U \_)-\___/   |_| \_\   
      )(  (__)_// \\_  //   \\_.-,_|___|_,-.||   \\,-._)(|_        _)(|_   <<   >> ||   \\,-.<<   >>   //   \\_  \\    >>  _// \\_     \\     //   \\_  
     (__)    (__) (__)(__)  (__)\_)-' '-(_/ (_")  (_/(__)__)      (__)__) (__) (__)(_")  (_/(__) (__) (__)  (__)(__)  (__)(__) (__)   (__)   (__)  (__) 
                                                                                                                                            Version 1.0
    '''

    print(hello)
    

def generate(count, length, includeSpecialChar, writeToFile):

    stringList = []
    chars = chars = string.ascii_letters + string.digits + string.ascii_uppercase

    if includeSpecialChar:
        chars = chars + string.punctuation
    
    for x in range(count):
        stringList.append(''.join(choice(chars) for i in range(length)))

    if writeToFile:
        save_results(stringList)
    else:
        for s in stringList:
            print(s)
            print('\n')


def save_results(results):

    thefile = open(create_file_name('StringGenerator'), 'w')

    for r in results:
        thefile.write('{0}\n\n'.format(r))

    thefile.close()

    print('\nYour file has been saved as {0}\n'.format(thefile.name))


def create_file_name(filename, fmt='{filename}_%Y%m%d%H%M%S.txt'):
    return datetime.datetime.now().strftime(fmt).format(filename=filename)


def main():

    parse = argparse.ArgumentParser(description=logo())
    parse.add_argument('--count', action='store', dest='howMany', required=False, help='The number of strings to generate.')
    parse.add_argument('--length', action='store', dest='length', required=True, help='How long should the string be?')
    parse.add_argument('-s', action='store_const', dest='specialChar', const=True, default=False, help='Include special characters in the string.')
    parse.add_argument('-o', action='store_const', dest='output', const=True, default=False, help='Write the results to a file.  The file will be saved in the same location as this script')
    
    args = parse.parse_args()

    # Perform some argument validation
    # ----------------------------------
    isError = False

    count = 0
    length = 0

    if args.howMany is None:
        count = 1
    else:
        try:
            count = int(args.howMany)
        except ValueError:
            print("[!] (--length) Please specify a number for the length.")
            exit(1)
    
    if args.length is None:
        print("[!] (--length) Please specify a number for the length.")
        exit(1)
    
    try:
        length = int(args.length)
    except ValueError:
        print("[!] (--length) Please specify a number for the length.")
        exit(1)
       
    if count < 1:
        print("[!] (--count) Please specify the number of strings to generate.  Must be greater than 0.")
        isError = True
    
    if length < 3:
        print("[!] (--length) Please specify the number of chars in the string.  Must be greater than 2.")
        isError = True
    
    if isError:
        print('\n')
        exit(1)
    
    length = int(args.length)

    # Generate the string(s)
    # ----------------------------------
    generate(count, length, args.specialChar, args.output)

if __name__ == "__main__":
    main()