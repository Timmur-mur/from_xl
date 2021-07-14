import sqlalchemy as sa
from sqlalchemy import MetaData, Table, text, delete
from sqlalchemy.dialects.mysql import insert
from sqlalchemy.engine.base import Connection


class Database:

    def __init__(self):
        self.__engine = sa.create_engine('mysql+pymysql://timur:8T7jJuCzNsXZPpph@localhost:1122/net_source')
        self.__metadata = MetaData(bind=self.__engine)

    def get_table(self, name):
        table = Table(name, self.__metadata, autoload=True)
        return table

    def connect(self):
        self.__conn = self.__engine.connect()
        return self.__conn

    def disconnect(self):
        self.__conn.close()

    def upsert(self, table, values):
        with self.__conn.begin():
            for row in values:
                insert_stmt = insert(table).values(row)
                do_update_stmt = insert_stmt.on_duplicate_key_update(row)
                print(row, 'inserted')
                self.__conn.execute(do_update_stmt)
            print('закончил обновлять')


