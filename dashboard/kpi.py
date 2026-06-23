def extract_kpis(sheets):

    summary = sheets["Executive_Summary"]

    findings = sheets["Quality_Findings"]

    return {

        "dts_score": float(
            summary.loc[0, "DTS Score"]
        ),

        "ai_status": summary.loc[0, "AI Readiness"],

        "total_issues": len(findings),

        "critical_issues": (
            findings["Severity"] == "Critical"
        ).sum(),

        "dimensions": (
            findings["Dimension"]
            .nunique()
        )
    }

def dimension_scores(sheets):

    summary = sheets["Executive_Summary"]

    scores = []

    # Read all dimension scores
    for column in [
        "Completeness",
        "Uniqueness",
        "Validity",
        "Consistency",
        "Accuracy"
    ]:

        if column in summary.columns:

            scores.append({
                "Dimension": column,
                "Score": summary.loc[0, column]
            })

    import pandas as pd

    return pd.DataFrame(scores)
