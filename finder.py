__author__ = 'thiago.candido'
import os
import concurrent.futures
from hashlib import sha256


class Finder:
    def __init__(self, path, file_type, max_threads):
        self.__root_path = path
        self.__max_threads = max_threads
        self.__file_type = file_type
        self.__files_read = 0
        self.__total_files = 0
        self.__file_hashmap = {}

    def __initialize(self):
        count = 0
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.__max_threads) as executor:
            for (directory_path, child_directories, files) in os.walk(self.__root_path):
                executor.submit(self.__count_files, files)

    def __count_files(self, files):
        for file in files:
            if file.lower().endswith(self.__file_type):
                self.__total_files += 1

    def process_tree(self):
        self.__initialize()
        if self.__total_files > 0:
            with concurrent.futures.ThreadPoolExecutor(max_workers=self.__max_threads) as executor:
                for (directory_path, child_directories, files) in os.walk(self.__root_path):
                    executor.submit(self.__process_folder, directory_path, files)
        else:
            print('\rno files were found with ' + self.__file_type + ' extension')


    def __process_folder(self, directory_path, files):
        for filename in files:
            file_path = os.path.join(directory_path, filename)
            if os.path.isfile(file_path) and file_path.lower().endswith(self.__file_type):
                hash = sha256(open(file_path, 'rb').read()).hexdigest()
                if (hash not in self.__file_hashmap):
                    self.__file_hashmap[hash] = [file_path]
                else:
                    self.__file_hashmap[hash].append(file_path)
                self.__files_read += 1
                self.__log()

    def get_duplicated_files(self):
        duplicated_files = {}
        for key in self.__file_hashmap:
            files = self.__file_hashmap[key]
            if len(files) > 1:
                duplicated_files[key] = self.__file_hashmap[key]
        return duplicated_files

    def __log(self):
        msg = '\r%d of %d files hashed' % (self.__files_read, self.__total_files)
        print(msg, end='')
