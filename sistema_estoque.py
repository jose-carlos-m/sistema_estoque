import sqlite3

# Função para conectar ao banco de dados SQLite
def conectar_banco():
    conn = sqlite3.connect('estoque.db')
    return conn

# Função para criar tabelas se não existirem
def criar_tabelas():
    conn = conectar_banco()
    cursor = conn.cursor()
    
    # Tabela de produtos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            preco REAL NOT NULL,
            quantidade INTEGER NOT NULL
        )
    ''')
    
    # Tabela de vendas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vendas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            produto_id INTEGER NOT NULL,
            quantidade_vendida INTEGER NOT NULL,
            valor_total REAL NOT NULL,
            FOREIGN KEY (produto_id) REFERENCES produtos(id)
        )
    ''')
    
    conn.commit()
    conn.close()

# Função para adicionar produtos
def adicionar_produto(nome, preco, quantidade):
    conn = conectar_banco()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO produtos (nome, preco, quantidade) 
        VALUES (?, ?, ?)
    ''', (nome, preco, quantidade))
    
    conn.commit()
    conn.close()
    print(f'Produto {nome} adicionado com sucesso!')

# Função para registrar uma venda
def registrar_venda(produto_id, quantidade_vendida):
    conn = conectar_banco()
    cursor = conn.cursor()
    
    # Verificar se o produto existe e se há estoque suficiente
    cursor.execute('SELECT quantidade, preco FROM produtos WHERE id = ?', (produto_id,))
    produto = cursor.fetchone()
    
    if produto is None:
        print("Produto não encontrado.")
        return
    
    quantidade_estoque, preco = produto
    
    if quantidade_estoque < quantidade_vendida:
        print("Estoque insuficiente para essa venda.")
        return
    
    # Atualizar o estoque
    nova_quantidade = quantidade_estoque - quantidade_vendida
    cursor.execute('UPDATE produtos SET quantidade = ? WHERE id = ?', (nova_quantidade, produto_id))
    
    # Registrar a venda
    valor_total = quantidade_vendida * preco
    cursor.execute('''
        INSERT INTO vendas (produto_id, quantidade_vendida, valor_total)
        VALUES (?, ?, ?)
    ''', (produto_id, quantidade_vendida, valor_total))
    
    conn.commit()
    conn.close()
    print(f'Venda registrada com sucesso! Produto {produto_id}, Quantidade vendida: {quantidade_vendida}, Valor total: R$ {valor_total:.2f}')

# Função para consultar estoque
def consultar_estoque():
    conn = conectar_banco()
    cursor = conn.cursor()
    
    cursor.execute('SELECT id, nome, preco, quantidade FROM produtos')
    produtos = cursor.fetchall()
    
    print("\n--- Estoque Atual ---")
    for produto in produtos:
        print(f'ID: {produto[0]}, Nome: {produto[1]}, Preço: R$ {produto[2]:.2f}, Quantidade: {produto[3]} unidades')
    
    conn.close()

# Função principal para exibir o menu
def menu():
    criar_tabelas()
    while True:
        print("\nSistema de Controle de Estoque e Vendas")
        print("1. Adicionar Produto")
        print("2. Registrar Venda")
        print("3. Consultar Estoque")
        print("4. Sair")
        
        opcao = input("Escolha uma opção: ")
        
        if opcao == "1":
            nome = input("Nome do produto: ")
            preco = float(input("Preço do produto: "))
            quantidade = int(input("Quantidade em estoque: "))
            adicionar_produto(nome, preco, quantidade)
        
        elif opcao == "2":
            produto_id = int(input("ID do produto: "))
            quantidade_vendida = int(input("Quantidade vendida: "))
            registrar_venda(produto_id, quantidade_vendida)
        
        elif opcao == "3":
            consultar_estoque()
        
        elif opcao == "4":
            print("Saindo do sistema...")
            break
        
        else:
            print("Opção inválida! Tente novamente.")

# Executar o sistema
if __name__ == "__main__":
    menu()