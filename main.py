
import openpyxl
from dabase import Database
import re



class ReadURLfromfile:

    def __init__(self, file):
        self.file = file
        self.resalt = []

    def read(self):
        i=1
        book = openpyxl.open(self.file, read_only=True)
        sheet = book.active
        for  row in sheet.rows:
            for index, line in enumerate(row):
                if index == 0:
                    yield line.value
        book.close()


class CleanedHttp:

    pattern = re.compile(r'^(([^:/?#]+):)?(//([^/?#]*))?([^?#]*)(\?([^#]*))?(#(.*))?')

    def __init__(self, obj_red_url, comment, db):
        
        self.urls = obj_red_url
        self.url_set = set()
        self.comment = comment
        self.db = db


    def clining(self):
        table = self.db.get_table('site')
        read = self.urls.read()
        url = next(read)
        flag = True
        while flag:
            new_url = self.pattern.search(url)
            if new_url:
                result = new_url.group().split('//')
                if len(result) == 2:
                    result = result[1].strip('/"')
                    self.url_set.add(result)
                    
                    if len(self.url_set) == 100:
                        resual_list = []
                        for url in self.url_set:
                            print(url)
                            resual_list.append(dict(url=url, comment=self.comment))
                        self.db.upsert(table, resual_list)
                        self.url_set.clear()
                        print('значение пустого set', self.url_set)
            
            try:
                url = next(read)
            except:
                flag = False
                resual_list = []
                for url in self.url_set:
                    resual_list.append(dict(url=url, comment=self.comment))
                self.db.upsert(table, resual_list)
                self.db.disconnect()

      

if __name__ == '__main__':
    db = Database()
    db.connect()
    newurl = ReadURLfromfile('/home/timur/urls/jewelry_manufacturers.xlsm') # объект в который считывается содержимое csv
    newurl
    clined_url = CleanedHttp(newurl, comment='ювелирные производители', db=db)
    clined_url.clining()
    #base_ob = WriteBase(clined_url.new_urls, comment = 'интернет магазины')
    #base_ob.write()
    