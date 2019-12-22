import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import *
from conectabanco import ConectaBanco
from datetime import date

########################################################################################################################
from inserts import InsertsEmprestimo  # DAVID

data_atual = date.today()  # Hora sem formatação
dataBr = str(data_atual)
dataO = dataBr.split("-")
dataRetirada = dataO[2] + "-" + dataO[1] + "-" + dataO[0]  # Data com formatação atual

dataDevolucao = str(int(dataO[2]) + 7) + "-" + dataO[1] + "-" + dataO[0]  # Data atual + 7 Dias

janela = Tk()
janela.resizable(0, 0)
fonteLbl = ('Verdana', '14', 'bold')
fonteInput = ('Verdana', '14')
fontBtn = ('Arial', '12', 'bold')
null = ""

dataHojeEscolhido = str(data_atual)
dataDevolveEscolhido = dataO[0] + "-" + dataO[1] + "-" + str(int(dataO[2]) + 7)


# David
###########################################################
# David Botoes Funcionais

def btnConsultarCadLivro():
    codLivroCad = edCodLivro.get()
    banco = InsertsEmprestimo()
    sets = ("%s" % (codLivroCad))

    try:
        reg = banco.selectNomeLivro(sets)

        if not reg:
            livroCadSaida["text"] = "Não encontrado!"

        else:
            edCodLivro.insert(0, reg[0])
            livroCadSaida["text"] = edCodLivro.get()
            edCodLivro.delete(0,END)
            edNLivro.insert(0,reg[1])
            print(codLivroCad)

    except:
            livroCadSaida["text"] = "Erro de Conexao"


def btnAcharLivro():  # Buscas
    idlivro = inIdLivro.get()
    banco = ConectaBanco()
    where = (" codigo_livro = '%s';" % idlivro)
    btnCEmprestar["state"] = "disable"
    painelOk.place(x=5500, y=4500)
    try:
        reg = banco.select("*", " tbl_livros", where)
        if not reg:
            livroSaida["text"] = "Não encontrado!"

        else:
            for registro in reg:
                painelOk.place(x=5500, y=4500)
                global idLivroEscolhido  # Essa função serve para que todas Funçoes tenham acesso a Variavel
                inIdLivro.delete(0, END)
                inIdLivro.insert(0, registro[0])
                idLivroEscolhido = inIdLivro.get()  # Pegando esse valor para usar na confirmação
                print(idLivroEscolhido)
                inIdLivro.delete(0, END)  # Para apagar o texto do input, para evitar que o mesmo entre na label
                inIdLivro.insert(0, registro[1])
                livroSaida["text"] = inIdLivro.get()
                inIdLivro.delete(0, END)

    except:
        livroSaida["text"] = "Erro de Conexao"







def btnConfirmarEmprestimo():
    sets = ("'%s','%s','%s','%s'" % (dataHojeEscolhido, dataDevolveEscolhido, idFuncEscolhido, idClienteEscolhido))

    btnCEmprestar["state"] = "disable"
    insertar = InsertsEmprestimo()
    banco = ConectaBanco()

    try:
        insertar.insertEmprestimo(sets)
        reg = banco.select("max(cod_emprestimo)", " tbl_emprestimo;")
        # insertar.insertLivroEmprestimo(idEmprestimo, idLivroEscolhido)

        if not insertar:  # Se não existe o registro
            print("Deu errado")
        else:  # Se existe o registro
            print("Funcionou")
            global idEmprestimo
            inBibliotecario.insert(0, reg[0])
            idEmprestimo = inBibliotecario.get()  # Pegando o ultimo ID inserido
            inBibliotecario.delete(0, END)
            print(idEmprestimo)
            setsLivroEmprestimo = ("%s,%s") % (idLivroEscolhido, idEmprestimo)
            insertar.insertLivroEmprestimo(setsLivroEmprestimo)
            codigo_EmprestimoSaida["text"] = idEmprestimo
            painelOk.place(x=550, y=450)

    except:
        dataDevoSaida["text"] = "Erro na Conexao!"


