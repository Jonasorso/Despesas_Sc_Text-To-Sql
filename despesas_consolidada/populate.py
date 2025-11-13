import pandas as pd
import sqlite3

# Caminhos
CSV_PATH = "/home/jonas/nl2sql/data/despesas/despesa_2025_04.csv"
DB_PATH = "/home/jonas/nl2sql/data/despesas_consolidada/despesas_consolidada.db"

# Função para converter valores monetários (ex: '7.000,00' → 7000.00)
def parse_float(val):
    if pd.isna(val):
        return None
    try:
        val = str(val).strip().replace('.', '').replace(',', '.')
        return float(val)
    except (ValueError, TypeError):
        return None

# Lê o CSV
df = pd.read_csv(CSV_PATH, sep=";", encoding="latin1", dtype=str)

# Converte os campos float
float_cols = [
    'Vl Dotação Inicial',
    'Vl Dotação Atualizada',
    'Vl Empenhado',
    'Vl Liquidado',
    'Vl Pago Orçamentário'
]
for col in float_cols:
    df[col] = df[col].apply(parse_float)

# Conecta ao SQLite
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Insere os dados
for idx, row in df.iterrows():
    values = (
        row['Ano'],
        row['Nro Mês'],
        row['Mês'],
        row['Nro Bimestre'],
        row['Bimestre'],
        row['Nro Trimestre'],
        row['Trimestre'],
        row['Nro Quadrimestre'],
        row['Quadrimestre'],
        row['Nro Semestre'],
        row['Semestre'],
        row['Código Poder'],
        row['Poder'],
        row['Código Órgão'],
        row['Órgão'],
        row['Código Unidade Gestora'],
        row['Unidade Gestora'],
        row['Código Gestão'],
        row['Gestão'],
        row['Código Tipo Entidade'],
        row['Tipo Entidade'],
        row['Código Função'],
        row['Função'],
        row['Código Subfunção'],
        row['Subfunção'],
        row['Código Programa'],
        row['Programa'],
        row['Código Ação'],
        row['Ação'],
        row['Código Subação'],
        row['Subação'],
        row['Código Identificador Uso'],
        row['Identificador Uso'],
        row['Código Fonte Recurso'],
        row['Fonte Recurso'],
        row['Código Grupo Fonte Recurso'],
        row['Grupo Fonte Recurso'],
        row['Código Especificação Fonte'],
        row['Especificação Fonte'],
        row['Código Tipo Fonte'],
        row['Tipo Fonte'],
        row['Código Categoria Econômica'],
        row['Categoria Econômica'],
        row['Código Grupo Natureza Despesa'],
        row['Grupo Natureza Despesa'],
        row['Código Modalidade Aplicação'],
        row['Modalidade Aplicação'],
        row['Código Elemento'],
        row['Elemento'],
        row['Código Subelemento'],
        row['Subelemento'],
        row.get('Código Credor', ''),
        row.get('Credor', ''),
        row.get('Indicador Despesa Emergencial', ''),
        row.get('Descrição Indicador Despesa Emergencial', ''),
        row['Vl Dotação Inicial'],
        row['Vl Dotação Atualizada'],
        row['Vl Empenhado'],
        row['Vl Liquidado'],
        row['Vl Pago Orçamentário']
    )

    cursor.execute("""
        INSERT INTO despesas_consolidadas VALUES (
            ?,?,?,?,?,?,?,?,?,?,
            ?,?,?,?,?,?,?,?,?,?,
            ?,?,?,?,?,?,?,?,?,?,
            ?,?,?,?,?,?,?,?,?,?,
            ?,?,?,?,?,?,?,?,?,?,
            ?,?,?,?,?,?,?,?,?,?
        )
    """, values)

    if idx % 100 == 0:
        conn.commit()

conn.commit()
conn.close()
print("Importação consolidada concluída com sucesso.")
