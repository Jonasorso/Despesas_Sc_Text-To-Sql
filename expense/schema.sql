-- action definition
CREATE TABLE action (
    action_code TEXT PRIMARY KEY,
    action_name TEXT
);

-- economic_category definition
CREATE TABLE economic_category (
    category_code TEXT PRIMARY KEY,
    category_name TEXT
);

-- element definition
CREATE TABLE element (
    element_code TEXT PRIMARY KEY,
    element_name TEXT
);

-- funding_specification definition
CREATE TABLE funding_specification (
    specification_code TEXT PRIMARY KEY,
    specification_name TEXT
);

-- funding_source definition
CREATE TABLE funding_source (
    source_code TEXT PRIMARY KEY,
    source_name TEXT
);

-- function definition
CREATE TABLE function (
    function_code TEXT PRIMARY KEY,
    function_name TEXT
);

-- management definition
CREATE TABLE management (
    management_code TEXT PRIMARY KEY,
    management_name TEXT
);

-- expense_group definition
CREATE TABLE expense_group (
    group_code TEXT PRIMARY KEY,
    group_name TEXT
);

-- source_group definition
CREATE TABLE source_group (
    group_code TEXT PRIMARY KEY,
    group_name TEXT
);

-- application_modality definition
CREATE TABLE application_modality (
    modality_code TEXT PRIMARY KEY,
    modality_name TEXT
);

-- agency definition
CREATE TABLE agency (
    agency_code TEXT PRIMARY KEY,
    agency_name TEXT
);

-- power_branch definition
CREATE TABLE power_branch (
    power_code TEXT PRIMARY KEY,
    power_name TEXT
);

-- program definition
CREATE TABLE program (
    program_code TEXT PRIMARY KEY,
    program_name TEXT
);

-- subaction definition
CREATE TABLE subaction (
    subaction_code TEXT PRIMARY KEY,
    subaction_name TEXT
);

-- subelement definition
CREATE TABLE subelement (
    subelement_code TEXT PRIMARY KEY,
    subelement_name TEXT
);

-- subfunction definition
CREATE TABLE subfunction (
    subfunction_code TEXT PRIMARY KEY,
    subfunction_name TEXT
);

-- time definition
CREATE TABLE time (
    id INTEGER PRIMARY KEY,
    year INTEGER,
    month_number INTEGER,
    month TEXT,
    bimester_number INTEGER,
    bimester TEXT,
    trimester_number INTEGER,
    trimester TEXT,
    quadrimester_number INTEGER,
    quadrimester TEXT,
    semester_number INTEGER,
    semester TEXT
);

-- entity_type definition
CREATE TABLE entity_type (
    entity_type_code TEXT PRIMARY KEY,
    entity_type_name TEXT
);

-- source_type definition
CREATE TABLE source_type (
    type_code TEXT PRIMARY KEY,
    type_name TEXT
);

-- management_unit definition
CREATE TABLE management_unit (
    unit_code TEXT PRIMARY KEY,
    unit_name TEXT
);

-- usage definition
CREATE TABLE usage (
    usage_code TEXT PRIMARY KEY,
    usage_name TEXT
);

-- expense_fact definition
CREATE TABLE expense_fact (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    time_id INTEGER,
    power_code TEXT,
    agency_code TEXT,
    unit_code TEXT,
    management_code TEXT,
    entity_type_code TEXT,
    function_code TEXT,
    subfunction_code TEXT,
    program_code TEXT,
    action_code TEXT,
    subaction_code TEXT,
    usage_code TEXT,
    source_code TEXT,
    group_code TEXT,
    specification_code TEXT,
    type_code TEXT,
    category_code TEXT,
    expense_group_code TEXT,
    modality_code TEXT,
    element_code TEXT,
    subelement_code TEXT,
    creditor_code TEXT,
    emergency_indicator TEXT,
    initial_budget_value REAL,
    updated_budget_value REAL,
    committed_value REAL,
    settled_value REAL,
    paid_budget_value REAL,
    emergency_expense_description TEXT,
    CONSTRAINT FK_expense_fact_action FOREIGN KEY (action_code) REFERENCES action(action_code),
    CONSTRAINT FK_expense_fact_economic_category FOREIGN KEY (category_code) REFERENCES economic_category(category_code),
    CONSTRAINT FK_expense_fact_element FOREIGN KEY (element_code) REFERENCES element(element_code),
    CONSTRAINT FK_expense_fact_funding_specification FOREIGN KEY (specification_code) REFERENCES funding_specification(specification_code),
    CONSTRAINT FK_expense_fact_funding_source FOREIGN KEY (source_code) REFERENCES funding_source(source_code),
    CONSTRAINT FK_expense_fact_function FOREIGN KEY (function_code) REFERENCES function(function_code),
    CONSTRAINT FK_expense_fact_management FOREIGN KEY (management_code) REFERENCES management(management_code),
    CONSTRAINT FK_expense_fact_expense_group FOREIGN KEY (expense_group_code) REFERENCES expense_group(group_code),
    CONSTRAINT FK_expense_fact_source_group FOREIGN KEY (group_code) REFERENCES source_group(group_code),
    CONSTRAINT FK_expense_fact_application_modality FOREIGN KEY (modality_code) REFERENCES application_modality(modality_code),
    CONSTRAINT FK_expense_fact_agency FOREIGN KEY (agency_code) REFERENCES agency(agency_code),
    CONSTRAINT FK_expense_fact_program FOREIGN KEY (program_code) REFERENCES program(program_code),
    CONSTRAINT FK_expense_fact_subaction FOREIGN KEY (subaction_code) REFERENCES subaction(subaction_code),
    CONSTRAINT FK_expense_fact_subelement FOREIGN KEY (subelement_code) REFERENCES subelement(subelement_code),
    CONSTRAINT FK_expense_fact_subfunction FOREIGN KEY (subfunction_code) REFERENCES subfunction(subfunction_code),
    CONSTRAINT FK_expense_fact_time FOREIGN KEY (time_id) REFERENCES time(id),
    CONSTRAINT FK_expense_fact_entity_type FOREIGN KEY (entity_type_code) REFERENCES entity_type(entity_type_code),
    CONSTRAINT FK_expense_fact_source_type FOREIGN KEY (type_code) REFERENCES source_type(type_code),
    CONSTRAINT FK_expense_fact_management_unit FOREIGN KEY (unit_code) REFERENCES management_unit(unit_code),
    CONSTRAINT FK_expense_fact_usage FOREIGN KEY (usage_code) REFERENCES usage(usage_code)
);