def btnLiberarEmprestimo():
    if livroSaida["text"] != "Não encontrado!" and livroSaida["text"] != "Erro de Conexao" and livroSaida[
        "text"] != null \
            and nomeSaida["text"] != "Não encontrado!" and nomeSaida["text"] != "Erro de Conexao" and nomeSaida[
        "text"] != null \
            and lblBibliotecarioSaida["text"] != "Não encontrado!" and lblBibliotecarioSaida[
        "text"] != "Erro de Conexao":
        btnCEmprestar["state"] = "normal"
        dataAtualSaida["text"] = dataRetirada
        dataDevoSaida["text"] = dataDevolucao
        painelOk.place(x=5500, y=4500)


def btnAcharFunc():  # Buscas
    idfunc = inBibliotecario.get()
    banco = ConectaBanco()
    where = (" codigo_bibliotecario = '%s';" % idfunc)
    btnCEmprestar["state"] = "disable"
    painelOk.place(x=5500, y=4500)

    try:
        reg = banco.select("*", " tbl_bibliotecario", where)
        if not reg:
            lblBibliotecarioSaida["text"] = "Não encontrado!"

        else:
            for registro in reg:
                global idFuncEscolhido  # Essa função serve para que todas Funçoes tenham acesso a Variavel
                idFuncEscolhido = inBibliotecario.get()
                print(idFuncEscolhido)
                inBibliotecario.delete(0, END)  # Para apagar o texto do input, para evitar que o mesmo entre na label
                inBibliotecario.insert(0, registro[1])
                lblBibliotecarioSaida["text"] = inBibliotecario.get()
                inBibliotecario.delete(0, END)

    except:
        lblBibliotecarioSaida["text"] = "Erro de Conexao"


def btnAcharNome():  # Buscas
    cpf = inCPF.get()
    banco = ConectaBanco()
    where = ("cpf = '%s'" % cpf)
    btnCEmprestar["state"] = "disable"
    painelOk.place(x=5500, y=4500)

    try:
        reg = banco.select("*", "tbl_cliente", where)
        if not reg:
            nomeSaida["text"] = "Não encontrado!"
        else:
            painelOk.place(x=5500, y=4500)
            for registro in reg:
                global idClienteEscolhido  # Essa função serve para que todas Funçoes tenham acesso a Variavel
                inCPF.delete(0, END)
                inCPF.insert(0, registro[0])
                idClienteEscolhido = inCPF.get()  # Pegando id correspondente a o CPF
                print(idClienteEscolhido)
                inCPF.delete(0, END)  # Para apagar o texto do input, para evitar que o mesmo entre na label
                inCPF.insert(0, registro[1])
                nomeSaida["text"] = inCPF.get()
                inCPF.delete(0, END)
    except:
        nomeSaida["text"] = "Erro de Conexao"


def btnAcharLivro():  # Buscas
    idlivro = inIdLivro.get()
    banco = ConectaBanco()
    where = (" codigo_livro = '%s';" % idlivro)
    btnCEmprestar["state"] = "disable"
    painelOk.place(x=5500, y=4500)
    try:
        reg = banco.select("*", " tbl_livros", where)
        if not reg:
            livroSaida["text"] = "Não encontrado!"

        else:
            for registro in reg:
                painelOk.place(x=5500, y=4500)
                global idLivroEscolhido  # Essa função serve para que todas Funçoes tenham acesso a Variavel
                inIdLivro.delete(0, END)
                inIdLivro.insert(0, registro[0])
                idLivroEscolhido = inIdLivro.get()  # Pegando esse valor para usar na confirmação
                print(idLivroEscolhido)
                inIdLivro.delete(0, END)  # Para apagar o texto do input, para evitar que o mesmo entre na label
                inIdLivro.insert(0, registro[1])
                livroSaida["text"] = inIdLivro.get()
                inIdLivro.delete(0, END)

    except:
        livroSaida["text"] = "Erro de Conexao"
        # DAVID


