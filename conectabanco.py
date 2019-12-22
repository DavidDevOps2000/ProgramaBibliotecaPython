import MySQLdb


class ConectaBanco:
    def __init__(self):
        self.con = ""

    def conecta(self):
        host = "localhost"
        user = "ProjetoFinal"
        password = "123456"
        db = "db_biblioteca"
        port = 3306
        self.con = MySQLdb.connect(host, user, password, db, port)

    def select(self, campos, tabelas, where=None):
        self.conecta()
        cur = self.con.cursor()
        query = ("SELECT " + campos + " FROM " + tabelas)
        if where:
            query = (query + " WHERE " + where)
        print(query)
        cur.execute(query)
        result = cur.fetchall()
        self.con.close()
        return result

    def insert(self, tabela, valores, campos=None):
        self.conecta()
        cur = self.con.cursor()
        query = ("INSERT INTO " + tabela)
        if campos:
            query = (query + "(" + campos + ")")
        query = (query + " VALUES(" + valores + ")")
        print(query)
        cur.execute(query)
        self.con.commit()
        self.con.close()

    def update(self, tabela, sets, where=None):
        self.conecta()
        cur = self.con.cursor()
        query = ("UPDATE " + tabela + " SET " + sets)
        if where:
            query = (query + " WHERE " + where)
        print(query)
        cur.execute(query)
        self.con.commit()
        self.con.close()

    def delete(self, tabela, where):
        self.conecta()
        cur = self.con.cursor()
        query = ("DELETE FROM " + tabela + " WHERE " + where)
        print(query)
        cur.execute(query)
        self.con.commit()
        self.con.close()
