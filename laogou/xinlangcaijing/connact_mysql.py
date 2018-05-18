import pymysql

class Mydb:
    def __init__(self):
        try:
            self.conn = pymysql.connect('127.0.0.1','root','123456','luxinwang',charset='utf8')
            self.cursor = self.conn.cursor()
        except Exception as e:
            print(e)

    def execute(self,sql,data=None):
        try:
            if data:
                self.cursor.execute(sql,data)
            else:
                self.cursor.execute(sql)
            self.conn.commit()

        except Exception as e:
            print('执行增删改失败')
            print(e)
            self.conn.rollback()

    def query(self,sql):
        self.cursor.execute(sql)
        res = self.cursor.fetchall()
        return res

    def close(self):
        self.cursor.close()
        self.conn.close()

