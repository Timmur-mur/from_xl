
import openpyxl
from dabase import session, Urls

class ReadURLfromfile:

    def __init__(self, file):
        self.file = file
        self.resalt = []

    def read(self):
        i=1
        book = openpyxl.open(self.file, read_only=True)
        sheet = book.active
        for row in range(2, sheet.max_row): #
            url = sheet[row][0].value
            yield url
        book.close()


class CleanedHttp:

    def __init__(self, obj_red_url):
        
        self.urls = obj_red_url
        self.url_set = set()

    def clining(self):
        read = self.urls.read()
        url = next(read)
        flag = True
        while flag:
            
            self.url_set.add(url.split('//')[1].strip('/"'))
            if len(self.url_set) == 100:
                base = WriteBase(self.url_set, 'internet shops')
                base.write() 
                self.url_set.clear()
            try:
                url = next(read)
            except:
                flag = False      
        print(self.url_set)






class WriteBase:

    def __init__(self, urls, comment):
        self.urls = urls
        self.comment = comment

    def write(self):
        for url in self.urls:
            url_new = Urls(url=url, comment=self.comment)
            session.add(url_new)
            try:
                session.commit()
                print('записали: ', url)
            except:
                session.rollback()
                continue
        session.close()
 
                #print('тут вставить код для записи транзакции в базу',tr_url)
           



# надо дописать код работы с алхимией, что бы можно было с ней использовать транзакцию


if __name__ == '__main__':
    newurl = ReadURLfromfile('/home/timur/urls/allonlineshopsfree.xlsx') # объект в который считывается содержимое csv
    newurl
    clined_url = CleanedHttp(newurl)
    clined_url.clining()
    #base_ob = WriteBase(clined_url.new_urls, comment = 'интернет магазины')
    #base_ob.write()
    