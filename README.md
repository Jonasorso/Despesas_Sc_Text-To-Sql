# Despesas_Sc_Text-To-Sql
# Despesas_Sc_Text-To-Sql

Repositório que disponibiliza uma base de dados de despesas públicas do Estado de Santa Catarina, preparada para experimentos de Text-to-SQL (NL2SQL), com foco em consultas em português e inglês.

---

## 1. Visão geral

Este repositório reúne dados orçamentários e financeiros de despesas públicas do Estado de Santa Catarina, organizados para servir como:

- base de testes para modelos de Text-to-SQL em cenário zero-shot;
- conjunto de exemplos de consultas em linguagem natural (português/inglês) para geração de SQL;
- estudo de impacto de diferentes esquemas de banco de dados (tabela única vs. esquema em estrela).

A base foi construída a partir de dados públicos obtidos em portais oficiais de transparência do governo de Santa Catarina, com foco em despesas executadas por órgãos estaduais.

---

## 2. Estrutura da base de dados

A organização exata dos arquivos pode ser ajustada, mas a proposta geral é:

- um esquema em **tabela única** (modelo denormalizado);
- um esquema em **estrela** (modelo dimensional).

Exemplo de organização (sugestão):

- `data/`
  - `single_table/`
    - `despesas_sc_single_table.sqlite` ou `.csv`
  - `star_schema/`
    - `despesas_sc_star_schema.sqlite`  
    - (opcional) arquivos auxiliares `.csv`
- `docs/`
  - dicionário de dados, layout das colunas e exemplos de consultas
- `examples/`
  - exemplos de perguntas em português e inglês, com SQL esperado (quando disponível)

Adapte os nomes aos arquivos que você efetivamente colocar no repositório.

---

## 3. Esquemas de banco de dados

### 3.1. Esquema em estrela (star schema)

No esquema em estrela, os dados são organizados em:

- uma tabela fato de despesas (ex.: `fato_despesa` ou `expense_fact`);
- tabelas dimensão para tempo, órgão, função, categoria econômica etc.

Exemplo de ideia de estrutura (ajuste para o seu schema real):

- Tabela fato (ex.: `expense_fact`)
  - `id_expense`
  - `id_time`
  - `id_agency`
  - `id_function`
  - `amount`
  - `year`, `month`
  - outros atributos numéricos ou de chave estrangeira

- Dimensões (exemplos):
  - `time_dim(id_time, date, year, month, day, ... )`
  - `agency_dim(id_agency, agency_code, agency_name, ...)`
  - `function_dim(id_function, function_code, function_name, ...)`

### 3.2. Esquema em tabela única (single table)

No esquema em tabela única, os mesmos atributos são denormalizados em uma única tabela, por exemplo:

- `expenses_flat`
  - `date`
  - `year`
  - `month`
  - `agency_code`, `agency_name`
  - `function_code`, `function_name`
  - `amount`
  - demais colunas descritivas

---

## 4. Uso para Text-to-SQL

A base foi planejada para experimentos de Text-to-SQL em dois eixos principais:

1. **Idioma**
   - Perguntas e descrições de colunas em **português** e **inglês**.
   - Possibilita avaliar o impacto da língua da pergunta em relação à língua da base (nomes de tabelas e colunas).

2. **Esquema**
   - Comparação entre:
     - consultas sobre o **esquema em estrela**;
     - consultas sobre a **tabela única**.
   - Permite estudar como a complexidade estrutural do schema afeta a acurácia dos modelos.

Sugestão de usos:

- Avaliar modelos de LLM em cenário zero-shot, fornecendo apenas o schema e a pergunta.
- Comparar desempenho entre diferentes modelos abertos (multilíngues, focados em código, etc.).
- Investigar erros típicos de geração de SQL em contexto de dados governamentais.

---

## 5. Como começar

### 5.1. Clonar o repositório

```bash
git clone https://github.com/Jonasorso/Despesas_Sc_Text-To-Sql.git
cd Despesas_Sc_Text-To-Sql
