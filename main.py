from connection import df
import pandas as pd
import numpy as np
import altair as alt
import webbrowser
import os

alt.data_transformers.enable('default')

# clean rank bands (extracting 501 from 501-510, 601 from 601-650, etc.)
df["rank_clean"] = df["rank_2027"].astype(str).str.split("-").str[0]
df['rank_numeric'] = pd.to_numeric(df['rank_clean'].str.replace(r'[^\d]', '', regex=True), errors='coerce')

# drop rows with missing rank_numeric values
df = df.dropna(subset=['rank_numeric'])
# handling missing values in overall_score by filling them with 0
df["overall_score_clean"] = df["overall_score"].fillna(0)

# identify rows where rank_2027 contains a hyphen (indicating a band)
is_band = df["rank_2027"].astype(str).str.contains("-")

# seed the generator for stable rendering
np.random.seed(42)
df["rank_jittered"] = df["rank_numeric"].astype(float)

# give rank bands a random jitter to avoid overlapping points in the visualization
df.loc[is_band, "rank_jittered"] += np.random.uniform(0,15, size=is_band.sum())

selection = alt.selection_point(fields=["region"], bind="legend")


chart = alt.Chart(df).mark_circle(size=50, opacity=0.7).encode(
    x=alt.X(
        'rank_jittered:Q', 
        title='2027 QS World Rank',
        scale=alt.Scale(domain=[1, 1520], reverse=False) 
    ),
    y=alt.Y(
        'overall_score_clean:Q', 
        title='Overall Score'
    ),
    color=alt.Color('region:N', title='Global Region', scale=alt.Scale(scheme='category10')),
    
    opacity=alt.condition(selection, alt.value(0.7), alt.value(0.05)),
    tooltip=[
        alt.Tooltip('rank_2027:N', title='Official Rank'),
        alt.Tooltip('university_name:N', title='University'),
        alt.Tooltip('country:N', title='Country'),
        alt.Tooltip('region:N', title='Region'),
        alt.Tooltip('overall_score:Q', title='Official Overall Score'),
        alt.Tooltip('ar_score:Q', title='Academic Reputation Score'),
        alt.Tooltip('er_score:Q', title='Employer Reputation Score')
    ]
).properties(
    width='container',  
    height=500,         
    title=alt.TitleParams(
        text='QS World University Rankings 2027',
        fontSize=25,
        subtitle="Visualization of the QS World University Rankings for 2027, highlighting universities' overall scores and their global regions.",
        subtitleFontSize=18
    )
).add_params(
    selection
).configure_view(
    strokeOpacity=0
).interactive()

output_file = "index.html"
chart.save(output_file)
webbrowser.open('file://'+ os.path.realpath(output_file))


