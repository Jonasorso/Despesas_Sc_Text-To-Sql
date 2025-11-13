import pandas as pd
import sqlite3

csv_path = "/home/jonas/nl2sql/data/despesas/despesa_2025_04.csv"
db_path = "/home/jonas/nl2sql/data/expense/expense.db"

colunas_pt_para_en = {
    'Ano': 'year',
    'Nro Mês': 'month_number',
    'Mês': 'month',
    'Nro Bimestre': 'bimester_number',
    'Bimestre': 'bimester',
    'Nro Trimestre': 'trimester_number',
    'Trimestre': 'trimester',
    'Nro Quadrimestre': 'quadrimester_number',
    'Quadrimestre': 'quadrimester',
    'Nro Semestre': 'semester_number',
    'Semestre': 'semester',
    'Código Poder': 'power_code',
    'Poder': 'power_name',
    'Código Órgão': 'agency_code',
    'Órgão': 'agency_name',
    'Código Unidade Gestora': 'unit_code',
    'Unidade Gestora': 'unit_name',
    'Código Gestão': 'management_code',
    'Gestão': 'management_name',
    'Código Tipo Entidade': 'entity_type_code',
    'Tipo Entidade': 'entity_type_name',
    'Código Função': 'function_code',
    'Função': 'function_name',
    'Código Subfunção': 'subfunction_code',
    'Subfunção': 'subfunction_name',
    'Código Programa': 'program_code',
    'Programa': 'program_name',
    'Código Ação': 'action_code',
    'Ação': 'action_name',
    'Código Subação': 'subaction_code',
    'Subação': 'subaction_name',
    'Código Identificador Uso': 'usage_code',
    'Identificador Uso': 'usage_name',
    'Código Fonte Recurso': 'source_code',
    'Fonte Recurso': 'source_name',
    'Código Grupo Fonte Recurso': 'group_code',
    'Grupo Fonte Recurso': 'group_name',
    'Código Especificação Fonte': 'specification_code',
    'Especificação Fonte': 'specification_name',
    'Código Tipo Fonte': 'type_code',
    'Tipo Fonte': 'type_name',
    'Código Categoria Econômica': 'category_code',
    'Categoria Econômica': 'category_name',
    'Código Grupo Natureza Despesa': 'expense_group_code',
    'Grupo Natureza Despesa': 'expense_group_name',
    'Código Modalidade Aplicação': 'modality_code',
    'Modalidade Aplicação': 'modality_name',
    'Código Elemento': 'element_code',
    'Elemento': 'element_name',
    'Código Subelemento': 'subelement_code',
    'Subelemento': 'subelement_name',
    'Código Credor': 'creditor_code',
    'Credor': 'creditor_name',                # adicionando, pois estava faltando
    'Indicador Despesa Emergencial': 'emergency_indicator',
    'Descrição Indicador Despesa Emergencial': 'emergency_expense_description',
    'Vl Dotação Inicial': 'initial_budget_value',
    'Vl Dotação Atualizada': 'updated_budget_value',
    'Vl Empenhado': 'committed_value',
    'Vl Liquidado': 'settled_value',
    'Vl Pago Orçamentário': 'paid_budget_value'
}

# Lê o CSV original
df = pd.read_csv(csv_path, sep=";", encoding="latin1", dtype=str)

# Renomeia as colunas com base no dicionário
df.rename(columns=colunas_pt_para_en, inplace=True)

# Cria conexão com o banco
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Insere dados nas tabelas dimensionais (usando "INSERT OR IGNORE" para evitar duplicatas)
def insert_dim(table, code_col, name_col):
    print(f"insery dim {table} {code_col} {name_col}")  
    print(df.head(5))  
    data = df[[code_col, name_col]].drop_duplicates().dropna()
    print(data.head(5))
    for _, row in data.iterrows():
        cursor.execute(f'''
            INSERT OR IGNORE INTO {table} ({code_col}, {name_col}) VALUES (?, ?)
        ''', (row[code_col], row[name_col]))

# Exemplo: inserir dados nas dimensões
insert_dim("power_branch", "power_code", "power_name")
insert_dim("agency", "agency_code", "agency_name")
insert_dim("management_unit", "unit_code", "unit_name")
insert_dim("function", "function_code", "function_name")
insert_dim("subfunction", "subfunction_code", "subfunction_name")
insert_dim("program", "program_code", "program_name")
insert_dim("action", "action_code", "action_name")
insert_dim("subaction", "subaction_code", "subaction_name")
insert_dim("funding_source", "source_code", "source_name")
insert_dim("source_group", "group_code", "group_name")
insert_dim("source_type", "type_code", "type_name")
insert_dim("funding_specification", "specification_code", "specification_name")
insert_dim("economic_category", "category_code", "category_name")
insert_dim("expense_group", "expense_group_code", "expense_group_name")
insert_dim("application_modality", "modality_code", "modality_name")
insert_dim("element", "element_code", "element_name")
insert_dim("subelement", "subelement_code", "subelement_name")
insert_dim("management", "management_code", "management_name")
insert_dim("entity_type", "entity_type_code", "entity_type_name")
insert_dim("usage", "usage_code", "usage_name")

# Inserir na dimensão de tempo (composição de colunas)
df['month_number'] = df['month_number'].astype(int)
df['time_id'] = df['year'].astype(str) + df['month_number'].astype(str).str.zfill(2)
df['time_id'] = df['time_id'].astype(int)

time_dim = df[['time_id', 'year', 'month_number', 'month']].drop_duplicates()
for _, row in time_dim.iterrows():
    cursor.execute('''
        INSERT OR IGNORE INTO time (id, year, month_number, month) VALUES (?, ?, ?, ?)
    ''', (row['time_id'], row['year'], row['month_number'], row['month']))

# Inserir dados na tabela fato
fact_cols = [
    'time_id', 'power_code', 'agency_code', 'unit_code', 'management_code',
    'entity_type_code', 'function_code', 'subfunction_code', 'program_code',
    'action_code', 'subaction_code', 'usage_code', 'source_code',
    'group_code', 'specification_code', 'type_code', 'category_code',
    'expense_group_code', 'modality_code', 'element_code', 'subelement_code',
    'creditor_code', 'emergency_indicator', 'initial_budget_value',
    'updated_budget_value', 'committed_value', 'settled_value',
    'paid_budget_value', 'emergency_expense_description'
]

for _, row in df[fact_cols].dropna(subset=['time_id']).iterrows():
    placeholders = ', '.join(['?'] * len(fact_cols))
    cursor.execute(f'''
        INSERT INTO expense_fact ({', '.join(fact_cols)})
        VALUES ({placeholders})
    ''', tuple(row[col] for col in fact_cols))

conn.commit()
conn.close()

print("✅ Dados importados com sucesso para o banco com schema em inglês.")
