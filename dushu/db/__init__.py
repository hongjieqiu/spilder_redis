import pymssql
class Database():
    def __init__(self):
        self.conn = pymssql.connect(
            host=".",
            user="sa",
            password="780910",
            database="ttt",
            charset='utf8'
        )
    def __enter__(self):
        return self.conn.cursor()
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.conn.rollback()
        else:
            self.conn.commit()
        return True
class BaseDao():
    def __init__(self):
        self.db =Database()
    def save(self,table_name,**item):
        sql = 'insert into %s(%s) values(%s)'
        fields = ','.join(item.keys())
        field_placeholds = ','.join(['%%(%s)s' % key for key in item])
        with self.db as cursor:
            cursor.execute(sql % (table_name, fields, field_placeholds), item)
            # 判断是否执行成功
            if cursor.rowcount > 0:
                return True
        return False
