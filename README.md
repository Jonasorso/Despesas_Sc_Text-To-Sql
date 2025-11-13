# Despesas_Sc_Text-To-Sql

Repository providing a public-spending database for the State of Santa Catarina (Brazil), prepared for Text-to-SQL (NL2SQL) experiments, with a focus on queries in Portuguese and English.

---

## 1. Overview

This repository gathers budget and expenditure data from the State of Santa Catarina, organized to serve as:

- a testbed for Text-to-SQL models in zero-shot scenarios;
- a set of natural language queries (Portuguese/English) for SQL generation;
- a study resource on how different database schemas (single table vs. star schema) affect performance.

The dataset was built from public data obtained from official transparency portals of the government of Santa Catarina, focusing on executed expenditures by state agencies.

---

## 2. Repository structure

The exact organization of files may vary, but the general idea is:

- one **single-table** schema (denormalized model);
- one **star schema** (dimensional model).

Example organization (you can adjust to match your actual files):

- `data/`
  - `single_table/`
    - `despesas_sc_single_table.sqlite` or `.csv`
  - `star_schema/`
    - `despesas_sc_star_schema.sqlite`  
    - (optional) auxiliary `.csv` files
- `docs/`
  - data dictionary, column layouts and query examples
- `examples/`
  - sample questions in Portuguese and English, with expected SQL (when available)

Please adapt names and paths to the files actually included in this repository.

---

## 3. Database schemas

### 3.1. Star schema

In the star schema, data are organized into:

- one expense fact table (e.g., `expense_fact` or `fato_despesa`);
- dimension tables for time, agency, function, economic category, etc.

Example structural idea (adjust to your real schema):

- Fact table (e.g., `expense_fact`)
  - `id_expense`
  - `id_time`
  - `id_agency`
  - `id_function`
  - `amount`
  - `year`, `month`
  - other numeric or foreign key attributes

- Dimensions (examples):
  - `time_dim(id_time, date, year, month, day, ...)`
  - `agency_dim(id_agency, agency_code, agency_name, ...)`
  - `function_dim(id_function, function_code, function_name, ...)`

### 3.2. Single-table schema

In the single-table schema, the same attributes are denormalized into a single table, for example:

- `expenses_flat`
  - `date`
  - `year`
  - `month`
  - `agency_code`, `agency_name`
  - `function_code`, `function_name`
  - `amount`
  - other descriptive columns

---

## 4. Text-to-SQL usage

The dataset was designed for Text-to-SQL experiments along two main axes:

1. **Language**
   - Questions and column descriptions in **Portuguese** and **English**.
   - Allows evaluation of the impact of query language relative to the language of the schema (table and column names).

2. **Schema**
   - Comparison between:
     - queries over the **star schema**;
     - queries over the **single-table** schema.
   - Enables studying how schema structural complexity affects model accuracy.

Suggested use cases:

- Evaluate LLMs in zero-shot mode, providing only the schema and the question.
- Compare performance across different open-source models (multilingual, code-oriented, etc.).
- Investigate typical SQL generation errors in the context of government finance data.

---

## 5. Getting started

### 5.1. Clone the repository

```bash
git clone https://github.com/Jonasorso/Despesas_Sc_Text-To-Sql.git
cd Despesas_Sc_Text-To-Sql
