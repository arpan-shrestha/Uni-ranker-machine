import os
from dotenv import load_dotenv
import pandas as pd
from sqlalchemy import create_engine

load_dotenv()
engine = create_engine(os.getenv("DATABASE_URL"))   
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

