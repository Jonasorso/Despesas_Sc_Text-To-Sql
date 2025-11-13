import sqlite3

# Conecta (ou cria) o banco SQLite
conn = sqlite3.connect("despesas_consolidada.db")
cursor = conn.cursor()

# Lê o script SQL do schema
with open("/home/jonas/nl2sql/data/despesas_consolidada/schema.sql", "r", encoding="utf-8") as f:
    schema_sql = f.read()

# Executa o script SQL para criar as tabelas
cursor.executescript(schema_sql)
conn.commit()
conn.close()

print("Banco de dados e tabelas criadas com sucesso.")
