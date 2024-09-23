import sqlite3
from datetime import datetime

# Conexão com o banco de dados SQLite
conn = sqlite3.connect('mercadinho.db')
cursor = conn.cursor()

# Função para criar as tabelas necessárias (produtos e vendas)
def criar_tabelas():
    cursor.execute('''CREATE TABLE IF NOT EXISTS produtos (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nome TEXT NOT NULL,
                        preco REAL NOT NULL,
                        quantidade INTEGER NOT NULL)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS vendas (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        produto_id INTEGER NOT NULL,
                        quantidade_vendida INTEGER NOT NULL,
                        data_venda TEXT NOT NULL,
                        FOREIGN KEY (produto_id) REFERENCES produtos(id))''')

    conn.commit()

# Função para cadastrar novos produtos
def cadastrar_produto(nome, preco, quantidade):
    cursor.execute('INSERT INTO produtos (nome, preco, quantidade) VALUES (?, ?, ?)', (nome, preco, quantidade))
    conn.commit()
    print(f'Produto {nome} cadastrado com sucesso!')

# Função para registrar uma venda
def registrar_venda(produto_id, quantidade_vendida):
    # Verificar se o produto existe e se tem estoque suficiente
    cursor.execute('SELECT quantidade FROM produtos WHERE id = ?', (produto_id,))
    produto = cursor.fetchone()

    if produto and produto[0] >= quantidade_vendida:
        # Atualizar estoque
        nova_quantidade = produto[0] - quantidade_vendida
        cursor.execute('UPDATE produtos SET quantidade = ? WHERE id = ?', (nova_quantidade, produto_id))
        
        # Registrar a venda
        data_venda = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute('INSERT INTO vendas (produto_id, quantidade_vendida, data_venda) VALUES (?, ?, ?)', (produto_id, quantidade_vendida, data_venda))
        
        conn.commit()
        print(f'Venda registrada com sucesso! {quantidade_vendida} unidade(s) vendida(s).')
    else:
        print('Estoque insuficiente ou produto não encontrado.')

# Função para exibir o estoque atual
def exibir_estoque():
    cursor.execute('SELECT * FROM produtos')
    produtos = cursor.fetchall()

    if produtos:
        print('Estoque atual:')
        for produto in produtos:
            print(f'ID: {produto[0]} | Nome: {produto[1]} | Preço: R$ {produto[2]:.2f} | Quantidade: {produto[3]}')
    else:
        print('Nenhum produto cadastrado.')

# Função para exibir o histórico de vendas
def exibir_historico_vendas():
    cursor.execute('''SELECT vendas.id, produtos.nome, vendas.quantidade_vendida, vendas.data_venda 
                      FROM vendas 
                      JOIN produtos ON vendas.produto_id = produtos.id''')
    vendas = cursor.fetchall()

    if vendas:
        print('Histórico de vendas:')
        for venda in vendas:
            print(f'ID da venda: {venda[0]} | Produto: {venda[1]} | Quantidade: {venda[2]} | Data: {venda[3]}')
    else:
        print('Nenhuma venda registrada.')

# Função principal para interagir com o usuário
def menu():
    criar_tabelas()
    while True:
        print("\n===== Menu do Mercadinho =====")
        print("1. Cadastrar Produto")
        print("2. Registrar Venda")
        print("3. Exibir Estoque")
        print("4. Exibir Histórico de Vendas")
        print("5. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            nome = input("Nome do produto: ")
            preco = float(input("Preço do produto: "))
            quantidade = int(input("Quantidade em estoque: "))
            cadastrar_produto(nome, preco, quantidade)
        
        elif opcao == '2':
            exibir_estoque()
            produto_id = int(input("ID do produto a ser vendido: "))
            quantidade_vendida = int(input("Quantidade a ser vendida: "))
            registrar_venda(produto_id, quantidade_vendida)
        
        elif opcao == '3':
            exibir_estoque()
        
        elif opcao == '4':
            exibir_historico_vendas()
        
        elif opcao == '5':
            print("Saindo...")
            break
        
        else:
            print("Opção inválida. Tente novamente.")

# Executar o menu
if __name__ == "__main__":
    menu()

# Fechar a conexão ao encerrar o programa
conn.close()
