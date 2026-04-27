import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# ============================================================
# CONFIGURAÇÕES
# ============================================================
ARQUIVO = r"D:\AnaliseDados\Sample - Superstore.csv"

sns.set_theme(style="darkgrid")
plt.rcParams['figure.figsize'] = (12, 5)

# ============================================================
# 1. CARREGAR OS DADOS
# ============================================================
print("=" * 55)
print("  ANÁLISE DE VENDAS — SUPERSTORE")
print("=" * 55)

df = pd.read_csv(ARQUIVO, encoding='latin1')

print(f"\n📦 Dataset carregado com sucesso!")
print(f"   Linhas  : {df.shape[0]:,}")
print(f"   Colunas : {df.shape[1]}")

# ============================================================
# 2. EXPLORAÇÃO INICIAL
# ============================================================
print("\n" + "─" * 55)
print("📋 COLUNAS DISPONÍVEIS")
print("─" * 55)
for col in df.columns:
    print(f"   • {col}")

print("\n" + "─" * 55)
print("🔍 PRIMEIRAS LINHAS")
print("─" * 55)
print(df[['Order Date', 'Category', 'Sales', 'Profit', 'Discount']].head())

print("\n" + "─" * 55)
print("📊 RESUMO ESTATÍSTICO")
print("─" * 55)
print(df[['Sales', 'Profit', 'Discount', 'Quantity']].describe().round(2))

# ============================================================
# 3. PERGUNTAS DE NEGÓCIO
# ============================================================

# ── 3.1 Vendas e Lucro por Categoria ──────────────────────
print("\n" + "─" * 55)
print("💰 VENDAS E LUCRO POR CATEGORIA")
print("─" * 55)
categoria = df.groupby('Category')[['Sales', 'Profit']].sum().round(2)
categoria['Margem (%)'] = (categoria['Profit'] / categoria['Sales'] * 100).round(1)
print(categoria.sort_values('Sales', ascending=False))

# ── 3.2 Vendas por Região ──────────────────────────────────
print("\n" + "─" * 55)
print("🗺️  VENDAS E LUCRO POR REGIÃO")
print("─" * 55)
regiao = df.groupby('Region')[['Sales', 'Profit']].sum().round(2)
regiao['Margem (%)'] = (regiao['Profit'] / regiao['Sales'] * 100).round(1)
print(regiao.sort_values('Sales', ascending=False))

# ── 3.3 Top 10 produtos mais lucrativos ───────────────────
print("\n" + "─" * 55)
print("🏆 TOP 10 PRODUTOS MAIS LUCRATIVOS")
print("─" * 55)
top_lucro = df.groupby('Product Name')['Profit'].sum().sort_values(ascending=False).head(10)
print(top_lucro.round(2).to_string())

# ── 3.4 Top 10 produtos no prejuízo ───────────────────────
print("\n" + "─" * 55)
print("🚨 TOP 10 PRODUTOS NO PREJUÍZO")
print("─" * 55)
prejuizo = df.groupby('Product Name')['Profit'].sum().sort_values().head(10)
print(prejuizo.round(2).to_string())

# ── 3.5 Impacto do desconto no lucro ──────────────────────
print("\n" + "─" * 55)
print("🎯 IMPACTO DO DESCONTO NA MARGEM")
print("─" * 55)
desconto = df.groupby('Discount')[['Sales', 'Profit']].mean().round(2)
print(desconto)

# ============================================================
# 4. VISUALIZAÇÕES
# ============================================================
print("\n📈 Gerando gráficos...")

fig, axes = plt.subplots(2, 2, figsize=(16, 10))
fig.suptitle('Análise de Vendas — Superstore', fontsize=16, fontweight='bold')

# Gráfico 1 — Lucro por Categoria
categoria['Profit'].sort_values().plot(
    kind='barh', ax=axes[0, 0],
    color=['#e74c3c', '#3498db', '#2ecc71']
)
axes[0, 0].set_title('Lucro por Categoria')
axes[0, 0].set_xlabel('Lucro ($)')

# Gráfico 2 — Vendas por Região
regiao['Sales'].sort_values().plot(
    kind='barh', ax=axes[0, 1], color='steelblue'
)
axes[0, 1].set_title('Vendas por Região')
axes[0, 1].set_xlabel('Vendas ($)')

# Gráfico 3 — Desconto vs Lucro (scatter)
axes[1, 0].scatter(df['Discount'], df['Profit'], alpha=0.3, color='coral')
axes[1, 0].axhline(y=0, color='red', linestyle='--', linewidth=1)
axes[1, 0].set_title('Desconto vs Lucro por Pedido')
axes[1, 0].set_xlabel('Desconto (%)')
axes[1, 0].set_ylabel('Lucro ($)')

# Gráfico 4 — Margem por Categoria
categoria['Margem (%)'].plot(
    kind='bar', ax=axes[1, 1],
    color=['#e74c3c', '#3498db', '#2ecc71']
)
axes[1, 1].set_title('Margem de Lucro por Categoria (%)')
axes[1, 1].set_ylabel('Margem (%)')
axes[1, 1].tick_params(axis='x', rotation=0)

plt.tight_layout()
plt.savefig(r"D:\AnaliseDados\analise_superstore.png", dpi=150, bbox_inches='tight')
plt.show()

print("\n✅ Gráfico salvo em: D:\\AnaliseDados\\analise_superstore.png")
print("\n" + "=" * 55)
print("  ANÁLISE CONCLUÍDA!")
print("=" * 55)
