import plotly.express as px


def dimension_bar(df):
    fig = px.bar(
        df,
        x="Dimension",
        y="Score",
        text="Score",
        title="Data Quality Dimension Scores",
        color="Dimension"
    )
    fig.update_layout(
        showlegend=False,
        yaxis_range=[0, 100]
    )
    return fig


import pandas as pd
import plotly.express as px


def severity_donut(findings):

    severity_counts = (
        findings["Severity"]
        .value_counts()
        .rename_axis("Severity")
        .reset_index(name="Count")
    )

    fig = px.pie(
        severity_counts,
        names="Severity",
        values="Count",
        hole=0.5,
        title="Severity Breakdown"
    )

    fig.update_traces(
        textposition="inside",
        textinfo="percent+label"
    )

    fig.update_layout(
        height=450
    )

    return fig

def issue_distribution(findings):

    df = (
        findings.groupby("Dimension")
        .size()
        .reset_index(name="Issues")
        .sort_values(
            "Issues",
            ascending=True
        )
    )

    fig = px.bar(
        df,
        x="Issues",
        y="Dimension",
        orientation="h",
        title="Issues by Quality Dimension",
        text="Issues"
    )

    return fig

def dts_comparison_chart(
    before_score,
    after_score
):

    import pandas as pd
    import plotly.express as px

    df = pd.DataFrame({

        "Stage": [
            "Before Cleaning",
            "After Cleaning"
        ],

        "DTS Score": [
            before_score,
            after_score
        ]

    })

    fig = px.bar(

        df,

        x="Stage",

        y="DTS Score",

        text="DTS Score",

        title="Data Quality Improvement"

    )

    fig.update_layout(

        yaxis_range=[0, 100],

        height=450

    )

    return fig