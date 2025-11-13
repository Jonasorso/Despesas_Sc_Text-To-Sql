-- acao definição

CREATE TABLE acao (
    cod_acao TEXT PRIMARY KEY,
    nome_acao TEXT
);


-- categoria_economica definição

CREATE TABLE categoria_economica (
    cod_categoria TEXT PRIMARY KEY,
    nome_categoria TEXT
);


-- elemento definição

CREATE TABLE elemento (
    cod_elemento TEXT PRIMARY KEY,
    nome_elemento TEXT
);


-- especificacao_fonte definição

CREATE TABLE especificacao_fonte (
    cod_especificacao TEXT PRIMARY KEY,
    nome_especificacao TEXT
);


-- fonte_recurso definição

CREATE TABLE fonte_recurso (
    cod_fonte TEXT PRIMARY KEY,
    nome_fonte TEXT
);


-- funcao definição

CREATE TABLE funcao (
    cod_funcao TEXT PRIMARY KEY,
    nome_funcao TEXT
);


-- gestao definição

CREATE TABLE gestao (
    cod_gestao TEXT PRIMARY KEY,
    nome_gestao TEXT
);


-- grupo_despesa definição

CREATE TABLE grupo_despesa (
    cod_grupo TEXT PRIMARY KEY,
    nome_grupo TEXT
);


-- grupo_fonte definição

CREATE TABLE grupo_fonte (
    cod_grupo TEXT PRIMARY KEY,
    nome_grupo TEXT
);


-- modalidade_aplicacao definição

CREATE TABLE modalidade_aplicacao (
    cod_modalidade TEXT PRIMARY KEY,
    nome_modalidade TEXT
);


-- orgao definição

CREATE TABLE orgao (
    cod_orgao TEXT PRIMARY KEY,
    nome_orgao TEXT
);


-- poder definição

CREATE TABLE poder (
    cod_poder TEXT PRIMARY KEY,
    nome_poder TEXT
);


-- programa definição

CREATE TABLE programa (
    cod_programa TEXT PRIMARY KEY,
    nome_programa TEXT
);


-- subacao definição

CREATE TABLE subacao (
    cod_subacao TEXT PRIMARY KEY,
    nome_subacao TEXT
);


-- subelemento definição

CREATE TABLE subelemento (
    cod_subelemento TEXT PRIMARY KEY,
    nome_subelemento TEXT
);


-- subfuncao definição

CREATE TABLE subfuncao (
    cod_subfuncao TEXT PRIMARY KEY,
    nome_subfuncao TEXT
);


-- tempo definição

CREATE TABLE tempo (
    id INTEGER PRIMARY KEY,
    ano INTEGER,
    nro_mes INTEGER,
    mes TEXT,
    nro_bimestre INTEGER,
    bimestre TEXT,
    nro_trimestre INTEGER,
    trimestre TEXT,
    nro_quadrimestre INTEGER,
    quadrimestre TEXT,
    nro_semestre INTEGER,
    semestre TEXT
);


-- tipo_entidade definição

CREATE TABLE tipo_entidade (
    cod_tipo_entidade TEXT PRIMARY KEY,
    nome_tipo_entidade TEXT
);


-- tipo_fonte definição

CREATE TABLE tipo_fonte (
    cod_tipo TEXT PRIMARY KEY,
    nome_tipo TEXT
);


-- unidade_gestora definição

CREATE TABLE unidade_gestora (
    cod_ug TEXT PRIMARY KEY,
    nome_ug TEXT
);


-- uso definição

CREATE TABLE uso (
    cod_uso TEXT PRIMARY KEY,
    nome_uso TEXT
);


-- fato_despesa definição

