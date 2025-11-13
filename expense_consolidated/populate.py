import pandas as pd
import sqlite3

csv_path = "/home/jonas/nl2sql/data/despesas/despesa_2025_04.csv"
db_path = "/home/jonas/nl2sql/data/expense_consolidated/expense_consolidated.db"

def parse_float(val):
    if pd.isna(val):
        return None
    try:
        val = str(val).strip().replace('.', '').replace(',', '.')
        return float(val)
    except (ValueError, TypeError):
        return None
    
# Mapeamento de colunas em português para nomes do schema da *única* tabela expense_fact
# Ensure these map exactly to the column names in your expense_fact CREATE TABLE statement
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
    'Unidade Gestora': 'management_unit', # Keeping original name 'unidade_gestora' as per schema
    'Código Gestão': 'management_code',
    'Gestão': 'management_name', # Keeping original name 'gestao' as per schema, but for consistency using _name
    'Código Tipo Entidade': 'entity_type_code',
    'Tipo Entidade': 'entity_type', # Keeping original name 'tipo_entidade' as per schema
    'Código Função': 'function_code',
    'Função': 'function_name', # Keeping original name 'funcao' as per schema, but for consistency using _name
    'Código Subfunção': 'subfunction_code',
    'Subfunção': 'subfunction_name', # Keeping original name 'subfuncao' as per schema, but for consistency using _name
    'Código Programa': 'program_code',
    'Programa': 'program_name', # Keeping original name 'programa' as per schema, but for consistency using _name
    'Código Ação': 'action_code',
    'Ação': 'action_name', # Keeping original name 'acao' as per schema, but for consistency using _name
    'Código Subação': 'subaction_code',
    'Subação': 'subaction_name', # Keeping original name 'subacao' as per schema, but for consistency using _name
    'Código Identificador Uso': 'usage_code',
    'Identificador Uso': 'usage_name', # Keeping original name 'uso' as per schema, but for consistency using _name
    'Código Fonte Recurso': 'source_code',
    'Fonte Recurso': 'source_name', # Keeping original name 'fonte' as per schema, but for consistency using _name
    'Código Grupo Fonte Recurso': 'group_code',
    'Grupo Fonte Recurso': 'group_name', # Keeping original name 'grupo' as per schema, but for consistency using _name
    'Código Especificação Fonte': 'specification_code',
    'Especificação Fonte': 'specification_name', # Keeping original name 'especificacao' as per schema, but for consistency using _name
    'Código Tipo Fonte': 'type_code',
    'Tipo Fonte': 'type_name', # Keeping original name 'tipo' as per schema, but for consistency using _name
    'Código Categoria Econômica': 'category_code',
    'Categoria Econômica': 'category_name', # Keeping original name 'categoria' as per schema, but for consistency using _name
    'Código Grupo Natureza Despesa': 'expense_group_code',
    'Grupo Natureza Despesa': 'expense_group_name', # Keeping original name 'grupo_despesa' as per schema, but for consistency using _name
    'Código Modalidade Aplicação': 'modality_code',
    'Modalidade Aplicação': 'modality_name', # Keeping original name 'modalidade' as per schema, but for consistency using _name
    'Código Elemento': 'element_code',
    'Elemento': 'element_name', # Keeping original name 'elemento' as per schema, but for consistency using _name
    'Código Subelemento': 'subelement_code',
    'Subelemento': 'subelement_name', # Keeping original name 'subelemento' as per schema, but for consistency using _name
    'Código Credor': 'creditor_code',
    'Credor': 'creditor_name',                # Updated to 'creditor_name' as per your schema
    'Indicador Despesa Emergencial': 'emergency_indicator',
    'Descrição Indicador Despesa Emergencial': 'emergency_description', # Updated to 'emergency_description' as per your schema
    'Vl Dotação Inicial': 'initial_budget_value',
    'Vl Dotação Atualizada': 'updated_budget_value',
    'Vl Empenhado': 'committed_value',
    'Vl Liquidado': 'settled_value',
    'Vl Pago Orçamentário': 'paid_budget_value'
}

# Lê o CSV original
df = pd.read_csv(csv_path, sep=";", encoding="latin1", dtype=str)

# Clean column names by stripping whitespace before renaming
df.columns = df.columns.str.strip()

# Renomeia as colunas com base no dicionário
df.rename(columns=colunas_pt_para_en, inplace=True)

# List of columns that should be numeric (REAL) in the database
numeric_cols = [
    'initial_budget_value', 'updated_budget_value', 'committed_value',
    'settled_value', 'paid_budget_value'
]

for col in numeric_cols:    
    df[col] = df[col].str.replace(',', '.', regex=False).replace('', '0')
    df[col] = df[col].apply(parse_float)

# Create connection with the database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

fact_table_columns = [
    'year', 'month_number', 'month', 'bimester_number', 'bimester',
    'trimester_number', 'trimester', 'quadrimester_number', 'quadrimester',
    'semester_number', 'semester', 'power_code', 'power_name', 'agency_code',
    'agency_name', 'unit_code', 'management_unit', 'management_code',
    'management_name', 'entity_type_code', 'entity_type', 'function_code',
    'function_name', 'subfunction_code', 'subfunction_name', 'program_code',
    'program_name', 'action_code', 'action_name', 'subaction_code',
    'subaction_name', 'usage_code', 'usage_name', 'source_code',
    'source_name', 'group_code', 'group_name', 'specification_code',
    'specification_name', 'type_code', 'type_name', 'category_code',
    'category_name', 'expense_group_code', 'expense_group_name', 'modality_code',
    'modality_name', 'element_code', 'element_name', 'subelement_code',
    'subelement_name', 'creditor_code', 'creditor_name', 'emergency_indicator',
    'emergency_description', 'initial_budget_value', 'updated_budget_value',
    'committed_value', 'settled_value', 'paid_budget_value'
]

# Filter the DataFrame to only include columns that exist in the fact_table_columns
# This handles cases where some CSV columns might not be needed in the final table
df_to_insert = df[fact_table_columns]

# Convert all values to string for SQLite insertion if not already numeric
# Pandas' to_sql handles type conversion, but for manual cursor.execute, it's safer.
# However, for REAL types, ensure they are already float/int.
# For TEXT columns, ensure they are string.

# Iterate over DataFrame rows and insert into the expense_fact table
for index, row in df_to_insert.iterrows():
    try:
        # Prepare values. Convert all to string, except for REAL values which are already float.
        # SQLite is forgiving, but explicit conversion can prevent issues.
        values = []
        for col_name in fact_table_columns:
            val = row[col_name]
            if pd.isna(val): # Handle NaN values (e.g., from dropna)
                values.append(None)
            else:
                values.append(val)

        placeholders = ', '.join(['?'] * len(fact_table_columns))
        insert_sql = f'''
            INSERT INTO expense_fact ({', '.join(fact_table_columns)})
            VALUES ({placeholders})
        '''
        cursor.execute(insert_sql, tuple(values))
    except Exception as e:
        print(f"Error inserting row {index}: {row}. Error: {e}")
        # Optionally, you can log the error and continue, or break
        conn.rollback() # Rollback the transaction on error
        raise # Re-raise the exception after rollback to stop execution


conn.commit()
conn.close()

print("✅ Dados importados com sucesso para a tabela 'expense_fact'.")