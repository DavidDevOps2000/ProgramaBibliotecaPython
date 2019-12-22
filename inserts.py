import MySQLdb


class InsertsEmprestimo:
    def __init__(self):
        self.con = ""

    def conecta(self):
        host = "localhost"
        user = "ProjetoFinal"
        password = "123456"
        db = "db_biblioteca"
        port = 3306
        self.con = MySQLdb.connect(host, user, password, db, port)

    def insertEmprestimo(self, setEmprestimo): #Inserindo dados na tabela tbl_emprestimo
        self.conecta()
        cur = self.con.cursor()
        query = "INSERT INTO tbl_Emprestimo (retirada, devolucao, FK_Bibliotecario," \
                " FK_Cliente) VALUES("'%s'")" %(setEmprestimo)
        print(query)
        cur.execute(query)
        self.con.commit()
        self.con.close()

    def insertLivroEmprestimo(self, setsLivroEmprestimo): #Inserindo dados na tabela tbl_emprestimo
        self.conecta()
        cur = self.con.cursor()
        query = "INSERT INTO Livro_Emprestimo(fk_livro, fk_emprestimo)" \
                " VALUES("'%s'");" %(setsLivroEmprestimo)
        print(query)
        cur.execute(query)
        self.con.commit()
        self.con.close()

    def selectTblEmprestimo(self):#Selecionando o registro mais atual para usar nos futuros inserts
        self.conecta()
        cur = self.con.cursor()
        query = "select max(cod_emprestimo) from tbl_emprestimo;"
        print(query)
        cur.execute(query)
        result = cur.fetchall()
        self.con.close()
        return result

    def selectNomeLivroEmprestado(self, setNomeLivroEmprestado):
        self.conecta()
        cur = self.con.cursor()
        query = "select nome_livro from tbl_livros join Livro_Emprestimo on livro_emprestimo.fk_" \
                "livro = tbl_livros.codigo_livro where fk_emprestimo='%s';" % (setNomeLivroEmprestado)
        print(query)
        cur.execute(query)
        result = cur.fetchall()
        self.con.close()
        return result

    # def selectNomeLivro(self, setNomeLivro):
    #     self.conecta()
    #     cur = self.con.cursor()
    #     query = "select * from tbl_livros where codigo_livro = '%s';" % (setNomeLivro)
    #     print(query)
    #     cur.execute(query)
    #     result = cur.fetchall()
    #     self.con.close()
    #     return result