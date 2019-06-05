import sys, os


def joinfile(fromdir, filename, todir):
    if not os.path.exists(todir):
        os.mkdir(todir)
    if not os.path.exists(fromdir):
        print('Wrong directory')
    outfile = open(os.path.join(todir, filename), 'wb')
    files = os.listdir(fromdir)  # list all the part files in the directory
    files.sort()  # sort part files to read in order
    for file in files:
        filepath = os.path.join(fromdir, file)
        infile = open(filepath, 'rb')
        data = infile.read()
        outfile.write(data)
        infile.close()
    outfile.close()


if __name__ == '__main__':
    fromdir = input('Directory containing part files?')
    filename = input('Name of file to be recreated?')
    todir = input('Directory to store recreated file?')

    try:
        joinfile(fromdir, filename, todir)
    except:
        print('Error joining files:')
        print(sys.exc_info()[0], sys.exc_info()[1])