CREATE TABLE fato_despesa (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	tempo_id INTEGER,
	cod_poder TEXT,
	cod_orgao TEXT,
	cod_ug TEXT,
	cod_gestao TEXT,
	cod_tipo_entidade TEXT,
	cod_funcao TEXT,
	cod_subfuncao TEXT,
	cod_programa TEXT,
	cod_acao TEXT,
	cod_subacao TEXT,
	cod_uso TEXT,
	cod_fonte TEXT,
	cod_grupo TEXT,
	cod_especificacao TEXT,
	cod_tipo TEXT,
	cod_categoria TEXT,
	cod_grupo_despesa TEXT,
	cod_modalidade TEXT,
	cod_elemento TEXT,
	cod_subelemento TEXT,
	cod_credor TEXT,
	indicador_emergencial TEXT,
	vl_dotacao_inicial REAL,
	vl_dotacao_atualizada REAL,
	vl_empenhado REAL,
	vl_liquidado REAL,
	vl_pago_orcamentario REAL,
	descricao_despesa_emergencial TEXT,
	CONSTRAINT FK_fato_despesa_acao FOREIGN KEY (cod_acao) REFERENCES acao(cod_acao),
	CONSTRAINT FK_fato_despesa_categoria_economica_2 FOREIGN KEY (cod_categoria) REFERENCES categoria_economica(cod_categoria),
	CONSTRAINT FK_fato_despesa_elemento_5 FOREIGN KEY (cod_elemento) REFERENCES elemento(cod_elemento),
	CONSTRAINT FK_fato_despesa_especificacao_fonte_6 FOREIGN KEY (cod_especificacao) REFERENCES especificacao_fonte(cod_especificacao),
	CONSTRAINT FK_fato_despesa_fonte_recurso_7 FOREIGN KEY (cod_fonte) REFERENCES fonte_recurso(cod_fonte),
	CONSTRAINT FK_fato_despesa_funcao_8 FOREIGN KEY (cod_funcao) REFERENCES funcao(cod_funcao),
	CONSTRAINT FK_fato_despesa_gestao_9 FOREIGN KEY (cod_gestao) REFERENCES gestao(cod_gestao),
	CONSTRAINT FK_fato_despesa_grupo_despesa_10 FOREIGN KEY (cod_grupo_despesa) REFERENCES grupo_despesa(cod_grupo),
	CONSTRAINT FK_fato_despesa_grupo_fonte_11 FOREIGN KEY (cod_grupo) REFERENCES grupo_fonte(cod_grupo),
	CONSTRAINT FK_fato_despesa_modalidade_aplicacao_12 FOREIGN KEY (cod_modalidade) REFERENCES modalidade_aplicacao(cod_modalidade),
	CONSTRAINT FK_fato_despesa_orgao_13 FOREIGN KEY (cod_orgao) REFERENCES orgao(cod_orgao),
	CONSTRAINT FK_fato_despesa_programa_15 FOREIGN KEY (cod_programa) REFERENCES programa(cod_programa),
	CONSTRAINT FK_fato_despesa_subacao_16 FOREIGN KEY (cod_subacao) REFERENCES subacao(cod_subacao),
	CONSTRAINT FK_fato_despesa_subelemento_17 FOREIGN KEY (cod_subelemento) REFERENCES subelemento(cod_subelemento),
	CONSTRAINT FK_fato_despesa_subfuncao_18 FOREIGN KEY (cod_subfuncao) REFERENCES subfuncao(cod_subfuncao),
	CONSTRAINT FK_fato_despesa_tempo_19 FOREIGN KEY (tempo_id) REFERENCES tempo(id),
	CONSTRAINT FK_fato_despesa_tipo_entidade_20 FOREIGN KEY (cod_tipo_entidade) REFERENCES tipo_entidade(cod_tipo_entidade),
	CONSTRAINT FK_fato_despesa_tipo_fonte_21 FOREIGN KEY (cod_tipo) REFERENCES tipo_fonte(cod_tipo),
	CONSTRAINT FK_fato_despesa_unidade_gestora_22 FOREIGN KEY (cod_ug) REFERENCES unidade_gestora(cod_ug),
	CONSTRAINT FK_fato_despesa_uso_23 FOREIGN KEY (cod_uso) REFERENCES uso(cod_uso)
);