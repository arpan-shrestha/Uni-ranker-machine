#column renaming and data insertion into postgresql database
import pandas as pd
import numpy as np
df = pd.read_excel("2027 QS World University Rankings 1.1 (For qs.com).xlsx", header = 1)
df.columns = [
    "index",
    "rank_2027",
    "rank_2026",
    "university_name",
    "country",
    "region",
    "size",
    "focus",
    "research",
    "status",
    "ar_score",
    "ar_rank",
    "er_score",
    "er_rank",
    "fsr_score",
    "fsr_rank",
    "cpf_score",
    "cpf_rank",
    "ifr_score",
    "ifr_rank",
    "isr_score",
    "isr_rank",
    "irn_score",
    "irn_rank",
    "eo_score",
    "eo_rank",
    "sus_score",
    "sus_rank",
    "overall_score"
]
df = df.drop(columns=["index"])
# drop duplicate text header row
df = df[df["rank_2027"] != "Rank"]
# Convert string hyphen into real numeric NULLS
score_columns = [
    "ar_score",
    "er_score",
    "fsr_score",
    "cpf_score",
    "ifr_score",
    "isr_score",
    "irn_score",
    "eo_score",
    "sus_score",
    "overall_score"
]
for col in score_columns:
    df[col] = df[col].replace(r"^\s*-\s*$", np.nan, regex=True) 
    df[col] = pd.to_numeric(df[col],errors="coerce")

print("Dataframe created successfully!!!")


#connection
from sqlalchemy import create_engine, text
engine = create_engine(
    "postgresql+psycopg2://arpanshrestha:@localhost:5432/qs_rankings"
)
with engine.begin() as conn:
    conn.execute(text("TRUNCATE TABLE universities;"))

df.to_sql(
    "universities",
    engine,
    if_exists="append",
    index=False,
)
print("Data inserted successfully!!! Total rows inserted: ", len(df))