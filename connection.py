import pandas as pd
from sqlalchemy import create_engine

engine = create_engine(
    "postgresql+psycopg2://arpanshrestha:@localhost:5432/qs_rankings"
)   
query = """
SELECT
    rank_2027,
    university_name,
    country,
    region,
    overall_score,
    ar_score,
    er_score
FROM universities
    """

df = pd.read_sql(query, engine)

