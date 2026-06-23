from connection import df
import pandas as pd
import altair as alt
import webbrowser
import os


# drops rows with missing rankings and forces clean numeric conversion
df['rank_numeric'] = pd.to_numeric(df['rank_2027'].astype(str).str.replace(r'[^\d]', '', regex=True), errors='coerce')
df = df.dropna(subset=['rank_numeric'])

# 2. Build the optimized chart configuration
chart = alt.Chart(df).mark_circle(size=50, opacity=0.7).encode(
    x=alt.X(
        'rank_numeric:Q', 
        title='2027 QS World Rank',
        scale=alt.Scale(domain=[1, 700]) 
    ),
    y=alt.Y(
        'overall_score:Q', 
        title='Overall Score'
    ),
    color=alt.Color('region:N', title='Global Region'),
    tooltip=[
        alt.Tooltip('rank_2027:N', title='Official Rank'),
        alt.Tooltip('university_name:N', title='University'),
        alt.Tooltip('country:N', title='Country'),
        alt.Tooltip('overall_score:Q', title='Overall Score'),
        alt.Tooltip('ar_score:Q', title='Academic Reputation Score'),
        alt.Tooltip('er_score:Q', title='Employer Reputation Score')
    ]
).properties(
    width='container',  
    height=500,         
    title='QS World University Rankings 2027: Rank vs. Score'
).interactive()

output_file = "index.html"
chart.save(output_file)
webbrowser.open('file://'+ os.path.realpath(output_file))


