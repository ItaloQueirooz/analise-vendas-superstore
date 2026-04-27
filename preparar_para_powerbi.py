import pandas as pd
import warnings
warnings.filterwarnings('ignore')

# ============================================================
# CONFIGURAÇÕES
# ============================================================
ARQUIVO_ENTRADA = r"D:\AnaliseDados\Sample - Superstore.csv"
ARQUIVO_SAIDA   = r"D:\AnaliseDados\superstore_limpo.csv"

# ============================================================
# 1. CARREGAR
# ============================================================
print("=" * 55)
print("  LIMPEZA E PREPARAÇÃO — SUPERSTORE")
print("=" * 55)

df = pd.read_csv(ARQUIVO_ENTRADA, encoding='latin1')
print(f"\n📦 Arquivo carregado: {df.shape[0]:,} linhas | {df.shape[1]} colunas")

# ============================================================
# 2. LIMPEZA
# ============================================================
print("\n🧹 Iniciando limpeza...")

# 2.1 Remover duplicatas
antes = len(df)
df = df.drop_duplicates()
depois = len(df)
print(f"   ✅ Duplicatas removidas: {antes - depois}")

# 2.2 Corrigir tipos de data
df['Order Date'] = pd.to_datetime(df['Order Date'])
df['Ship Date']  = pd.to_datetime(df['Ship Date'])
print(f"   ✅ Datas convertidas corretamente")

# 2.3 Verificar nulos
nulos = df.isnull().sum().sum()
print(f"   ✅ Valores nulos encontrados: {nulos}")

# 2.4 Padronizar texto (remover espaços extras)
colunas_texto = df.select_dtypes(include='object').columns
for col in colunas_texto:
    df[col] = df[col].str.strip()
print(f"   ✅ Textos padronizados")

# ============================================================
# 3. ENRIQUECIMENTO — novas colunas úteis para o Power BI
# ============================================================
print("\n✨ Adicionando colunas calculadas...")

# Ano, Mês e Trimestre
df['Ano']       = df['Order Date'].dt.year
df['Mes']       = df['Order Date'].dt.month
df['Mes_Nome']  = df['Order Date'].dt.strftime('%B')
df['Trimestre'] = df['Order Date'].dt.quarter.map({1:'Q1', 2:'Q2', 3:'Q3', 4:'Q4'})
print(f"   ✅ Ano, Mês, Trimestre extraídos")

# Dias para envio
df['Dias_Envio'] = (df['Ship Date'] - df['Order Date']).dt.days
print(f"   ✅ Dias de envio calculados")

# Margem de lucro por pedido
df['Margem_%'] = (df['Profit'] / df['Sales'] * 100).round(2)
print(f"   ✅ Margem % calculada por pedido")

# Classificação de desconto
df['Faixa_Desconto'] = pd.cut(
    df['Discount'],
    bins=[-0.01, 0, 0.2, 0.4, 1.0],
    labels=['Sem Desconto', 'Desconto Baixo (1-20%)', 'Desconto Médio (21-40%)', 'Desconto Alto (41%+)']
)
print(f"   ✅ Faixas de desconto classificadas")

# Classificação de lucro
df['Status_Lucro'] = df['Profit'].apply(
    lambda x: '✅ Lucrativo' if x > 0 else '❌ Prejuízo'
)
print(f"   ✅ Status de lucro por pedido")

# Ticket médio por pedido
ticket = df.groupby('Order ID')['Sales'].sum().reset_index()
ticket.columns = ['Order ID', 'Ticket_Total_Pedido']
df = df.merge(ticket, on='Order ID', how='left')
print(f"   ✅ Ticket total por pedido")

# ============================================================
# 4. FILTROS — remover dados problemáticos
# ============================================================
print("\n🔍 Aplicando filtros de qualidade...")

# Remover vendas zeradas ou negativas
antes = len(df)
df = df[df['Sales'] > 0]
print(f"   ✅ Vendas inválidas removidas: {antes - len(df)}")

# Remover dias de envio negativos (erro de dados)
antes = len(df)
df = df[df['Dias_Envio'] >= 0]
print(f"   ✅ Datas de envio inválidas removidas: {antes - len(df)}")

# ============================================================
# 5. RESUMO FINAL
# ============================================================
print("\n" + "─" * 55)
print("📊 RESUMO DO DATASET LIMPO")
print("─" * 55)
print(f"   Total de pedidos  : {df['Order ID'].nunique():,}")
print(f"   Total de clientes : {df['Customer ID'].nunique():,}")
print(f"   Total de produtos : {df['Product ID'].nunique():,}")
print(f"   Período           : {df['Order Date'].min().strftime('%d/%m/%Y')} até {df['Order Date'].max().strftime('%d/%m/%Y')}")
print(f"   Vendas totais     : ${df['Sales'].sum():,.2f}")
print(f"   Lucro total       : ${df['Profit'].sum():,.2f}")
print(f"   Margem média      : {df['Margem_%'].mean():.1f}%")
print(f"   Pedidos lucrativos: {(df['Status_Lucro'] == '✅ Lucrativo').sum():,}")
print(f"   Pedidos prejuízo  : {(df['Status_Lucro'] == '❌ Prejuízo').sum():,}")

# ============================================================
# 6. EXPORTAR
# ============================================================
df.to_csv(ARQUIVO_SAIDA, index=False, encoding='utf-8-sig')

print("\n" + "=" * 55)
print(f"✅ Arquivo salvo em:")
print(f"   {ARQUIVO_SAIDA}")
print("=" * 55)
print("\n💡 Próximo passo: abra o Power BI e importe")
print("   o arquivo 'superstore_limpo.csv'")