########################################################################################################################
# BREHMER FUNCÇOES
def btnSalvarCliente():  # Salvar dados
    cpf = inputCPF.get()
    nome = inNome.get()
    email = inEmail.get()
    tel = inTel.get()
    nasc = inNasc.get()
    banco = ConectaBanco()
    valores = ("'%s','%s','%s','%s', '%s'" % (cpf, nome, email, tel, nasc))
    sets = ("nome='%s',email='%s',telefone ='%s', nasc='%s'" % (nome, email, tel, nasc))
    where = ("cpf = '%s'" % cpf)
    try:
        reg = banco.select("*", "tbl_cliente", where)
        if not reg:  # Se não existe o registro
            banco.insert("tbl_cliente", valores)
            lbMensagem["text"] = "Cadastrado com sucesso!"
        else:  # Se existe o registro
            banco.update("tbl_cliente", sets, where)
            lbMensagem["text"] = "Registro atualizado!"
    except:
        lbMensagem["text"] = "Erro no BD, notifique o ADM!"


def btnAchar():  # PESQUISAR
    inNome['state'] = "normal"
    inTel['state'] = "normal"
    inEmail['state'] = "normal"
    inNasc['state'] = "normal"
    btnSalvarCliente['state'] = "normal"

    inNome.delete(0, END)
    inEmail.delete(0, END)
    inTel.delete(0, END)
    inNasc.delete(0, END)
    cpf = inputCPF.get()

    banco = ConectaBanco()
    where = ("cpf = '%s'" % cpf)

    try:
        reg = banco.select("*", "tbl_cliente", where)
        if not reg:
            lbMensagem["text"] = "Registro não encontrado!"
        else:
            lbMensagem["text"] = "Registro encontrado!"
            for registro in reg:
                inNome.insert(0, registro[1])
                inEmail.insert(0, registro[4])
                inTel.insert(0, registro[5])
                inNasc.insert(0, registro[3])
    except:
        lbMensagem["text"] = "Erro no BD, notifique o ADM!"


########################################################################################################################
# Funcao para consultar cadastro
# Função para fechar a janela


def btConsult():
    cod_livro = edCodLivro.get()
    nome_livro = edNLivro.get()
    genero = edGenLivro.get()
    autor = edAutor.get()
    editora = edEditora.get()
    banco = ConectaBanco()
    valores = ("'%s','%s','%s','%s','%s'" % (cod_livro, nome_livro, genero, autor, editora))
    try:
        banco.select("livros", valores)
    except:
        messagebox.ERROR('Falha', 'Não possivel localizar o cadastro')
    else:
        messagebox.showinfo("cadastro localizado!")


# Função do bt confirma(Cadastrar)
def btSalvar():
    cod_livro = edCodLivro.get()

    nome_livro = edNLivro.get()
    genero = edGenLivro.get()
    autor = edAutor.get()
    editora = edEditora.get()

    banco = ConectaBanco()
    valores = ("'%s','%s','%s','%s','%s'" % (cod_livro, nome_livro, genero, autor, editora))
    try:
        banco.insert("livros", valores)
    except:
        messagebox.showinfo('Sucesso', 'Cadastro Efetuado com Sucesso!!!!')

    else:
        messagebox.showerror('Falha', 'Não foi possivel cadastrar!')


# Defininto tipo padrão de fonte
fonte = ('Arial', '16', 'bold')  # Define o padrão de fonte

# Criando as Abas

guias = ttk.Notebook(janela, width=480, height=290)

frame_CadastroLivro = Frame(guias)
frame_CadastroFuncionario = Frame(guias)
frame_Emprestimo = Frame(guias)
frame_CadastroCliente = Frame(guias)
frame_ConsultarEmprestimos = Frame(guias)

