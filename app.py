import gradio as gr
import altair as alt
import numpy as np
import pandas as pd
from connection import df


df["rank_clean"] = df["rank_2027"].astype(str).str.split("-").str[0]
df["rank_numeric"] = pd.to_numeric(
    df["rank_clean"].str.replace(r"[^\d]","", regex=True), errors="coerce"
)
df=df.dropna(subset=["rank_numeric"])
df["overall_score_clean"]=df["overall_score"].fillna(0)
df["region"]=df["region"].astype(str).str.strip()
df["university_name_lower"]=df["university_name"].astype(str).str.lower()

is_band=df["rank_2027"].astype(str).str.contains("-")
np.random.seed(42)
df["rank_jittered"]=df["rank_numeric"].astype(float)
df.loc[is_band,"rank_jittered"] += np.random.uniform(0,15, size=is_band.sum())

def update_chart(search_query, selected_region):
    filtered_df = df.copy()
    if selected_region and selected_region != "All region":
        filtered_df = filtered_df[filtered_df["region"]==selected_region]

    if search_query:
        filtered_df = filtered_df[
            filtered_df["university_name_lower"].str.contains(search_query.lower())
        ]

    if filtered_df.empty:
        empty_chart=(
            alt.Chart(pd.DataFrame())
            .mark_text(fontSize=16, color="aliceblue", fontStyle="bold")
            .encode(text=alt.value("No universities found matching your search"))
            .properties(width=900, height=500)
        )
        return empty_chart
    
    chart=(
        alt.Chart(filtered_df).mark_circle(size=70, opacity=0.8, stroke="white", strokeWidth=0.4).encode(
            x=alt.X("rank_jittered:Q", title="2027 QS World Rank", scale=alt.Scale(domain=[1,1520])),
            y=alt.Y("overall_score_clean:Q", title="Overall Score"),
            color=alt.Color("region:N", title="Region", scale=alt.Scale(scheme="category10")),
            tooltip=[
                alt.Tooltip("rank_2027:N", title="Official Rank"),
                alt.Tooltip("university_name:N", title="University"),
                alt.Tooltip("country:N", title="Country"),
                alt.Tooltip("region:N", title="Region"),
                alt.Tooltip("overall_score:Q", title="Official Overall Score"),
                alt.Tooltip("ar_score:Q", title="Academic Reputation Score"),
                alt.Tooltip("er_score:Q", title="Employer Reputation Score")
            ],
        ).properties(width=900, height=500)
        .interactive()
        )
    return chart

regions_list=["All region"] + sorted(list(df["region"].unique()))

with gr.Blocks(title="QS World University Rankings 2027") as demo:
    gr.Markdown(
        """
        # QS World University Rankings 2027
        Type a university name in the search box or select a region from the dropdown to filter the universities displayed in the chart.
        """
    )

    with gr.Row():
        search_box=gr.Textbox(
            label="Search University",
            placeholder="Type a university name..."
        )
        region_dropdown = gr.Dropdown(
            choices=regions_list,
            value="All region",
            label="Filter by Region",
        )
    plot_output = gr.Plot(label="QS World Rankings Chart")

    search_box.change(fn=update_chart, inputs=[search_box, region_dropdown], outputs=plot_output)
    region_dropdown.change(fn=update_chart, inputs=[search_box, region_dropdown], outputs=plot_output)

    demo.load(fn=update_chart, inputs=[search_box, region_dropdown], outputs=plot_output)

if __name__ == "__main__":
    import os
    port=int(os.environ.get("PORT", 7860))
    demo.launch(server_name="0.0.0.0", server_port=port)