# -*- coding: utf-8, utf-8-si, euc-kr -*-

import csv
import platform

class Writer(object):
    def __init__(self, category_name, start_date, end_date):
        self.user_operating_system = str(platform.system())
        self.category_name = category_name
        self.start_date = str(start_date.replace(',',''))
        self.end_date = str(end_date.replace(',',''))
        self.file = None
        self.initialize_file()
        self.wcsv = csv.writer(self.file)

    def initialize_file(self):
        file_name = f"{self.category_name}_{self.start_date}_{self.end_date}.csv"
        if self.user_operating_system == "Windows":
            self.file = open(file_name, 'w', -1, encoding='utf-8-sig', newline='')
        # Other OS uses utf-8
        else:
            self.file = open(file_name, 'w', -1, encoding='utf-8', newline='')

    def get_writer_csv(self):
        return self.wcsv

    def close(self):
        print(f"\r\n [{self.category_name}] 뉴스 저장을 마침니다. \n")
        self.file.close()
