from flask_mysqldb import MySQL


class Database():

    def initializeDatabase(self, app):
        app.config['MYSQL_HOST'] = 'localhost'
        app.config['MYSQL_USER'] = 'root'
        app.config['MYSQL_PASSWORD'] = 'wewwew123'
        app.config['MYSQL_DB'] = 'Bismuth_Database'
        app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
        mysql = MySQL(app) 
        return mysql

    def save(self,Object,tableName, cur):
        objectKeys = self.removeTokens(['_',']','[',"'"], list(Object.__dict__.keys()))
        objectValues = self.removeTokens([']','['], list(Object.__dict__.values()))
        cur.execute('''INSERT INTO {table} ({keys}) VALUES ({values});'''.format(keys = objectKeys, values = objectValues , table = tableName))
        cur.connection.commit()

    def removeTokens(self, token, theString): 
        for i in token : theString = str(theString[0:len(theString)]).replace(i, '')
        return theString

    def get(self, keys,tableName, condition, cur): 
        cur.execute('''SELECT {columns} FROM {tableName} WHERE {condition};'''.format(columns = keys, tableName = tableName, condition = condition))
        rv = cur.fetchall()
        return rv



