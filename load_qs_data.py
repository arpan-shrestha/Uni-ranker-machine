#column renaming and data insertion into postgresql database
import pandas as pd
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
print("Dataframe created successfully!!!")


#connection
from sqlalchemy import create_engine
engine = create_engine(
    "postgresql+psycopg2://arpanshrestha:@localhost:5432/qs_rankings"
)

df.to_sql(
    "universities",
    engine,
    if_exists="replace",
    index=False,
)
print("Data inserted successfully!!! Total rows inserted: ", len(df))