# Criando As Guias
guias.add(frame_CadastroLivro, text="Buscar/Cadastrar Livro*")
guias.add(frame_CadastroFuncionario, text="Busca Funcionário*")
guias.add(frame_CadastroCliente, text="Cadastrar e Consultar Clientes")
guias.add(frame_Emprestimo, text="Emprestar")
guias.add(frame_ConsultarEmprestimos, text="Clientes e Livros Emprestados")

guias.pack(fill=BOTH, expand=1)
######################################################################################################################
# David
# Paineis
# Tela de Consulta
telaConsulta = Frame(frame_Emprestimo, bd=2, pady=10, padx=10)
telaConsulta.place(x=50, y=10)
#
painelOk = Frame(frame_Emprestimo, bd=2, pady=10, padx=10)
painelOk.place(x=5500, y=4500)
imgOk = PhotoImage(file="img/ok.png")
imgOk = imgOk.subsample(10, 10)
btnOk = Button(painelOk, image=imgOk, bd=0, state="disabled")
btnOk.grid(row=0, column=0)

# Tela de Verifica
telaVerifica = Frame(frame_Emprestimo, bd=2, pady=10, padx=10)
telaVerifica.place(x=50, y=160)

# Painel de Data
painelData = Frame(frame_Emprestimo, bd=2, pady=10, padx=10)
painelData.place(x=40, y=360)

# Botoes
btnConsultarCpf = Button(telaConsulta, font=fontBtn, text="Consultar", fg="black",  # Consultar CPF
                         activebackground="#A9A9A9", activeforeground="blue", command=btnAcharNome)

btnConsultarLivro = Button(telaConsulta, font=fontBtn, text="Consultar", fg="black",  # Consultar livro
                           activebackground="#A9A9A9", activeforeground="blue", command=btnAcharLivro)

btnConsultarBiblio = Button(telaConsulta, font=fontBtn, text="Consultar", fg="black",  # Consultar Funcionario
                            activebackground="#A9A9A9", activeforeground="blue", command=btnAcharFunc)

btnEmprestar = Button(telaVerifica, font=fontBtn, text="Emprestar Livro", fg="Blue",  # Validar campos
                      activebackground="#A9A9A9", activeforeground="blue", command=btnLiberarEmprestimo)

btnCEmprestar = Button(painelData, font=fontBtn, text="Confirmar Emprestimo", fg="Green",  # Confirmar transação
                       activebackground="#A9A9A9", activeforeground="Green", state="disabled",
                       command=btnConfirmarEmprestimo)
# David
#######################################################################################################################

# Criando Label da Busca Livro
lbCodLivro = Label(frame_CadastroLivro, text="Código Livro:", font=fonte, pady=10)
btnConsultarLivroCadastro = Button(frame_CadastroLivro, text="Consultar Livro", font=fontBtn, command=btnConsultarCadLivro)

lbNLivro = Label(frame_CadastroLivro, text="Nome Livro:", font=fonte, pady=10, padx=10)
lbGenLivro = Label(frame_CadastroLivro, text="Genero:", font=fonte, pady=10, padx=10)
lbAutor = Label(frame_CadastroLivro, text="Autor:", font=fonte, pady=10, padx=10)
lbEditora = Label(frame_CadastroLivro, text="Editora:", font=fonte, pady=10, padx=10)

# Criando Ed
edCodLivro = Entry(frame_CadastroLivro, font=fonte, width=15)
edNLivro = Entry(frame_CadastroLivro, font=fonte, width=15, state="disabled")
edGenLivro = Entry(frame_CadastroLivro, font=fonte, width=15)
edAutor = Entry(frame_CadastroLivro, font=fonte, width=15, state="disabled")
edEditora = Entry(frame_CadastroLivro, font=fonte, width=15, state="disabled")
livroCadSaida = Label(frame_CadastroLivro, text="Resultados", font=fonte, pady=10, padx=10)

# Botoes da consulta Livro
btSalvar = Button(frame_CadastroLivro, font=fontBtn, text="Salvar livro", fg="Blue",
                  activebackground="#A9A9A9", activeforeground="white", command=btSalvar, state="disabled")

