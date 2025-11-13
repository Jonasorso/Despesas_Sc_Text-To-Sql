import pandas as pd
import sqlite3
from unidecode import unidecode

CSV_PATH = "/home/jonas/nl2sql/data/despesas/despesa_2025_01.csv"
DB_PATH = "/home/jonas/nl2sql/data/despesas/despesas.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Lista das tabelas a limpar antes da inserção (ajuste conforme necessário)
tables_to_clear = [
    'fato_despesa', 'tempo', 'poder', 'orgao', 'unidade_gestora', 'gestao',
    'tipo_entidade', 'funcao', 'subfuncao', 'programa', 'acao', 'subacao', 'uso',
    'fonte_recurso', 'grupo_fonte', 'especificacao_fonte', 'tipo_fonte',
    'categoria_economica', 'grupo_despesa', 'modalidade_aplicacao', 'elemento',
    'subelemento'
]

print("Limpando tabelas...")
for t in tables_to_clear:
    cursor.execute(f"DELETE FROM {t};")
conn.commit()
print("Tabelas limpas.")



# Carrega CSV com pandas
df = pd.read_csv(CSV_PATH, sep=";", encoding="latin1", dtype=str)
df = df[:10]
# Função para converter string numérica com vírgula para float ou None se vazio
def to_float(val):
    if pd.isna(val):
        print('isna')
        return None
    val = val.strip()
    if val == '' or val.upper() == 'N/A':
        print('N/A')
        return None
    val = val.replace('.', '').replace(',', '.')
    try:
        return float(val)
    except:
        return None

# Lista de colunas float no CSV que serão convertidas
float_cols = [
    'Vl Dotação Inicial',
    'Vl Dotação Atualizada',
    'Vl Empenhado',
    'Vl Liquidado',
    'Vl Pago Orçamentário'
]

for col in float_cols:
    if col in df.columns:
        print("valor antes ", df[col])            
        df[col] = df[col].apply(to_float)        
        print("valor depois ", df[col])    
    else:
        print(f"Atenção: coluna float '{col}' não encontrada no CSV.")