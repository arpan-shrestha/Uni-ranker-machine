DROP TABLE IF EXISTS universities;

CREATE TABLE universities(
    rank_2027 TEXT,
    rank_2026 TEXT,

    university_name TEXT,
    country TEXT,
    region TEXT,

    size VARCHAR(10),
    focus VARCHAR(10),
    research VARCHAR(10),
    status TEXT,

    ar_score FLOAT,
    ar_rank VARCHAR(10),

    er_score FLOAT,
    er_rank VARCHAR(10),

    fsr_score FLOAT,
    fsr_rank VARCHAR(10),

    cpf_score FLOAT,
    cpf_rank VARCHAR(10),

    ifr_score FLOAT,
    ifr_rank VARCHAR(10),

    isr_score FLOAT,
    isr_rank VARCHAR(10),

    irn_score FLOAT,
    irn_rank VARCHAR(10),

    eo_score FLOAT, 
    eo_rank VARCHAR(10),

    sus_score FLOAT,
    sus_rank VARCHAR(10),

    overall_score FLOAT
);