####################################################################################################################
# David
# Campos de Label e ENTRADA DE DADOS
# e suas localizações
# Entrada de TEXTO
inCPF = Entry(telaConsulta, width=15, font=fonteInput)
inIdLivro = Entry(telaConsulta, width=15, font=fonteInput)
inBibliotecario = Entry(telaConsulta, width=15, font=fonteInput, show="*")

# Labels CPF e ID livro
cpfText = Label(telaConsulta, text="Cpf do Cliente:", font=fonteLbl, pady=10, padx=7)
idLivroText = Label(telaConsulta, text="ID do Livro:", font=fonteLbl, pady=10, padx=7)
inBibliotecarioText = Label(telaConsulta, text="ID Biblio..", font=fonteLbl, pady=10, padx=7)

# Label Resultados
cpfTextNome = Label(telaVerifica, text="Nome Cliente:", font=fonteLbl, pady=10, padx=7)
idLivroTextNome = Label(telaVerifica, text="Nome do Livro:", font=fonteLbl, pady=10, padx=7)
lblBibliotecario = Label(telaVerifica, text="Nome funcionario:", font=fonteLbl, pady=5, padx=7)

# Label de Saida de Dados
nomeSaida = Label(telaVerifica, text="", font=fonteLbl, pady=10, padx=7)
livroSaida = Label(telaVerifica, text="", font=fonteLbl, pady=10, padx=7)
lblBibliotecarioSaida = Label(telaVerifica, text="", font=fonteLbl, pady=10, padx=7)

# Label de data
lblDataAtual = Label(painelData, text="Data da Retirada:", font=fonteLbl, pady=5, padx=7)
lblDataDevol = Label(painelData, text="Data da Entrega:", font=fonteLbl, pady=5, padx=7)
dataAtualSaida = Label(painelData, text="", font=fonteLbl, pady=5, padx=7)
dataDevoSaida = Label(painelData, text="", font=fonteLbl, pady=5, padx=7)
codigo_Emprestimo = Label(painelData, text="Código Emprestimo:", font=fonteLbl, pady=5, padx=7)
codigo_EmprestimoSaida = Label(painelData, text="", font=fonteLbl, pady=5, padx=7)  # Codigo emprestimo Saida
# David
#####################################################################################################################

# Exibindo campos do formulario Consulta Livro

lbCodLivro.grid(row=5, column=0)
lbNLivro.grid(row=6, column=0)
lbGenLivro.grid(row=7, column=0)
lbAutor.grid(row=8, column=0)
lbEditora.grid(row=9, column=0)

edCodLivro.grid(row=5, column=1)
btnConsultarLivroCadastro.grid(row=5, column=2)
edNLivro.grid(row=6, column=1)

edAutor.grid(row=8, column=1)
edEditora.grid(row=9, column=1)

btSalvar.grid(row=10, column=2, )
livroCadSaida.grid(row=11, column=0)
comboExample = ttk.Combobox(frame_CadastroLivro, width=26)
comboExample['values'] = ["Aventura", "AutoAjuda", "Cientificos", "Contos", "Cronicas",
"Didaticos", "fantasia", "Ficção", "Horror", "Juvenil", "Ação", "Drama", "Jogos", "Poesia", "Politica","Romance"]
print(dict(comboExample))
comboExample.grid(row=7, column=1)
comboExample.current(0)

# Tela Consulta Funcionario

lbNome = Label(frame_CadastroFuncionario, text="Nome:", font=fonte, pady=10, padx=10)
lbCpf = Label(frame_CadastroFuncionario, text="CPF:", font=fonte, pady=10, padx=10, fg="red")
lbDtnascimento = Label(frame_CadastroFuncionario, text="Data Nascimento:", font=fonte, pady=10, padx=10)
lbCel = Label(frame_CadastroFuncionario, text="Celular:", font=fonte, pady=10, padx=10)

