import sys
from pathlib import Path

PROJECT_ROOT = (
    Path(__file__)
    .resolve()
    .parent
    .parent
)

if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(
        str(PROJECT_ROOT)
    )


import streamlit as st
import tempfile
from pathlib import Path

from src.engine import DATATSTYEngine
from data_loader import load_excel
from kpi import (
    extract_kpis,
    dimension_scores
)
from charts import (
    dimension_bar,
    severity_donut,
    issue_distribution,
    dts_comparison_chart
)
from theme import apply_theme

st.set_page_config(
    page_title="DATASTY | AI Data Dashboard",
    layout="wide"
)

apply_theme()

st.title("DATASTY | AI Data Dashboard")
st.divider()

st.subheader(
    "Upload Dataset"
)

uploaded_file = st.file_uploader(
    "Upload CSV or Excel File",
    type=["csv", "xlsx", "xls"]
)

if uploaded_file is not None:

    if st.button(
        "Analyze Dataset",
        type="primary"
    ):

        with st.spinner(
            "Running DATASTY Analysis..."
        ):

            temp_dir = Path(
                tempfile.gettempdir()
            )

            temp_file = (
                temp_dir /
                uploaded_file.name
            )

            with open(
                temp_file,
                "wb"
            ) as f:

                f.write(
                    uploaded_file.getbuffer()
                )

            engine = DATATSTYEngine(
                str(temp_file)
            )

            result = engine.run()

            st.session_state["analysis_result"] = result

        st.session_state["before_dts"] = (
                    result["before_dts"]
                )

        st.session_state["after_dts"] = (
                    result["after_dts"]
                )

        st.session_state["improvement"] = (
                    result["improvement"]
                )

        st.success(
                    "Analysis Completed Successfully!"
                )

        # st.metric(
        #     "Before DTS",
        #     result["before_dts"]
        # )

        # st.metric(
        #     "After DTS",
        #     result["after_dts"]
        # )

        # st.metric(
        #     "Improvement",
        #     result["improvement"]
        # )

        # st.metric(
        #     "AI Status",
        #     result["status"])
if "analysis_result" not in st.session_state:

    st.info(
        "Upload a dataset and click Analyze Dataset to begin."
    )

    st.stop()

# ======================
# DOWNLOAD SECTION
# ======================

# st.subheader(
#     "Downloads"
# )

# excel_file = open(
#     result["report_path"],
#     "rb"
# )

if "analysis_result" in st.session_state:

    result = st.session_state[
        "analysis_result"
    ]

    st.subheader(
        "Downloads"
    )

    with open(
        result["report_path"],
        "rb"
    ) as f:

        st.download_button(
            "📊 Download Excel Report",
            f,
            file_name=
            "DATASTY_Report.xlsx"
        )

    # with open(
    #     result["pdf_path"],
    #     "rb"
    # ) as f:

    #     st.download_button(
    #         "📄 Download PDF Report",
    #         f,
    #         file_name=
    #         "DATATSTY_Report.pdf"
    #     )

    with open(
        result["cleaned_path"],
        "rb"
    ) as f:

        st.download_button(
            "🧹 Download Cleaned Dataset",
            f,
            file_name=
            "cleaned_dataset.csv"
        )

# st.download_button(
#     label="Download PDF Report",
#     data=pdf_file,
#     file_name="DATATSTY_Report.pdf",
#     mime="application/pdf"
# )

# cleaned_file = open(
#     result["cleaned_path"],
#     "rb"
# )

# st.download_button(
#     label="Download Cleaned Dataset",
#     data=cleaned_file,
#     file_name="cleaned_dataset.csv",
#     mime="text/csv"
# )

try:

    sheets = load_excel()

    kpis = extract_kpis(
        sheets
    )

    findings = sheets.get(
        "Quality Findings"
    )

    if findings is None:

        findings = sheets.get(
            "Quality_Findings"
        )

    if findings is None:

        st.error(
            "Quality Findings sheet not found."
        )

        st.stop()

except Exception as e:

    st.error(
        f"Unable to load report: {e}"
    )

    st.stop()

st.sidebar.header(
            "DATASTY Filters"
        )


severity = st.sidebar.selectbox(
    "Severity",
    ["All"] +
    sorted(
        findings["Severity"]
        .dropna()
        .unique()
    )
)


dimension = st.sidebar.selectbox(
    "Dimension",
    ["All"] +
    sorted(
        findings["Dimension"]
        .dropna()
        .unique()
    )
)


filtered = findings.copy()


if severity != "All":

    filtered = filtered[
        filtered["Severity"] == severity
    ]


if dimension != "All":

    filtered = filtered[
        filtered["Dimension"] == dimension
    ]

# ==========================
# TABS
# ==========================

tab1, tab2, tab3 = st.tabs(
    [
        "📊 Executive Summary",
        "🔍 Quality Findings",
        "💡 Recommendations"
    ]
)

# ==================================
# TAB 1
# OVERVIEW
# ==================================

with tab1:

    col1, col2, col3, col4, col5 = st.columns(5)

    before_dts = st.session_state.get(
        "before_dts",
        kpis["dts_score"]
    )

    after_dts = st.session_state.get(
        "after_dts",
        kpis["dts_score"]
    )

    improvement = st.session_state.get(
        "improvement",
        0
    )

    col1.metric(
        "Before DTS",
        round(before_dts, 2)
    )

    col2.metric(
        "After DTS",
        round(after_dts, 2)
    )

    col3.metric(
        "Improvement",
        f"+{round(improvement,2)}"
    )

    col4.metric(
        "AI Status",
        kpis["ai_status"]
    )

    col5.metric(
        "Critical Issues",
        kpis["critical_issues"]
    )

    st.divider()

    st.subheader(
        "Data Quality Improvement"
    )

    st.plotly_chart(
        dts_comparison_chart(
            before_dts,
            after_dts
        ),
        use_container_width=True
    )

    st.divider()

    left, right = st.columns(2)

    dimension_df = dimension_scores(
        sheets
    )

    with left:

        st.plotly_chart(
            dimension_bar(
                dimension_df
            ),
            use_container_width=True
        )

    with right:

        st.plotly_chart(
            severity_donut(
                filtered
            ),
            use_container_width=True
        )

# ==================================
# TAB 2
# QUALITY FINDINGS
# ==================================

with tab2:

    st.subheader(
        "Issue Distribution"
    )

    st.plotly_chart(
        issue_distribution(
            filtered
        ),
        use_container_width=True
    )

    st.subheader(
        "Issue Explorer"
    )

    st.dataframe(
        filtered,
        use_container_width=True
    )

# ==================================
# TAB 3
# RECOMMENDATIONS
# ==================================

with tab3:

    try:

        recommendations_df = sheets[
            "Recommendations"
        ]

        st.dataframe(
            recommendations_df,
            use_container_width=True
        )

    except:

        st.info(
            "No recommendations available."
        )

# # ==================================
# # TAB 4
# # DOWNLOADS
# # ==================================

# with tab4:

#     st.subheader(
#         "Downloads"
#     )

#     csv = filtered.to_csv(
#         index=False
#     ).encode("utf-8")

#     st.download_button(
#         "Download Findings CSV",
#         data=csv,
#         file_name="DATATSTY_Findings.csv",
#         mime="text/csv"
#     )

#     st.info(
#         "Excel Report, PDF Report and Cleaned Dataset downloads will be added here next."
#     )