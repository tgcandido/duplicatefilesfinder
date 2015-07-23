__author__ = 'thiago.candido'
import sys
import timeit
from json import dumps
from os import path
from finder import Finder


def main():
    if len(sys.argv) < 3:
        print ('please tell me the root folder, the file extension and the maximum number of threads that I can use. default number of threads is 2')
        return

    root_folder = sys.argv[1]
    file_type = sys.argv[2].lower()

    if len(sys.argv) == 4:
        max_threads = int(sys.argv[3])
    else:
        max_threads = 2

    start = timeit.default_timer()
    duplicated_files = find_duplicates(root_folder, file_type, max_threads)
    print ('\n%.2f seconds' % round(timeit.default_timer() - start, 2))

    if (len(duplicated_files) > 0):
        print_duplicates_to_file(duplicated_files, root_folder, file_type)
    else:
        print ('hurr durr - I haven\'t found duplicated files.')


def print_duplicates_to_file(duplicates, file_name, file_type):
    outputpath = path.join(file_name, 'duplicated-' + file_type.replace('.', '') + '-files.json')
    with open(outputpath, 'w')as outputfile:
        outputfile.write(dumps(duplicates, indent=4, sort_keys=True))

    print ('the ones I\'ve found are in : %s \n\nSee ya' % outputpath)


def find_duplicates(path, file_type, max_threads):
    finder = Finder(path, file_type, max_threads)
    finder.process_tree()
    return finder.get_duplicated_files()


if __name__ == "__main__":
    main()