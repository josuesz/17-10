import sqlite3
from tkinter import *
from tkinter import messagebox, ttk

# Funções para o banco de dados
def conectar():
    conn = sqlite3.connect('n1ficha.db')
    return conn

def criar_tabela():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Clientes (
            cod_Clientes INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            numero TEXT,
            endereco TEXT
        )
    ''')
    conn.commit()
    cursor.close()
    conn.close()

def incluir_cliente(nome, numero, endereco):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Clientes (nome, numero, endereco) VALUES (?, ?, ?)", (nome, numero, endereco))
    conn.commit()
    cursor.close()
    conn.close()

def consultar_clientes():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Clientes")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

def excluir_cliente(cod_cliente):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Clientes WHERE cod_Clientes = ?", (cod_cliente,))
    conn.commit()
    cursor.close()
    conn.close()

def limpar_campos():
    entry_nome.delete(0, END)
    entry_numero.delete(0, END)
    entry_endereco.delete(0, END)

# Funções de interface
def incluir():
    nome = entry_nome.get()
    numero = entry_numero.get()
    endereco = entry_endereco.get()
    incluir_cliente(nome, numero, endereco)
    messagebox.showinfo("Sucesso", "Cliente incluído com sucesso!")
    limpar_campos()

def consultar():
    for row in tree.get_children():
        tree.delete(row)
    for cliente in consultar_clientes():
        tree.insert("", END, values=cliente)

def excluir():
    selected_item = tree.selection()
    if selected_item:
        cod_cliente = tree.item(selected_item)['values'][0]
        excluir_cliente(cod_cliente)
        messagebox.showinfo("Sucesso", "Cliente excluído com sucesso!")
        consultar()  # Atualiza a lista
    else:
        messagebox.showwarning("Selecione", "Selecione um cliente para excluir.")

# Criação da tabela ao iniciar
criar_tabela()

# Interface Gráfica
root = Tk()
root.title("Sistema de Manutenção - Clientes")

# Frame de inclusão
frame = Frame(root)
frame.pack(pady=10)

Label(frame, text="Nome").grid(row=0, column=0)
entry_nome = Entry(frame)
entry_nome.grid(row=0, column=1)

Label(frame, text="Número").grid(row=1, column=0)
entry_numero = Entry(frame)
entry_numero.grid(row=1, column=1)

Label(frame, text="Endereço").grid(row=2, column=0)
entry_endereco = Entry(frame)
entry_endereco.grid(row=2, column=1)

Button(frame, text="Incluir Cliente", command=incluir).grid(row=3, columnspan=2)

# Treeview para consulta
tree = ttk.Treeview(root, columns=("cod_Clientes", "nome", "numero", "endereco"), show='headings')
tree.heading("cod_Clientes", text="Código")
tree.heading("nome", text="Nome")
tree.heading("numero", text="Número")
tree.heading("endereco", text="Endereço")
tree.pack()

Button(root, text="Consultar Clientes", command=consultar).pack()
Button(root, text="Excluir Cliente", command=excluir).pack()

root.mainloop()