# Campos  Consulta Funcionario
edNome = Entry(frame_CadastroFuncionario, font=fonte, width=15)
edCpf = Entry(frame_CadastroFuncionario, font=fonte, width=15)
edDtnascimento = Entry(frame_CadastroFuncionario, font=fonte, width=15)
edCel = Entry(frame_CadastroFuncionario, font=fonte, width=15)

# Botões Consulta Funcionario
btSalvar = Button(frame_CadastroFuncionario, font=fonte, text="Salvar", fg="Blue",
                  activebackground="#A9A9A9", activeforeground="white", command=btSalvar, state="disabled")

btPesquisar = Button(frame_CadastroFuncionario, font=15, text="Buscar", fg="Black",
                     activebackground="#A9A9A9", activeforeground="white", command=btConsult)

####################################################################################################################
# BREHMER LABELS
# Formulário
lbCPF = Label(frame_CadastroCliente, text="CPF:", font=fonte, pady=10, padx=10)
labelNome = Label(frame_CadastroCliente, text="Nome:", font=fonte, pady=10, padx=10)
lbEmail = Label(frame_CadastroCliente, text="E-mail:", font=fonte, pady=10, padx=10)
lbTel = Label(frame_CadastroCliente, text="Telefone:", font=fonte, pady=10, padx=10)
lbNasc = Label(frame_CadastroCliente, text="Data de nascimento:", font=fonte, pady=10, padx=10)

# Inserçao de dados
inputCPF = Entry(frame_CadastroCliente, font=fonte, width=25)
inNome = Entry(frame_CadastroCliente, font=fonte, width=25, state="disabled")
inEmail = Entry(frame_CadastroCliente, font=fonte, width=25, state="disabled")
inTel = Entry(frame_CadastroCliente, font=fonte, width=25, state="disabled")
inNasc = Entry(frame_CadastroCliente, font=fonte, width=25, state="disabled")
btnSalvarCliente = Button(frame_CadastroCliente, font=fonte, text="Salvar", fg="Blue", state="disabled",
                          activebackground="#A9A9A9", activeforeground="white", command=btnSalvarCliente)

# Colocando no Grip
lbCPF.grid(row=0, column=0)
labelNome.grid(row=1, column=0)
lbEmail.grid(row=2, column=0)
lbTel.grid(row=3, column=0)
lbNasc.grid(row=4, column=0)
inputCPF.grid(row=0, column=1)
inNome.grid(row=1, column=1)
inEmail.grid(row=2, column=1)
inTel.grid(row=3, column=1)
inNasc.grid(row=4, column=1)
btnSalvarCliente.grid(row=5, column=1, columnspan=3)

# criando o botão de Pesquisar
photoLupa = PhotoImage(file="img/lupa2.png")
logoLupa = photoLupa.subsample(15, 15)
btBusca = Button(frame_CadastroCliente, image=logoLupa, bd=0, command=btnAchar)
btBusca.grid(row=0, column=3)

# criando o botão Fechar

lbMensagem = Label(frame_CadastroCliente, text="", font=fonte)
lbMensagem.place(x=20, y=280)

####################################################################################################################
# David
# Painel de Consulta
cpfText.grid(row=0, column=1)  # Label do CPF
inCPF.grid(row=0, column=2)  # Entrada de Dados
idLivroText.grid(row=1, column=1)  # Label do ID livro
inIdLivro.grid(row=1, column=2)  # Entrada de Dados
inBibliotecarioText.grid(row=2, column=1)  # Label Bibliotecario
inBibliotecario.grid(row=2, column=2)  # Entrada de dados

btnConsultarCpf.grid(row=0, column=3, columnspan=23)  # Botão consultar
btnConsultarLivro.grid(row=1, column=3)  # Botão consultar
btnConsultarBiblio.grid(row=2, column=3)  # Consultar Funcionario

