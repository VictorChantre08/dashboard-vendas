import pandas as pd
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 1. LER A TABELA
# O pandas vai ler seu arquivo e guardar na variável 'df'
df = pd.read_excel('vendas.xlsx')

# 2. LIMPEZA (O passo mais importante para você!)
# Lembra que no Excel deu erro #VALOR!? Vamos corrigir isso aqui.
# Transformamos a coluna em números. Se algo não for número, vira 'NaN' (vazio)
df['preco_unitario'] = pd.to_numeric(df['preco_unitario'], errors='coerce')
df['quantidade'] = pd.to_numeric(df['quantidade'], errors='coerce')

# 3. FAZER A CONTA (Quantidade x Preço)
# O Python faz isso para todas as linhas de uma vez
df['valor_total'] = df['quantidade'] * df['preco_unitario']

# 4. TRATAR DATAS
# Garante que o Python entenda a coluna 'data' como tempo, não texto
df['data'] = pd.to_datetime(df['data'])

# 5. ANÁLISES SIMPLES
print("--- RELATÓRIO DE VENDAS ---")

# Quanto vendemos no total?
total_geral = df['valor_total'].sum()
print(f"Faturamento Total: R$ {total_geral:,.2f}")

# Qual estado vendeu mais? (Equivalente à Tabela Dinâmica)
vendas_por_estado = df.groupby('estado')['valor_total'].sum().sort_values(ascending=False)
print("\nRanking de Vendas por Estado:")
print(vendas_por_estado)

# 6. SALVAR O RESULTADO
# Cria um novo Excel com a coluna 'valor_total' corrigida
df.to_excel('vendas_finalizadas.xlsx', index=False)
print("\nArquivo 'vendas_finalizadas.xlsx' salvo com sucesso!")

# 7. Média de preços dos produtos vendidos
media_preco = df['preco_unitario'].mean()
print(f"O preço médio dos produtos é: R$ {media_preco:.2f}")


# --- Incluindo trabalho com gráficos ---

import matplotlib.pyplot as plt

# Criar o gráfico de barras dos estados
vendas_por_estado.plot(kind='bar', color='skyblue')

plt.title('Vendas Totais por Estado')
plt.xlabel('Estado')
plt.ylabel('Valor Total (R$)')
plt.xticks(rotation=45) # Inclina os nomes dos estados para ler melhor
plt.tight_layout() # Ajusta o espaçamento

# Salva o gráfico como uma imagem
plt.savefig('grafico_vendas_estado.png')
print("Gráfico gerado com sucesso!")

# Se quiser que o gráfico abra na tela agora:
plt.show()


# --- ANÁLISE DE PRODUTOS ---
print("\n--- Volume de Vendas por Produto ---")
ranking_produtos = df.groupby('produto')['quantidade'].sum().sort_values(ascending=False)
print(ranking_produtos)

# Criar um gráfico para os produtos
plt.figure(figsize=(10, 6))
ranking_produtos.plot(kind='barh', color='salmon') # 'barh' faz barras horizontais
plt.title('Produtos Mais Vendidos (Quantidade)')
plt.xlabel('Quantidade Total')
plt.tight_layout()
plt.savefig('produtos_mais_vendidos.png')


# --- ANÁLISE ESPECÍFICA: SÃO PAULO ---

# 1. Criar um novo DataFrame apenas com dados de SP
df_sp = df[df['estado'] == 'SP']

print("\n--- Relatório Específico: SÃO PAULO ---")
print(f"Total de vendas em SP: {len(df_sp)} transações")
print(f"Faturamento em SP: R$ {df_sp['valor_total'].sum():,.2f}")

# 2. Qual o produto mais vendido especificamente em SP?
ranking_sp = df_sp.groupby('produto')['quantidade'].sum().sort_values(ascending=False)
print("\nProdutos mais vendidos em SP:")
print(ranking_sp)

# 3. Salvar apenas os dados de SP em um Excel separado
df_sp.to_excel('vendas_apenas_SP.xlsx', index=False)
print("\nArquivo 'vendas_apenas_SP.xlsx' gerado com sucesso!")
