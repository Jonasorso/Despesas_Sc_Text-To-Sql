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

# Função para converter string numérica com vírgula para float ou None se vazio
def to_float(val):
    if pd.isna(val):
        return None
    val = val.strip()
    if val == '' or val.upper() == 'N/A':
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
        df[col] = df[col].apply(to_float)
    else:
        print(f"Atenção: coluna float '{col}' não encontrada no CSV.")

# Função auxiliar para inserir dimensões e evitar duplicados
def insert_dim(table, cod_col, nome_col, cod_val, nome_val):
    if cod_val is None or cod_val == '':
        return
    cursor.execute(f"SELECT 1 FROM {table} WHERE {cod_col} = ?", (cod_val,))
    if cursor.fetchone() is None:
        cursor.execute(
            f"INSERT INTO {table} ({cod_col}, {nome_col}) VALUES (?, ?)",
            (cod_val, nome_val)
        )

# Cache para ids da tabela tempo
tempo_cache = {}

def get_tempo_id(row):
    key = (
        int(row['Ano']),
        int(row['Nro Mês']),
        row['Mês'],
        int(row['Nro Bimestre']),
        row['Bimestre'],
        int(row['Nro Trimestre']),
        row['Trimestre'],
        int(row['Nro Quadrimestre']),
        row['Quadrimestre'],
        int(row['Nro Semestre']),
        row['Semestre']
    )
    if key in tempo_cache:
        return tempo_cache[key]

    cursor.execute("""
        SELECT id FROM tempo WHERE 
            ano=? AND nro_mes=? AND mes=? AND
            nro_bimestre=? AND bimestre=? AND
            nro_trimestre=? AND trimestre=? AND
            nro_quadrimestre=? AND quadrimestre=? AND
            nro_semestre=? AND semestre=?
    """, key)
    res = cursor.fetchone()
    if res:
        tempo_cache[key] = res[0]
        return res[0]

    cursor.execute("""
        INSERT INTO tempo (
            ano, nro_mes, mes, nro_bimestre, bimestre,
            nro_trimestre, trimestre, nro_quadrimestre, quadrimestre,
            nro_semestre, semestre
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, key)
    conn.commit()
    tempo_id = cursor.lastrowid
    tempo_cache[key] = tempo_id
    return tempo_id

print("Iniciando inserção dos dados...")

for idx, row in df.iterrows():
    # Inserção das dimensões
    insert_dim('poder', 'cod_poder', 'nome_poder', row['Código Poder'], row['Poder'])
    insert_dim('orgao', 'cod_orgao', 'nome_orgao', row['Código Órgão'], row['Órgão'])
    insert_dim('unidade_gestora', 'cod_ug', 'nome_ug', row['Código Unidade Gestora'], row['Unidade Gestora'])
    insert_dim('gestao', 'cod_gestao', 'nome_gestao', row['Código Gestão'], row['Gestão'])
    insert_dim('tipo_entidade', 'cod_tipo_entidade', 'nome_tipo_entidade', row['Código Tipo Entidade'], row['Tipo Entidade'])
    insert_dim('funcao', 'cod_funcao', 'nome_funcao', row['Código Função'], row['Função'])
    insert_dim('subfuncao', 'cod_subfuncao', 'nome_subfuncao', row['Código Subfunção'], row['Subfunção'])
    insert_dim('programa', 'cod_programa', 'nome_programa', row['Código Programa'], row['Programa'])
    insert_dim('acao', 'cod_acao', 'nome_acao', row['Código Ação'], row['Ação'])
    insert_dim('subacao', 'cod_subacao', 'nome_subacao', row['Código Subação'], row['Subação'])
    insert_dim('uso', 'cod_uso', 'nome_uso', row['Código Identificador Uso'], row['Identificador Uso'])
    insert_dim('fonte_recurso', 'cod_fonte', 'nome_fonte', row['Código Fonte Recurso'], row['Fonte Recurso'])
    insert_dim('grupo_fonte', 'cod_grupo', 'nome_grupo', row['Código Grupo Fonte Recurso'], row['Grupo Fonte Recurso'])
    insert_dim('especificacao_fonte', 'cod_especificacao', 'nome_especificacao', row['Código Especificação Fonte'], row['Especificação Fonte'])
    insert_dim('tipo_fonte', 'cod_tipo', 'nome_tipo', row['Código Tipo Fonte'], row['Tipo Fonte'])
    insert_dim('categoria_economica', 'cod_categoria', 'nome_categoria', row['Código Categoria Econômica'], row['Categoria Econômica'])
    insert_dim('grupo_despesa', 'cod_grupo', 'nome_grupo', row['Código Grupo Natureza Despesa'], row['Grupo Natureza Despesa'])
    insert_dim('modalidade_aplicacao', 'cod_modalidade', 'nome_modalidade', row['Código Modalidade Aplicação'], row['Modalidade Aplicação'])
    insert_dim('elemento', 'cod_elemento', 'nome_elemento', row['Código Elemento'], row['Elemento'])
    insert_dim('subelemento', 'cod_subelemento', 'nome_subelemento', row['Código Subelemento'], row['Subelemento'])

    tempo_id = get_tempo_id(row)

    # Prepara valores para fato_despesa
    vals = (
        tempo_id,
        row.get('Código Poder'),
        row.get('Código Órgão'),
        row.get('Código Unidade Gestora'),
        row.get('Código Gestão'),
        row.get('Código Tipo Entidade'),
        row.get('Código Função'),
        row.get('Código Subfunção'),
        row.get('Código Programa'),
        row.get('Código Ação'),
        row.get('Código Subação'),
        row.get('Código Identificador Uso'),
        row.get('Código Fonte Recurso'),
        row.get('Código Grupo Fonte Recurso'),
        row.get('Código Especificação Fonte'),
        row.get('Código Tipo Fonte'),
        row.get('Código Categoria Econômica'),
        row.get('Código Grupo Natureza Despesa'),
        row.get('Código Modalidade Aplicação'),
        row.get('Código Elemento'),
        row.get('Código Subelemento'),
        row.get('Código Credor'),  # cod_credor removido do CSV/tabela, ajusta aqui se necessário
        row.get('Indicador Despesa Emergencial'),  # indicador_emergencial removido do CSV/tabela
        row['Vl Dotação Inicial'],
        row['Vl Dotação Atualizada'],
        row['Vl Empenhado'],
        row['Vl Liquidado'],
        row['Vl Pago Orçamentário'],
        row.get('Descrição Indicador Despesa Emergencial', None)
    )

    cursor.execute("""
        INSERT INTO fato_despesa (
            tempo_id,
            cod_poder,
            cod_orgao,
            cod_ug,
            cod_gestao,
            cod_tipo_entidade,
            cod_funcao,
            cod_subfuncao,
            cod_programa,
            cod_acao,
            cod_subacao,
            cod_uso,
            cod_fonte,
            cod_grupo,
            cod_especificacao,
            cod_tipo,
            cod_categoria,
            cod_grupo_despesa,
            cod_modalidade,
            cod_elemento,
            cod_subelemento,
            cod_credor,
            indicador_emergencial,
            vl_dotacao_inicial,
            vl_dotacao_atualizada,
            vl_empenhado,
            vl_liquidado,
            vl_pago_orcamentario,
            descricao_despesa_emergencial
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, vals)

    if idx % 100 == 0:
        conn.commit()

conn.commit()
conn.close()

print("Importação finalizada com sucesso.")