# Painel de Saida de Pesquisa
cpfTextNome.grid(row=3, column=1)  # Label de Saida de dados
idLivroTextNome.grid(row=4, column=1)  # Label de Saida de dados
nomeSaida.grid(row=3, column=2, columnspan=30)  # Saida dos Nomes
livroSaida.grid(row=4, column=2, columnspan=30)  # Saida dos Nomes
lblBibliotecario.grid(row=5, column=1)
lblBibliotecarioSaida.grid(row=5, column=2, columnspan=45)

# Botoes de Emprestimos
btnEmprestar.grid(row=6, column=2)  # Botao Emprestar

lblDataAtual.grid(row=0, column=2)  # Label Data Saida
lblDataDevol.grid(row=1, column=2)  # Label Data Devolução
dataAtualSaida.grid(row=0, column=3)
dataDevoSaida.grid(row=1, column=3)  # Data da Devolução saida
btnCEmprestar.grid(row=2, column=2)  # Botao Confirmar emprestimo
codigo_Emprestimo.grid(row=3, column=2)  # Codigo emprestimo
codigo_EmprestimoSaida.grid(row=3, column=3)

####################################################################################################################
# Exibindo os componentes do formulario  Consulta Funcionario
lbNome.grid(row=1, column=0)
lbCpf.grid(row=0, column=0)
lbDtnascimento.grid(row=3, column=0)
lbCel.grid(row=6, column=0)

edNome.grid(row=1, column=1)
edCpf.grid(row=0, column=1)
edDtnascimento.grid(row=3, column=1)
edCel.grid(row=6, column=1)

btPesquisar.grid(row=0, column=3, columnspan=4)


####################################################################################################################
def btnConsultarLivro():
    # Pegando os campos do Entry para fazer Verificação
    idNomeLivro = inConsultarText.get()
    insertar = InsertsEmprestimo()
    setsConsultarLivro = ("%s" % (idNomeLivro))
    print(idNomeLivro)

    try:
        livroEscolhido = insertar.selectNomeLivroEmprestado(setsConsultarLivro)

        if not insertar:  # Se não existe o registro
            print(livroEscolhido)
            print("Deu errado")
        else:  # Se existe o registro
            inConsultarText.delete(0, END)
            inConsultarText.insert(0, livroEscolhido[0])
            nomeLivroSaida["text"] = inConsultarText.get()
            inConsultarText.delete(0, END)
            print("Funcionou")

    except:
        nomeLivroSaida["text"] = "Erro na Conexao!"

    # ABA CONSULTA EMPRESTIMOS DE LIVROS


telaVericaLivros = Frame(frame_ConsultarEmprestimos, bd=2, pady=10, padx=10)
telaVericaLivros.place(x=10, y=20)
btnConsultarLivroEmprestado = Button(telaVericaLivros, font=fontBtn, text="Confirmar", fg="Green",
                                     # Confirmar transação
                                     activebackground="#A9A9A9", activeforeground="Green", command=btnConsultarLivro)

consultarText = Label(telaVericaLivros, text="Codigo Emprestimo:", font=fonteLbl, pady=10, padx=7)
inConsultarText = Entry(telaVericaLivros, width=15, font=fonteInput)
lblNomeLivro = Label(telaVericaLivros, text="Nome Livro:", font=fonteLbl, pady=10, padx=7)
nomeLivroSaida = Label(telaVericaLivros, text="", font=fonteLbl, pady=10, padx=7)

consultarText.grid(row=0, column=0)
inConsultarText.grid(row=0, column=1)
btnConsultarLivroEmprestado.grid(row=0, column=2)

lblNomeLivro.grid(row=1, column=0)
nomeLivroSaida.grid(row=1, column=1, columnspan=15)  # Nome Livro escolhido pela consulta

####################################################################################################################

# Configurações da janela principal
janela.geometry("800x600+500+50")  # Larg x Alt + DistaciaEsq + DistandiaTop
janela.title("Biblioteca")  # Define o titulo da janela
janela.iconbitmap("img/icone.ico")
janela.mainloop()  # Exibe a janela


