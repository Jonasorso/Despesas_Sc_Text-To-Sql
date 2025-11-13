
import json

def load_spider_examples(path, schema_path="data/spider/tables.json"):
    with open(path, encoding="utf-8") as f:
        examples = json.load(f)

    with open(schema_path, encoding="utf-8") as f:
        schemas = json.load(f)

    schema_map = {s["db_id"]: s for s in schemas}

    for ex in examples:
        ex["schema"] = parse_schema(schema_map[ex["db_id"]])
    
    return examples

def parse_schema(schema):
    tables = []
    for i, table_name in enumerate(schema["table_names_original"]):
        column_names = [
            col[1]
            for col in schema["column_names_original"]
            if col[0] == i
        ]
        tables.append({
            "table_name": table_name,
            "columns": column_names
        })
    return {"tables": tables}
